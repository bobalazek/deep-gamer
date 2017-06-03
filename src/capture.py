import sys, os, time, datetime, json
import win32api
from helpers.common import *
from helpers.keyboard_capture import get_pressed_keyboard_keys, check_for_capturing_hotkeys
from helpers.gamepad_capture import get_pressed_gamepad_buttons_and_axes

# Preparation
is_capturing = False # If we should be capturing
toggle_capturing_hotkeys = ['left_control', 'F11'] # view the full codes map inside helpers/keyboard_capture.py
inputs = None # Saves the current input on every tick
now = datetime.datetime.now()
session_id = now.strftime('%Y-%m-%d_%H%M%S')
data_dir = get_data_dir()
activity = len(sys.argv) > 1 and sys.argv[1] or 'general'
session_dir = os.path.join(data_dir, activity, 'raw', session_id)
if not os.path.exists(session_dir):
    os.makedirs(session_dir)

# Functions
def capture_image(timestamp):
    filename = timestamp.replace(':', '') + '.png'
    filepath = os.path.join(session_dir, filename)

    grab_image(filepath)
    
    return filename, filepath

def capture_inputs():    
    return {
        'keyboard': get_keyboard_inputs(),
        'mouse': get_mouse_inputs(),
        'gamepad': get_gamepad_inputs(),
    }

def get_mouse_inputs():
    return {
        'position': win32api.GetCursorPos(),
        'buttons': {
            'left': win32api.GetKeyState(0x01) < 0,
            'right': win32api.GetKeyState(0x02) < 0,
            'middle': win32api.GetKeyState(0x04) < 0,
        }
    }

def get_keyboard_inputs():
    return get_pressed_keyboard_keys()


def get_gamepad_inputs():
    return get_pressed_gamepad_buttons_and_axes()

def do_capturing():
    global inputs, is_capturing

    now = datetime.datetime.now()
    timestamp = now.isoformat()

    if check_for_capturing_hotkeys(inputs['keyboard'], toggle_capturing_hotkeys):
        is_capturing = not is_capturing

    if is_capturing:
        image_name, image_path = capture_image(timestamp)
        data = {
            'timestamp': timestamp,
            'image': {
                'name': image_name,
                'path': image_path,
            },
            'inputs': inputs,
        }
        with open(os.path.join(session_dir, 'log.txt'), 'a') as log_file:
            log_file.write(json.dumps(data) + "\n")

    return is_capturing

# Main
if __name__ == "__main__":
    last_time = time.time()
    
    print('Start at {0}'.format(now))
    
    while True:
        inputs = capture_inputs()

        if do_capturing():
            print('Last execution took {0} seconds.'.format(time.time() - last_time))
        
        last_time = time.time()
