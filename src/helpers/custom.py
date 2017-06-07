import sys
import os
import datetime
import json
import random
import numpy as np
import cv2
from PIL import Image
from helpers.common import *
from helpers.models.inception_v3 import inception_v3

'''
In this file we will specify all the custom methods, 
that can/will be different from game to game.
'''

# Preparation
now = datetime.datetime.now()
data_dir = get_data_dir()
args = get_args()

activity = args['activity']
mode = args['mode']
network_dir = os.path.join(data_dir, activity, 'network', mode)
network_logs_dir = os.path.join(network_dir, 'logs')
network_checkpoint_path = os.path.join(network_dir, 'checkpoint.tflearn')
network_model_path = os.path.join(network_dir, 'model.tflearn')

controls_map = {
    'forward': [1, 0, 0, 0, 0, 0, 0, 0, 0],
    'backward': [0, 1, 0, 0, 0, 0, 0, 0, 0],
    'left': [0, 0, 1, 0, 0, 0, 0, 0, 0],
    'right': [0, 0, 0, 1, 0, 0, 0, 0, 0],
    'forward+left': [0, 0, 0, 0, 1, 0, 0, 0, 0],
    'forward+right': [0, 0, 0, 0, 0, 1, 0, 0, 0],
    'backward+left': [0, 0, 0, 0, 0, 0, 1, 0, 0],
    'backward+right': [0, 0, 0, 0, 0, 0, 0, 1, 0],
    'none': [0, 0, 0, 0, 0, 0, 0, 0, 0],
}

# Methods


def get_processed_image_size():
    return (640, 480)


def get_toggle_capture_hotkeys():
    return ['left_control', 'F11'] # View the full list inside src/capture/keyboard.py


def get_epochs():
    return 64


def get_xy_batch_size():
    return 512


def get_device(action='train'):
    return '/cpu:0'


def get_validation_set_percentage():
    return 0.1


def preprocess_image(image):
    image = image.resize(get_processed_image_size(), Image.ANTIALIAS)

    image_array = np.array(image)

    image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)

    return image_array # MUST return a np.array()


def get_image_processing_data_row(processed_image_path, inputs):
    return {
        'image_path': processed_image_path,
        'controls': get_controls_from_inputs(inputs),
    }


def get_controls_from_inputs(inputs):
    forward = inputs['keyboard']['w'] or inputs['gamepad']['axes']['right_trigger'] > 0
    backward = inputs['keyboard']['s'] or inputs['gamepad']['axes']['left_trigger'] > 0
    left = inputs['keyboard']['a'] or inputs['gamepad']['axes']['left']['x'] < 0
    right = inputs['keyboard']['d'] or inputs['gamepad']['axes']['left']['x'] > 0

    return {
        'forward': forward,
        'backward': backward,
        'left': left,
        'right': right,
    }


def convert_controls_to_array(controls):
    output = controls_map['none']

    left = 'left' in controls and controls['left']
    right = 'right' in controls and controls['right']
    forward = 'forward' in controls and controls['forward']
    backward = 'backward' in controls and controls['backward']
    forwardLeft = (forward and left)
    forwardRight = (forward and right)
    backwardLeft = (backward and left)
    backwardRight = (backward and right)
    
    if forwardLeft:
        output = controls_map['forward+left']
    elif forwardRight:
        output = controls_map['forward+right']
    elif backwardLeft:
        output = controls_map['backward+left']
    elif backwardRight:
        output = controls_map['backward+right']
    elif forward:
        output = controls_map['forward']
    elif backward:
        output = controls_map['backward']
    elif left:
        output = controls_map['left']
    elif right:
        output = controls_map['right']

    return output


def get_xy():
    X = []
    Y = []
    batch_size = get_xy_batch_size()

    processed_dir = os.path.join(data_dir, activity, 'processed', mode)
    processed_data_file_path = os.path.join(processed_dir, 'data.txt')
    processed_data_file = open(processed_data_file_path, 'r+').read()
    processed_data = processed_data_file.split("\n")
    processed_data = list(filter(None, processed_data))

    random.shuffle(processed_data)

    rows = 1
    for row in processed_data:
        # that returns the same results as defined in the get_image_processing_data_row()
        row_data = json.loads(row)

        X.append(np.array(Image.open(row_data['image_path'])))
        Y.append(convert_controls_to_array(row_data['controls']))

        rows += 1

        if rows > batch_size:
            break

    return X, Y


def get_model(load_existing=False):
    # Prepare dirs
    if not os.path.exists(network_logs_dir):
        os.makedirs(network_logs_dir)

    # Prepare data
    input2_size, input1_size = get_processed_image_size()
    output_size = len(convert_controls_to_array({}))

    # Return the model
    model = inception_v3(
        input1_size,
        input2_size,
        output_size,
        tensorboard_dir=network_logs_dir,
        checkpoint_path=network_checkpoint_path,
        best_checkpoint_path=network_checkpoint_path
    )

    if load_existing:
        model.load(network_model_path)

    return model


def save_model(model):
    # TODO: make backups/archives?
    model.save(network_model_path)


def get_prediction(model, X):
    action = None
    prediction = model.predict([X])
    prediction = prediction[0]
    sys.stdout.flush()

    max_index = np.argmax(prediction)

    # View controls_map dict to see, which output corresponds to which action
    # TODO: shorter version of it?
    if max_index == 0:
        action = 'forward'
    elif max_index == 1:
        action = 'backward'
    elif max_index == 2:
        action = 'left'
    elif max_index == 3:
        action = 'right'
    elif max_index == 4:
        action = 'forward+left'
    elif max_index == 5:
        action = 'forward+right'
    elif max_index == 6:
        action = 'backward+left'
    elif max_index == 7:
        action = 'backward+right'

    return {
        'action': action,
        'action_confidence': prediction[max_index],
        'raw': prediction,
    }


def get_model_run_id():
    return now.strftime('%Y%m%d_%H%M%S') + '_' + '{0}_{1}'.format(activity, mode)
