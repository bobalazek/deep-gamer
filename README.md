# GTA5 Deep Driving

## Installation
* Install the python requirements: `pip3 install -r requirements.txt`

## Workflow
* First you will need to capture all the footage on which you want your "AI" to learn on. You'll do that with `python src/capture.py {ACTIVITY}` (the {ACTIVITY} can be any value, such as: driving, walking, shooting, ...). This will capture your (primary) screen and save all the screenshots into `data/{ACTIVITY}/raw/{TIMESTAMP}`
* After that we need to process all the gathered data. For that, just run `python src/process.py {ACTIVITY} {PROCESSING_TYPE}` (for now, you can leave {PROCESSING_TYPE} out; it is rather for debugging purposes to see, which processing type will give the best results)
