import datetime
from helpers.common import *
from networks.wasd import WASDNetwork


if __name__ == "__main__":
    args = get_args()
    network = WASDNetwork()

    if args['action'] == 'capture':
        network.capture()
    elif args['action'] == 'train':
        network.train()
    elif args['action'] == 'preprocess':
        network.preprocess()
    elif args['action'] == 'evaluate':
        network.evaluate()
