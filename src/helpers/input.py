# https://stackoverflow.com/a/23468236
import ctypes
import time

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


# http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
DI_CODES = {
    'escape': 0x01,
    '1': 0x02,
    '2': 0x03,
    '3': 0x04,
    '4': 0x05,
    '5': 0x06,
    '6': 0x07,
    '7': 0x08,
    '8': 0x09,
    '9': 0x0A,
    '0': 0x0B,
    'minus': 0x0C,
    'equals': 0x0D,
    'back': 0x0E,
    'tab': 0x0F,
    'q': 0x10,
    'w': 0x11,
    'e': 0x12,
    'r': 0x13,
    't': 0x14,
    'y': 0x15,
    'u': 0x16,
    'i': 0x17,
    'o': 0x18,
    'p': 0x19,
    'lbracket': 0x1A,
    'rbracket': 0x1B,
    'return': 0x1C,
    'lcontrol': 0x1D,
    'a': 0x1E,
    's': 0x1F,
    'd': 0x20,
    'f': 0x21,
    'g': 0x22,
    'h': 0x23,
    'j': 0x24,
    'k': 0x25,
    'l': 0x26,
    'semicolon': 0x27,
    'apostrophe': 0x28,
    'grave': 0x29,
    'lshift': 0x2A,
    'backslash': 0x2B,
    'z': 0x2C,
    'x': 0x2D,
    'c': 0x2E,
    'v': 0x2F,
    'b': 0x30,
    'n': 0x31,
    'm': 0x32,
    'comma': 0x33,
    'period': 0x34,
    'slash': 0x35,
    'rshift': 0x36,
    'miltiply': 0x37,
    'lmenu': 0x38,
    'space': 0x39,
    'capital': 0x3A,
    'F1': 0x3B,
    'F2': 0x3C,
    'F3': 0x3D,
    'F4': 0x3E,
    'F5': 0x3F,
    'F6': 0x40,
    'F7': 0x41,
    'F8': 0x42,
    'F9': 0x43,
    'F10': 0x44,
    'numlock': 0x45,
    'scroll': 0x46,
    'numpad_7': 0x47,
    'numpad_8': 0x48,
    'numpad_9': 0x49,
    'substract': 0x4A,
    'numpad_4': 0x4B,
    'numpad_5': 0x4C,
    'numpad_6': 0x4D,
    'add': 0x4E,
    'numpad_1': 0x4F,
    'numpad_2': 0x50,
    'numpad_3': 0x51,
    'numpad_0': 0x52,
    'decimal': 0x53,
    'F11': 0x57,
    'F12': 0x58,
}


def press_keyboard_key(key):
    hexKeyCode = DI_CODES[key]

    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def release_keyboard_key(key):
    hexKeyCode = DI_CODES[key]

    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002,
                        0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
