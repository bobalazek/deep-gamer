import os, datetime, json
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
network_checkpoint_dir = os.path.join(network_dir, 'checkpoint')
network_logs_dir = os.path.join(network_dir, 'logs')

# Methods
# MUST return a tuple
def get_processed_image_size():
    return (640, 480)

# MUST return an array
# View the full list inside src/capture/keyboard.py
def get_toggle_capture_hotkeys():
    return ['left_control', 'F11']

# MUST return an integer
def get_epochs():
    return 32

# MUST return a np.array()
def preprocess_image(image):
    image = image.resize(get_processed_image_size(), Image.ANTIALIAS)

    image_array = np.array(image)

    image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)

    return image_array

# MUST return a dictionary
def get_image_processing_data_row(processed_image_path, inputs):
    return {
        'image_path': processed_image_path,
        'controls': get_controls_from_inputs(inputs),
    }

def get_controls_from_inputs(inputs):
    forward = inputs['keyboard']['w'] or inputs['gamepad']['axes']['right_trigger'] > 0
    backward = inputs['keyboard']['s'] or inputs['gamepad']['axes']['left_trigger'] > 0
    left = inputs['keyboard']['a'] or  inputs['gamepad']['axes']['left']['x'] < 0
    right = inputs['keyboard']['d'] or inputs['gamepad']['axes']['left']['x'] > 0
    
    return {
        'forward': forward,
        'backward': backward,
        'left': left,
        'right': right,
    }

def convert_controls_to_array(controls):
    forward = 'forward' in controls and controls['forward']
    backward = 'backward' in controls and controls['backward']
    left = 'left' in controls and controls['left']
    right = 'right' in controls and controls['right']
    
    return [
        forward and 1 or 0, # forward
        backward and 1 or 0, # backward
        left and 1 or 0, # left
        left and 1 or 0, # right
        (forward and left) and 1 or 0, # forward+left
        (forward and right) and 1 or 0, # backward+right
    ]

def get_xy():
    X = []
    Y = []

    processed_dir = os.path.join(data_dir, activity, 'processed', mode)
    processed_data_file_path = os.path.join(processed_dir, 'data.txt')
    processed_data_file = open(processed_data_file_path, 'r+').read()
    processed_data = processed_data_file.split("\n")
    processed_data = [x for x in processed_data if x != ''] # TODO: find a quicker solution? filter()?

    for row in processed_data:
        row_data = json.loads(row) # that returns the same results as defined in the get_image_processing_data_row()

        X.append(np.array(Image.open(row_data['image_path'])))
        Y.append(convert_controls_to_array(row_data['controls']))

    return X, Y

def get_model():
    # Prepare dirs
    if not os.path.exists(network_checkpoint_dir):
        os.makedirs(network_checkpoint_dir)
    
    if not os.path.exists(network_logs_dir):
        os.makedirs(network_logs_dir)
    
    width, height = get_processed_image_size()

    return inception_v3(
        height,
        width,
        len(convert_controls_to_array({})),
        tensorboard_dir=network_logs_dir
    )

def save_model(model):
    model.save(os.path.join(network_dir, 'network.tflearn'))

def get_model_run_id():
    return now.strftime('%Y%m%d_%H%M%S') + '_' + '{0}_{1}'.format(activity, mode)
