from helpers.inputs import get_gamepad

gamepad = {
    'buttons': {
        'north': False,
        'south': False,
        'east': False,
        'west': False,
        'start': False,
        'back': False,
        'mode': False,
        'left_bumper': False,
        'right_bumper': False,
        'left_trigger': 0,
        'right_trigger': 0,
    },
    'axes': {
        'left': {
            'x': 0,
            'y': 0,
        },
        'right': {
            'x': 0,
            'y': 0,
        },
        'd_pad': {
            'x': 0,
            'y': 0,
        },
    },
}

def get_pressed_gamepad_buttons_and_axes():
    try:
        events = get_gamepad(blocking=False)
        for event in events:
            code = event.code
            state = event.state

            if code == 'SYN_REPORT':
                continue
            
            print(code, state)
            
            if code == 'BTN_NORTH':
                gamepad['buttons']['north'] = state == 1
            elif code == 'BTN_SOUTH':
                gamepad['buttons']['south'] = state == 1
            elif code == 'BTN_EAST':
                gamepad['buttons']['east'] = state == 1
            elif code == 'BTN_WEST':
                gamepad['buttons']['west'] = state == 1
            elif code == 'BTN_SELECT':
                gamepad['buttons']['start'] = state == 1
            elif code == 'BTN_START':
                gamepad['buttons']['back'] = state == 1
            elif code == 'BTN_TL':
                gamepad['buttons']['left_bumper'] = state == 1
            elif code == 'BTN_TR':
                gamepad['buttons']['right_bumper'] = state == 1
            elif code == 'ABS_Z':
                gamepad['buttons']['left_trigger'] = state != 0 and (state / 255) or 0
            elif code == 'ABS_RZ':
                gamepad['buttons']['right_trigger'] = state != 0 and (state / 255) or 0
            elif code == 'ABS_X':
                gamepad['axes']['left']['x'] = state != 0 and (state / 32768) or 0
            elif code == 'ABS_Y':
                gamepad['axes']['left']['y'] = state != 0 and (state / 32768) or 0
            elif code == 'ABS_RX':
                gamepad['axes']['right']['x'] = state != 0 and (state / 32768) or 0
            elif code == 'ABS_RY':
                gamepad['axes']['right']['y'] = state != 0 and (state / 32768) or 0
            elif code == 'ABS_HAT0X':
                gamepad['axes']['d_pad']['x'] = state
            elif code == 'ABS_HAT0Y':
                gamepad['axes']['d_pad']['y'] = state

    except:
        pass

    return gamepad
