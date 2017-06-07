import sys
import os
import time
import datetime
import json
from helpers.common import *
from helpers.custom import *
from helpers.capture.keyboard import get_pressed_keyboard_keys, check_for_capturing_hotkeys
from helpers.capture.gamepad import get_pressed_gamepad_buttons_and_axes
from helpers.capture.mouse import get_mouse_position_and_buttons

# Preparation
is_capturing = False  # If we should be capturing
inputs = None  # Saves the current input on every tick
toggle_capture_hotkeys = get_toggle_capture_hotkeys()
now = datetime.datetime.now()
data_dir = get_data_dir()
args = get_args()

session_id = now.strftime('%Y-%m-%d_%H%M%S')
session_dir = os.path.join(data_dir, args['activity'], 'raw', session_id)

# Functions


def prepare_folders_and_files():
    if not os.path.exists(session_dir):
        os.makedirs(session_dir)


def capture_image(timestamp):
    filename = timestamp.replace(':', '') + '.jpg'
    filepath = os.path.join(session_dir, filename)

    # TODO: batch image save?
    grab_image(file_path=filepath, file_format='JPEG')

    return filename, filepath


def capture_inputs():
    return {
        'keyboard': get_pressed_keyboard_keys(),
        'mouse': get_mouse_position_and_buttons(),
        'gamepad': get_pressed_gamepad_buttons_and_axes(),
    }


def capture():
    global inputs, is_capturing

    now = datetime.datetime.now()
    timestamp = now.isoformat()

    if check_for_capturing_hotkeys(inputs['keyboard'], toggle_capture_hotkeys):
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

    # Prepare folders and files
    prepare_folders_and_files()

    print('Start at {0}'.format(now))
    sys.stdout.flush()

    while True:
        inputs = capture_inputs()

        if capture():
            print('Last execution took {0} seconds.'.format(
                time.time() - last_time))
            print('Controls: {0}'.format(get_controls_from_inputs(inputs)))
            sys.stdout.flush()

        last_time = time.time()
