import sys
import os
import datetime
import json
import random
import numpy as np
import cv2
from PIL import Image
from helpers.common import *
from helpers.input import press_keyboard_key, release_keyboard_key
from helpers.actions.capture import CaptureAction
from helpers.actions.process import ProcessAction
from helpers.actions.train import TrainAction
from helpers.actions.evaluate import EvaluateAction
from helpers.models.inception_v3 import inception_v3


class DefaultNetwork:

    args = get_args()

    model = None
    device = '/cpu:0'
    size = (640, 480)  # (width, height)
    train_iterations = 128
    train_batch_size = 256
    train_epochs = 1
    train_shuffle_data = False
    validation_set_percentage = 0.1  # 0.1 = 10%
    # All hotkeys: src/capture/keyboard.py
    toggle_capture_hotkeys = ['left_control', 'F11']
    toggle_evaluate_hotkeys = ['left_control', 'F10']

    def __init__(self):
        self.activity = self.args['activity']
        self.mode = self.args['mode']
        self.force_new_model = self.args['force_new_model']
        self.network_dir = os.path.join(
            get_data_dir(), self.activity, 'network', self.mode)
        self.network_logs_dir = os.path.join(self.network_dir, 'logs')
        self.network_checkpoint_path = os.path.join(
            self.network_dir, 'checkpoint.tflearn')
        self.network_model_path = os.path.join(
            self.network_dir, 'model.tflearn')
        self.processed_dir = os.path.join(
            get_data_dir(), self.activity, 'processed', self.mode)
        self.processed_data_file_path = os.path.join(
            self.processed_dir, 'data.txt')

    def get_xy(self, iteration):
        X = []
        Y = []

        processed_data_file = open(self.processed_data_file_path, 'r+').read()
        processed_data = processed_data_file.split("\n")
        processed_data = list(filter(None, processed_data))

        if self.train_shuffle_data:
            random.shuffle(processed_data)

        from_index, to_index = get_from_and_to_index(iteration=iteration,
                                                     batch_size=self.train_batch_size,
                                                     total_size=len(processed_data))
        processed_data = processed_data[from_index:to_index]

        for row in processed_data:
            row_data = json.loads(row)

            X.append(np.array(Image.open(row_data['image_path'])))
            Y.append(self.convert_controls_to_array(row_data['controls']))

        return X, Y

    # Model related stuff
    def prepare_model(self, load_existing=True):
        # Prepare dirs
        if not os.path.exists(self.network_logs_dir):
            os.makedirs(self.network_logs_dir)

        # Prepare data
        input2_size, input1_size = self.size
        output_size = len(self.convert_controls_to_array({}))

        # Return the model
        self.model = inception_v3(
            input1_size,
            input2_size,
            output_size,
            tensorboard_dir=self.network_logs_dir,
            checkpoint_path=self.network_checkpoint_path,
            best_checkpoint_path=self.network_checkpoint_path
        )

        if load_existing and not self.force_new_model:
            self.model.load(self.network_model_path)

        return self.model

    def get_model(self):
        if self.model is None:
            sys.exit('Exiting. You need to run prepare_model() first')

        return self.model

    def save_model(self, model):
        model = self.get_model()
        return model.save(self.network_model_path)

    def fit_model(self, X, Y, model_run_id):
        return model.fit(
            X, Y,
            validation_set=self.validation_set_percentage,
            n_epoch=self.train_epochs,
            show_metric=True,
            snapshot_epoch=False,
            run_id=model_run_id)

    def get_model_prediction(self, X, controls_map):
        action = None

        prediction = self.model.predict([X])
        prediction = prediction[0]

        max_index = np.argmax(prediction)

        # View controls_map dict to see, which output corresponds to which
        # action
        for control, output in controls_map.items():
            control_max_index = np.argmax(output)
            if max_index == control_max_index:
                action = control

        return {
            'action': action,
            'action_confidence': prediction[max_index],
        }

    def get_model_run_id(self):
        now = datetime.datetime.now()
        return now.strftime('%Y%m%d_%H%M%S') + '_' + \
            '{0}_{1}'.format(self.activity, self.mode)

    def trigger_action(self, action):
        if action == 'forward' or action == 'forward+left' or action == 'forward+right':
            press_keyboard_key('w')
        else:
            release_keyboard_key('w')

        if action == 'backward' or action == 'backward+left' or action == 'backward+right':
            press_keyboard_key('s')
        else:
            release_keyboard_key('s')

        if action == 'left' or action == 'forward+left' or action == 'backward+left':
            press_keyboard_key('a')
        else:
            release_keyboard_key('a')

        if action == 'right' or action == 'forward+right' or action == 'backward+right':
            press_keyboard_key('a')
        else:
            release_keyboard_key('a')

        if action == 'none':
            release_keyboard_key('w')
            release_keyboard_key('s')
            release_keyboard_key('a')
            release_keyboard_key('d')

    # Helpers
    def get_device(self, action='train'):
        return self.device

    def preprocess_image(self, image):
        image = image.resize(self.size, Image.ANTIALIAS)

        image_array = np.array(image)

        image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)

        return image_array  # MUST return a np.array()

    def process_image(self, image, return_array=False):
        if isinstance(image, str):
            image = Image.open(image)

        processed_image_array = self.preprocess_image(image)

        if return_array:
            return processed_image_array

        return Image.fromarray(processed_image_array)

    def get_image_processing_data_row(self, processed_image_path, inputs):
        return {
            'image_path': processed_image_path,
            'controls': self.get_controls_from_inputs(inputs),
        }

    def get_controls_from_inputs(self, inputs):
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

    def get_controls_map(self):
        return {
            'forward': [1, 0, 0, 0, 0, 0, 0, 0, 0],
            'backward': [0, 1, 0, 0, 0, 0, 0, 0, 0],
            'left': [0, 0, 1, 0, 0, 0, 0, 0, 0],
            'right': [0, 0, 0, 1, 0, 0, 0, 0, 0],
            'forward+left': [0, 0, 0, 0, 1, 0, 0, 0, 0],
            'forward+right': [0, 0, 0, 0, 0, 1, 0, 0, 0],
            'backward+left': [0, 0, 0, 0, 0, 0, 1, 0, 0],
            'backward+right': [0, 0, 0, 0, 0, 0, 0, 1, 0],
            'none': [0, 0, 0, 0, 0, 0, 0, 0, 1],
        }

    def convert_controls_to_array(self, controls):
        controls_map = self.get_controls_map()

        left = 'left' in controls and controls['left']
        right = 'right' in controls and controls['right']
        forward = 'forward' in controls and controls['forward']
        backward = 'backward' in controls and controls['backward']
        forwardLeft = (forward and left)
        forwardRight = (forward and right)
        backwardLeft = (backward and left)
        backwardRight = (backward and right)

        output = controls_map['none']

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

    # Main methods
    def capture(self):
        captureAction = CaptureAction(self)
        captureAction.capture()

    def process(self):
        processAction = ProcessAction(self)
        processAction.process()

    def train(self):
        trainAction = TrainAction(self)
        trainAction.train()

    def evaluate(self):
        evaluateAction = EvaluateAction(self)
        evaluateAction.evaluate()
