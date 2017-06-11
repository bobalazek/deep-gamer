import sys
import os
import datetime
import time
import tensorflow as tf
from helpers.common import *


class EvaluateAction:

    network = None
    is_evaluating = False

    def __init__(self, network):
        self.network = network

    def evaluate(self):
        now = datetime.datetime.now()

        print('Start at {0}'.format(now))
        print('=' * 32)
        sys.stdout.flush()

        with tf.device(self.network.get_device(action='evaluate')):
            loading_model_start = time.time()

            print('Loading model ...')
            sys.stdout.flush()

            self.network.prepare_model()

            print(
                'Model loaded. It took {0} seconds to load.'.format(
                    time.time() -
                    loading_model_start))
            print('=' * 32)
            sys.stdout.flush()

        last_time = time.time()
        controls_map = self.network.get_controls_map()

        print('To start/stop evaluating, press: {0}'.format(
            ' & '.join(self.network.toggle_evaluate_hotkeys)))
        print('=' * 32)
        sys.stdout.flush()

        while True:
            self.inputs = get_inputs()

            if check_for_capturing_hotkeys(
                    self.inputs['keyboard'], self.network.toggle_evaluate_hotkeys):
                self.is_evaluating = not self.is_evaluating

            if self.is_evaluating:
                original_image = grab_image()
                X = self.network.process_image(
                    original_image, return_array=True)

                with tf.device(self.network.get_device(action='evaluate')):
                    prediction = self.network.get_model_prediction(X, controls_map)
                    print('Prediction: {0}.'.format(prediction))
                    sys.stdout.flush()

                print('Last execution took {0} seconds.'.format(
                    time.time() - last_time))
                sys.stdout.flush()

            last_time = time.time()
