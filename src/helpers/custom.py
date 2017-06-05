import json
import numpy as np
import cv2
from PIL import Image
from helpers.common import *

'''
In this file we will specify all the custom methods, 
that can/will be different from game to game.
'''

# MUST return an array
# View the full list inside src/capture/keyboard.py
def get_toggle_capture_hotkeys():
    return ['left_control', 'F11']

# MUST return a np.array()
def preprocess_image(image):
    image_array = np.array(image)

    image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
    image_array = cv2.Canny(image_array, threshold1=50, threshold2=250)
    
    return image_array

# MUST return a dictionary
def get_image_processing_data_row(processed_image_path, inputs):
    return {
        'image_path': processed_image_path,
        'controls': get_controls_from_inputs(inputs),
    }

def get_controls_from_inputs(inputs):
    return {
        'forward': inputs['keyboard']['w'] or 
            inputs['gamepad']['axes']['right_trigger'] > 0,
        'backward': inputs['keyboard']['s'] or 
            inputs['gamepad']['axes']['left_trigger'] > 0,
        'left': inputs['keyboard']['a'] or 
            inputs['gamepad']['axes']['left']['x'] < 0,
        'right': inputs['keyboard']['d'] or 
            inputs['gamepad']['axes']['left']['x'] > 0,
    }

def convert_controls_to_array(controls):
    return [
        controls['forward'] and 1 or 0,
        controls['backward'] and 1 or 0,
        controls['left'] and 1 or 0,
        controls['right'] and 1 or 0,
    ]

def get_xy(activity, mode):
    X = []
    Y = []

    processed_dir = os.path.join(data_dir, activity, 'processed', mode)
    processed_data_file_path = os.path.join(processed_dir, 'data.txt')
    processed_data_file = open(processed_data_file_path, 'r+').read()
    processed_data = processed_data_file.split("\n")
    processed_data = [x for x in processed_data if x != ''] # TODO: find a quicker solution? filter()?

    for row in processed_data:
        row_data = json.loads(image_raw_data) # that returns the same results as defined in the get_image_processing_data_row()

        X.append(np.array(Image.open(row_data['image_path'])))
        Y.append(convert_controls_to_array(row_data['controls']))

    return X, Y
