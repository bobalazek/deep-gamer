import sys
import datetime
import tensorflow as tf
from custom import *
from helpers.common import *

# Preparation
now = datetime.datetime.now()
args = get_args()

def train():
    print('Loading model ...')
    sys.stdout.flush()

    with tf.device(get_device(action='train')):
        model = get_model(force_new_model=args['force_new_model'])

    model_run_id = get_model_run_id()
    iterations = get_train_iterations()
    epochs = get_train_epochs()

    print('Start at {0}'.format(now))
    print('=' * 32)
    sys.stdout.flush()

    for iteration in range(iterations):
        print('Starting iteration #{0}'.format(iteration))
        sys.stdout.flush()

        X, Y = get_xy(iteration=iteration)

        with tf.device(get_device(action='train')):
            model.fit(
                X, Y,
                validation_set=get_validation_set_percentage(),
                n_epoch=epochs,
                show_metric=True,
                snapshot_epoch=False,
                run_id=model_run_id
            )

        print('Saving model ...')
        sys.stdout.flush()

        save_model(model)

        print('Model saved.')
        print('=' * 32)
        sys.stdout.flush()
