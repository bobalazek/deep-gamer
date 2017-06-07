import sys
import os
import time
import tensorflow as tf
from helpers.common import *
from helpers.custom import *
from helpers.image import *

# Main
if __name__ == "__main__":
    print('Loading model ...')
    sys.stdout.flush()

    model = get_model(load_existing=True)
    last_time = time.time()

    print('Start at {0}'.format(now))
    sys.stdout.flush()

    while True:
        original_image = grab_image()
        X = process_image(original_image, return_array=True)

        with tf.device(get_device(action='evaluate')):
            prediction = get_prediction(model, X)
            print('Prediction: {0}.'.format(prediction))
            sys.stdout.flush()

        print('Last execution took {0} seconds.'.format(
            time.time() - last_time))
        sys.stdout.flush()

        last_time = time.time()
