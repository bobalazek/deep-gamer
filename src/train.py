import sys, datetime
import tensorflow as tf
from helpers.common import *
from helpers.custom import *

# Preparation
now = datetime.datetime.now()

# Main 
if __name__ == "__main__":
    print('Loading model ...')
    sys.stdout.flush()

    with tf.device(get_device('train')):
        model = get_model()

    model_run_id = get_model_run_id()
    epochs = get_epochs()

    print('Start at {0}'.format(now))
    sys.stdout.flush()

    for i in range(epochs):
        print('Starting epoch {0}'.format(i))
        sys.stdout.flush()

        X, Y = get_xy()

        model.fit(
            X, Y,
            validation_set=get_validation_set_percentage(),
            n_epoch=1,
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
