import datetime
from helpers.common import *
from helpers.actions.capture import capture
from helpers.actions.train import train
from helpers.actions.process import process
from helpers.actions.evaluate import evaluate

now = datetime.datetime.now()
args = get_args()

if __name__ == "__main__":
    if args['action'] == 'capture':
        capture()
    elif args['action'] == 'train':
        train()
    elif args['action'] == 'process':
        process()
    elif args['action'] == 'evaluate':
        evaluate()
