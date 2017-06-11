import datetime
from helpers.common import *
from networks.gta5 import GTA5Network


if __name__ == "__main__":
    args = get_args()
    network = GTA5Network()

    if args['action'] == 'capture':
        network.capture()
    elif args['action'] == 'train':
        network.train()
    elif args['action'] == 'process':
        network.process()
    elif args['action'] == 'evaluate':
        network.evaluate()
