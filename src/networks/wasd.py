import os
import datetime
import json
import random
import numpy as np
import cv2
from PIL import Image
from helpers.common import *
from helpers.input import press_keyboard_key, release_keyboard_key
from helpers.models.inception_v3 import inception_v3
from networks.abstract import AbstractNetwork


'''
The typical network for driving games - WASD (forward, left, backward, right).
'''


class WASDNetwork(AbstractNetwork):

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

        model_file_exists = os.path.isfile(self.network_model_path + '.index')

        if load_existing and not self.force_new_model and model_file_exists:
            self.model.load(self.network_model_path)

        return self.model

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
    def process_image(self, image, return_array=False):
        if isinstance(image, str):
            image = Image.open(image)

        # Do processing
        processed_image = image.resize(self.size, Image.ANTIALIAS)
        processed_image_array = np.array(processed_image)
        processed_image_array = cv2.cvtColor(
            processed_image_array, cv2.COLOR_BGR2RGB)

        if return_array:
            return processed_image_array

        return Image.fromarray(processed_image_array)

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
