import sys
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
        
        print('Loading model ...')
        sys.stdout.flush()

        with tf.device(self.network.get_device(action='train')):
            model = self.network.get_model(force_new_model=self.args['force_new_model'])

        model_run_id = self.network.get_model_run_id()

        print('Start at {0}'.format(now))
        print('=' * 32)
        sys.stdout.flush()

        for iteration in range(self.network.train_iterations):
            print('Starting iteration #{0}'.format(iteration))
            sys.stdout.flush()

            X, Y = self.network.get_xy(iteration=iteration)

            with tf.device(self.network.get_device(action='train')):
                model.fit(
                    X, Y,
                    validation_set=self.network.validation_set_percentage,
                    n_epoch=self.network.train_epochs,
                    show_metric=True,
                    snapshot_epoch=False,
                    run_id=model_run_id)

            print('Saving model ...')
            sys.stdout.flush()

            save_model(model)

            print('Model saved.')
            print('=' * 32)
            sys.stdout.flush()
