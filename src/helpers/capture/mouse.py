import win32api

def get_mouse_position_and_buttons():
    return {
        'position': win32api.GetCursorPos(),
        'buttons': {
            'left': win32api.GetKeyState(0x01) < 0,
            'right': win32api.GetKeyState(0x02) < 0,
            'middle': win32api.GetKeyState(0x04) < 0,
        }
    }
