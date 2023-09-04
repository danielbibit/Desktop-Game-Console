# RUN THIS FILE FROM THE ROOT
import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import automation.xinput as xinput

from time import sleep

while True:
    input = ''
    sleep(0.1)

    try:
        input = hex(xinput.get_state(0).Gamepad.wButtons)
        print(input)
    except:
        print('no controller found')
