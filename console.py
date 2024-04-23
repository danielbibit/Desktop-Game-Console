import argparse
import time
import pyautogui
import automation.windows as windows
from automation.config import config

def sunshine_do(system, resolution):
    system.unlock(bytes(config['desktop_password'].encode()), config['com_port'])

    time.sleep(1)

    system.switch_display('external')

    time.sleep(1)

    if resolution[0] == 1280 and resolution[1] == 800:
        system.set_display_resolution(1680, 1050)
    elif resolution[0] == 1920 and resolution[1] == 1080:
        system.set_display_resolution(1920, 1080)

    time.sleep(2)

    pyautogui.hotkey('winleft', 'm')

    time.sleep(1)

    # Sunshine launch steam


def sunshine_undo(system):
    # Sunshine close steam

    system.set_display_resolution(3840, 2160)

    time.sleep(1)

    system.switch_display('internal')

    time.sleep(1)

    system.lock()


if __name__ == '__main__':
    print('Starting script')

    parser = argparse.ArgumentParser()
    system = windows.Windows(config)

    parser.add_argument('-r', '--resolution', nargs=2, type=int, help='Set resolution')
    parser.add_argument('-c', '--command', nargs=1, type=str, help='Sunshine mode')

    args = vars(parser.parse_args())
    print(args)

    command = args['command'][0]

    if command == 'sunshine_do':
        sunshine_do(system, args['resolution'])
    elif command == 'sunshine_undo':
        sunshine_undo(system)

