import sys
import os
import datetime
import time
import tensorflow as tf
from helpers.common import *

class EvaluateAction:
    
    network = None
    
    def __init__(self, network):
        self.network = network

    def evaluate(self):
        now = datetime.datetime.now()

        print('Loading model ...')
        sys.stdout.flush()

        with tf.device(self.network.get_device(action='evaluate')):
            model = self.network.get_model()

        last_time = time.time()
        controls_map = self.network.get_controls_map()

        print('Start at {0}'.format(now))
        print('=' * 32)
        sys.stdout.flush()

        while True:
            original_image = grab_image()
            X = self.network.process_image(original_image, return_array=True)

            with tf.device(self.network.get_device(action='evaluate')):
                prediction = get_prediction(model, X, controls_map)
                print('Prediction: {0}.'.format(prediction))
                sys.stdout.flush()

            print('Last execution took {0} seconds.'.format(
                time.time() - last_time))
            sys.stdout.flush()

            last_time = time.time()
