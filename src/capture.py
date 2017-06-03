import sys, os, time, datetime
import win32api
from PIL import ImageGrab
from helpers.keyboard_capture import get_pressed_keyboard_keys, check_for_capturing_hotkeys
from helpers.gamepad_capture import get_pressed_gamepad_buttons_and_axes

# Preparation
is_capturing = False # If we should be capturing
toggle_capturing_hotkeys = ['left_control', 'F11'] # view the full codes map inside helpers/keyboard_capture.py
inputs = None # Saves the current input on every tick
now = datetime.datetime.now()
session_id = now.strftime('%Y-%m-%d_%H%M%S')
screenshots_dir = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '..',
        'data'
    )
)
activity = len(sys.argv) > 1 and sys.argv[1] or 'general'

save_dir = os.path.join(screenshots_dir, activity, 'raw', session_id)
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Functions
def capture_screenshot(timestamp):
    filename = timestamp.replace(':', '') + '.png'
    filepath = os.path.join(save_dir, filename)

    # TODO: fix -- not working in the MINGW64 terminal
    im = ImageGrab.grab()
    im.save(filepath)
    
    return filepath

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

    time.sleep(0.25)
    now = datetime.datetime.now()
    timestamp = now.isoformat()

    if check_for_capturing_hotkeys(inputs['keyboard'], toggle_capturing_hotkeys):
        is_capturing = not is_capturing

    if is_capturing:
        screenshot = capture_screenshot(timestamp)
        data = {
            'timestamp': timestamp,
            'screenshot': screenshot,
            'inputs': inputs,
        }
        # TODO: save to log file

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
