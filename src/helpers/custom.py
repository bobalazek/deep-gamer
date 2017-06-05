import numpy as np
import cv2

'''
In this file we will specify all the custom methods, 
that can/will be different from game to game.
'''

# MUST return an array
# View the full list inside src/capture/keyboard.py
def get_toggle_capture_hotkeys():
    return ['left_control', 'F11']

# MUST return a np.array()
def custom_preprocess_image(image):
    image_array = np.array(image)

    image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
    image_array = cv2.Canny(image_array, threshold1=50, threshold2=250)
    
    return image_array

# MUST return a dictionary
def get_image_processing_data_row(processed_image_path, image_data):
    return {
        'image_path': processed_image_path,
        'controls': {
            'forward': image_data['inputs']['keyboard']['w'] or 
                image_data['inputs']['gamepad']['axes']['right_trigger'] > 0,
            'backward': image_data['inputs']['keyboard']['s'] or 
                image_data['inputs']['gamepad']['axes']['left_trigger'] > 0,
            'left': image_data['inputs']['keyboard']['a'] or 
                image_data['inputs']['gamepad']['axes']['left']['x'] < 0,
            'right': image_data['inputs']['keyboard']['d'] or 
                image_data['inputs']['gamepad']['axes']['left']['x'] > 0,
        },
    }
