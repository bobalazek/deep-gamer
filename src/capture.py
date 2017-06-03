import os, time, datetime
import win32api
from PIL import ImageGrab
from helpers.keyboard_capture import get_pressed_keyboard_keys
from helpers.gamepad_capture import get_pressed_gamepad_buttons_and_axes

# Preparation
now = datetime.datetime.now()
session_id = '{0}-{1}-{2}_evening'.format(now.year, now.month, now.day)
screenshots_dir = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '..',
        'data'
    )
)
activity = 'driving'

# Functions
def capture_screenshot(timestamp):
    save_dir = os.path.join(screenshots_dir, activity, 'raw', session_id)
    
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    filename = timestamp.replace(':', '') + '.png'
    filepath = os.path.join(save_dir, filename)

    im = ImageGrab.grab()
    im.save(filepath)
    
    return True

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
    now = datetime.datetime.now()
    timestamp = now.isoformat()
    screenshot = capture_screenshot(timestamp)
    inputs = capture_inputs()
    
    #print(inputs)
    
    return True

if __name__ == "__main__":
    last_time = time.time()
    while True:
        do_capturing()
        print('Last execution took {0} seconds.'.format(time.time() - last_time))
        last_time = time.time()
