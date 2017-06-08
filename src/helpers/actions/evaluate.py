import sys
import os
import time
import tensorflow as tf
from custom import *
from helpers.common import *
from helpers.image import *


def evaluate():
    print('Loading model ...')
    sys.stdout.flush()

    with tf.device(get_device(action='evaluate')):
        model = get_model()

    last_time = time.time()
    controls_map = get_controls_map()

    print('Start at {0}'.format(now))
    print('=' * 32)
    sys.stdout.flush()

    while True:
        original_image = grab_image()
        X = process_image(original_image, return_array=True)

        with tf.device(get_device(action='evaluate')):
            prediction = get_prediction(model, X, controls_map)
            print('Prediction: {0}.'.format(prediction))
            sys.stdout.flush()

        print('Last execution took {0} seconds.'.format(
            time.time() - last_time))
        sys.stdout.flush()

        last_time = time.time()
