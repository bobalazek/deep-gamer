# Deep Gamer

## Requirements
* Python 3.5+
* See requirements.txt

## Installation
* Install the python requirements: `pip3 install -r requirements.txt`

## Workflow
* First you will need to capture all the footage on which you want your "AI" to learn on. You'll do that with `python src/capture.py --activity="{ACTIVITY}""` (the {ACTIVITY} can be any value, such as: driving, walking, shooting, ...). This will capture your (primary) screen and save all the screenshots into `data/{ACTIVITY}/raw/{TIMESTAMP}`
* After that we need to process all the gathered data. For that, just run `python src/process.py --activity="{ACTIVITY}" --mode="{MODE}"` (for now, you can leave {MODE} out; it is rather for debugging purposes to see, which processing type will give the best results)
* Now that we have all our data prepared, we will need to train the model. We do that with `python src/train.py --activity="{ACTIVITY}" --mode="{MODE}" --load-existing` (in case you want to select a special mode). This may take a couple of hours/days. To view the training, start a separate terminal and run `python -m tensorflow.tensorboard --logdir=data/{ACTIVITY}/network/{MODE}/logs` (ex. `python -m tensorflow.tensorboard --logdir=data/general/network/default/logs`). Now you can go to http://localhost:6006
* Now we are finally ready to evaluate the model. We can do that with `python src/evaluate.py --activity="{ACTIVITY}" --mode="{MODE}"`

## Author
Borut Balazek <bobalazek124@gmail.com> (http://bobalazek.com)

## License
Proprietary - All rights reserved - Borut Balazek <bobalazek124@gmail.com>
