# Deep Gamer

## Requirements
* Windows OS
* Python 3.5+
* See requirements.txt

## Installation
* Install the python requirements: `pip3 install -r requirements.txt`

## Development
Every custom stuff you may want / will need to change is inside the `src/custom.py` file.

## Workflow

> **Note**: For now, you can leave `--activity="{ACTIVITY}" --mode="{MODE}"` out, as the default value for `--activity` is `general` and for `--mode` it's `default`. The reason for `{ACTIVITY}` is, that you can capture different activities in your game, such as `driving, walking, running, ...`. The `mode` on the other hand, is ONLY relevant for processing, training & capturing. For example with activity, you'll always have the same raw data, if you select a `mode`, then you can process, train & capture different modes, like: try different images sizes (`large_sizes_input`, `small_sizes_input`, ...), different color manipulations (`black_and_white`, `lower_brightness`, `higher_contrast`, ...), ... and then later you can compare which model works best, without having to replace your existing model(-s).

### Capture
First you will need to capture all the footage on which you want your "AI" to learn on. You'll do that with `python src/deep_gamer.py capture`. This will capture your (primary) screen and save all the screenshots into `data/{ACTIVITY}/raw/{TIMESTAMP}`

### Process
After that we need to process all the gathered data. For that, just run `python src/deep_gamer.py process`

### Train
Now that we have all our data prepared, we will need to train the model. We do that with `python src/deep_gamer.py train` (you can add the `--force-new-model`, if you don't want to continue to train your existing model). This may take a couple of hours/days.
To view the training, start a separate terminal and run `python -m tensorflow.tensorboard --logdir=data/{ACTIVITY}/network/{MODE}/logs` (ex. `python -m tensorflow.tensorboard --logdir=data/general/network/default/logs`). Now you can go to http://localhost:6006

### Evaluate
Now we are finally ready to evaluate the model. We can do that with `python src/deep_gamer.py evaluate`.

## Author
Borut Balazek <bobalazek124@gmail.com> (http://bobalazek.com)

## License
Deep Gamer is licensed under the MIT license.
