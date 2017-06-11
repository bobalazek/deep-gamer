# https://github.com/tflearn/tflearn/blob/master/examples/images/alexnet.py

""" AlexNet.

References:
    - Alex Krizhevsky, Ilya Sutskever & Geoffrey E. Hinton. ImageNet
    Classification with Deep Convolutional Neural Networks. NIPS, 2012.

Links:
    - [AlexNet Paper](http://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks.pdf)

"""

from __future__ import division, print_function, absolute_import

import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.estimator import regression


def alexnet(
        input1_size,  # height
        input2_size,  # width
        output_size,
        tensorboard_dir='/tmp/tflearn_logs',
        checkpoint_path=None,
        best_checkpoint_path=None,
        learning_rate=0.001,
        best_val_accuracy=0.0,
        max_checkpoints=None,
        tensorboard_verbose=3):

    network = input_data(shape=[None, input1_size, input2_size, 3])

    network = conv_2d(network, 96, 11, strides=4, activation='relu')
    network = max_pool_2d(network, 3, strides=2)
    network = local_response_normalization(network)
    network = conv_2d(network, 256, 5, activation='relu')
    network = max_pool_2d(network, 3, strides=2)
    network = local_response_normalization(network)
    network = conv_2d(network, 384, 3, activation='relu')
    network = conv_2d(network, 384, 3, activation='relu')
    network = conv_2d(network, 256, 3, activation='relu')
    network = max_pool_2d(network, 3, strides=2)
    network = local_response_normalization(network)
    network = fully_connected(network, 4096, activation='tanh')
    network = dropout(network, 0.5)
    network = fully_connected(network, 4096, activation='tanh')
    network = dropout(network, 0.5)
    network = fully_connected(network, output_size, activation='softmax')
    network = regression(network, optimizer='momentum',
                         loss='categorical_crossentropy',
                         learning_rate=learning_rate)

    model = tflearn.DNN(network, checkpoint_path=checkpoint_path,
                        best_checkpoint_path=best_checkpoint_path,
                        best_val_accuracy=best_val_accuracy,
                        max_checkpoints=max_checkpoints,
                        tensorboard_verbose=tensorboard_verbose,
                        tensorboard_dir=tensorboard_dir)

    return model
