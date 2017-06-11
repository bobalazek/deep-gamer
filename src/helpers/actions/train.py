import sys
import time
import datetime
import tensorflow as tf
from helpers.common import *


class TrainAction:

    network = None
    is_capturing = False  # If we should be capturing
    inputs = None  # Saves the current input on every tick

    args = get_args()

    def __init__(self, network):
        self.network = network

    def train(self):
        now = datetime.datetime.now()

        print('Start at {0}'.format(now))
        print('=' * 32)
        sys.stdout.flush()

        with tf.device(self.network.get_device(action='train')):
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

        model_run_id = self.network.get_model_run_id()

        for iteration in range(self.network.train_iterations):
            print('Starting iteration #{0}'.format(iteration))
            sys.stdout.flush()

            X, Y = self.network.get_xy(iteration=iteration)

            with tf.device(self.network.get_device(action='train')):
                self.network.fit_model(X, Y, model_run_id)

            print('Saving model ...')
            sys.stdout.flush()

            self.network.save_model()

            print('Model saved.')
            print('=' * 32)
            sys.stdout.flush()
