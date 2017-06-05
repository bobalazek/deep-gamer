import datetime
import tensorflow as tf
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

    for i in range(epochs):
        print('Starting epoch {0}'.format(i))

        X, Y = get_xy()
        count = len(X)
        validation_set_count = int(count * 0.10)
        train_x = X[:-validation_set_count]
        train_y = Y[:-validation_set_count]
        test_x = Y[-validation_set_count:]
        test_y = Y[-validation_set_count:]

        model.fit(
            train_x,
            train_y,
            validation_set=(test_x, test_y),
            n_epoch=1,
            show_metric=True,
            snapshot_epoch=False,
            run_id=model_run_id
        )
        
        if i % 8 == 0:
            print('Saving model ...')
            save_model(model)
