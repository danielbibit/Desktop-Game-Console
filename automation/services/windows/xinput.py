# This code is a strip down version of the XInput-Python package by Zuzu_Typ
# For the original code, https://github.com/Zuzu-Typ/XInput-Python

import ctypes, ctypes.util

from ctypes import Structure, POINTER


ERROR_SUCCESS               = 0
ERROR_BAD_ARGUMENTS         = 160
ERROR_DEVICE_NOT_CONNECTED  = 1167

# loading the DLL #
XINPUT_DLL_NAMES = (
    "XInput1_4.dll",
    "XInput9_1_0.dll",
    "XInput1_3.dll",
    "XInput1_2.dll",
    "XInput1_1.dll"
)

libXInput = None

for name in XINPUT_DLL_NAMES:
    found = ctypes.util.find_library(name)
    if found:
        libXInput = ctypes.WinDLL(found)
        break

if not libXInput:
    raise IOError("XInput library was not found.")
#/loading the DLL #

# defining static global variables #
WORD    = ctypes.c_ushort
BYTE    = ctypes.c_ubyte
SHORT   = ctypes.c_short
DWORD   = ctypes.c_ulong
#/defining static global variables #

# defining XInput compatible structures #
class XINPUT_GAMEPAD(Structure):
    _fields_ = [("wButtons", WORD),
                ("bLeftTrigger", BYTE),
                ("bRightTrigger", BYTE),
                ("sThumbLX", SHORT),
                ("sThumbLY", SHORT),
                ("sThumbRX", SHORT),
                ("sThumbRY", SHORT),
                ]

class XINPUT_STATE(Structure):
    _fields_ = [("dwPacketNumber", DWORD),
                ("Gamepad", XINPUT_GAMEPAD),
                ]


libXInput.XInputGetState.argtypes = [DWORD, POINTER(XINPUT_STATE)]
libXInput.XInputGetState.restype = DWORD

def XInputGetState(dwUserIndex, state):
    return libXInput[100](dwUserIndex, ctypes.byref(state))
#/defining XInput compatible structures #


# defining custom classes and methods #
class XInputNotConnectedError(Exception):
    pass

class XInputBadArgumentError(ValueError):
    pass

def get_state(user_index):
    """get_state(int) -> XINPUT_STATE
Returns the raw state of the controller."""
    state = XINPUT_STATE()
    res = XInputGetState(user_index, state)
    if res == ERROR_DEVICE_NOT_CONNECTED:
        raise XInputNotConnectedError("Controller [{}] appears to be disconnected.".format(user_index))

    if res == ERROR_BAD_ARGUMENTS:
        raise XInputBadArgumentError("Controller [{}] doesn't exist. IDs range from 0 to 3.".format(user_index))

    assert res == 0, "Couldn't get the state of controller [{}]. Is it disconnected?".format(user_index)

    return state
