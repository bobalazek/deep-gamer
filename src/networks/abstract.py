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


class AbstractNetwork:

    args = get_args()

    model = None
    device = '/cpu:0'
    size = (640, 360)  # (width, height)
    train_iterations = 128
    train_batch_size = 256
    train_epochs = 1
    train_shuffle_data = False
    validation_set_percentage = 0.1  # 0.1 = 10%
    # All hotkeys: src/capture/keyboard.py
    toggle_capture_hotkeys = ['left_control', 'F11']
    toggle_evaluate_hotkeys = ['left_control', 'F10']

    def __init__(self):
        self.game = self.args['game']
        self.activity = self.args['activity']
        self.mode = self.args['mode']
        self.force_new_model = self.args['force_new_model']

        self.network_dir = os.path.join(
            get_data_dir(), self.game, self.activity, 'network', self.mode)
        self.network_logs_dir = os.path.join(self.network_dir, 'logs')
        self.network_checkpoint_path = os.path.join(
            self.network_dir, 'checkpoint.tflearn')
        self.network_model_path = os.path.join(
            self.network_dir, 'model.tflearn')
        self.processed_dir = os.path.join(
            get_data_dir(), self.game, self.activity, 'processed', self.mode)
        self.processed_data_file_path = os.path.join(
            self.processed_dir, 'data.txt')

        # Prepare dirs
        if not os.path.exists(self.network_logs_dir):
            os.makedirs(self.network_logs_dir)

    def get_xy(self, iteration):
        raise NotImplementedError('You need to implement this method.')

    def prepare_model(self, load_existing=True):
        raise NotImplementedError('You need to implement this method.')

    def get_model(self):
        return self.model

    def save_model(self):
        return self.model.save(self.network_model_path)

    def fit_model(self, X, Y, model_run_id):
        return self.model.fit(
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
        raise NotImplementedError('You need to implement this method.')

    # Helpers
    def get_device(self, action='train'):
        return self.device

    def process_image(self, image, return_array=False):
        raise NotImplementedError('You need to implement this method.')

    def get_image_processing_data_row(self, processed_image_path, inputs):
        return {
            'image_path': processed_image_path,
            'controls': self.get_controls_from_inputs(inputs),
        }

    def get_controls_from_inputs(self, inputs):
        raise NotImplementedError('You need to implement this method.')

    def get_controls_map(self):
        raise NotImplementedError('You need to implement this method.')

    def convert_controls_to_array(self, controls):
        raise NotImplementedError('You need to implement this method.')

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
