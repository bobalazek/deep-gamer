import datetime
from helpers.common import *
from helpers.custom import *

# Preparation
now = datetime.datetime.now()

# Main
if __name__ == "__main__":
    model = get_model()
    model_run_id = get_model_run_id()
    epochs = get_epochs()
    
    print('Start at {0}'.format(now))

    for i in xrange(epochs):
        print('Starting epoch {0}'.format(i))
        
        X, Y = get_xy()
        train_x = X[:-100]
        train_Y = Y[:-100]
        test_x = Y[-100:]
        test_Y = Y[-100:]
        
        model.fit(
            train_x,
            train_y,
            validation_set=(test_x, test_y),
            n_epoch=1,
            show_metric=True,
            snapshot_epoch=False,
            run_id=model_run_id
        )
