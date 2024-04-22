import subprocess
import time
import pyautogui
import ctypes
import pywintypes
import win32api
import win32con
import automation.services.serial_keyboard as serial_keyboard

pyautogui.FAILSAFE = False
class Windows():
    def __init__(self, config):
        pass

    def process_exists(self, process_name: str) -> bool:
        call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
        # use buildin check_output right away
        output = subprocess.check_output(call).decode()
        # check in last line for process name
        last_line = output.strip().split('\r\n')[-1]
        # because Fail message could be translated
        return last_line.lower().startswith(process_name.lower())

    def is_locked(self) -> bool:
        # This will not work if another user is logged in
        # Windows will spawn another instance of LogonUI.exe
        return self.process_exists('LogonUI.exe')

    def lock(self):
        subprocess.call('rundll32.exe user32.dll,LockWorkStation')
        time.sleep(0.5)

    def unlock(self, desktop_password: bytes, com_port: str):
        if self.is_locked():
            print('Pc is locked, unlocking with keyboard')

            # Make sure to not write password somewhere else if another user is logged in
            pyautogui.hotkey('winleft', 'm')
            time.sleep(0.5)

            try:
                usb_keyboard = serial_keyboard.new_arduino_connection(com_port)

                # https://www.arduino.cc/reference/en/language/functions/usb/keyboard/keyboardmodifiers/
                with usb_keyboard:
                    # 8 ascii - backspace
                    usb_keyboard.write(b'write:8\n')

                    # # 27 ascii - escape
                    # usb_keyboard.write(b'write:27\n')

                    time.sleep(0.5)

                    # usb_keyboard.write(b'print:' + desktop_password + b'\n')
                    for char in desktop_password:
                        usb_keyboard.write(b'write:' + str(char).encode() + b'\n')

                    # 10 ascii line feed
                    usb_keyboard.write(b'write:10\n')
            except Exception as e:
                print('Error while writing to keyboard')
                print(e)

    def switch_display(self, mode: str):
        print('switch_display ' + mode)

        if mode == 'external':
            subprocess.call('displayswitch.exe 4')

        elif mode == 'internal':
            subprocess.call('displayswitch.exe 1')

        elif mode == 'extend':
            subprocess.call('displayswitch.exe /extend')

    def launch_steam_big_picture(self):
        pyautogui.hotkey('winleft', 'm')
        time.sleep(0.5)
        pyautogui.hotkey('winleft', 'r')
        time.sleep(1)
        pyautogui.write('steam://open/gamepadui')
        time.sleep(1)
        pyautogui.press('enter')

    def get_current_resolution(self):
        user32 = ctypes.windll.user32

        return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    def set_display_resolution(self, width: int, height: int):
        devmode = pywintypes.DEVMODEType()

        devmode.PelsWidth = width
        devmode.PelsHeight = height

        # Set the display resolution as defautl
        flags = win32con.CDS_UPDATEREGISTRY

        devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT

        win32api.ChangeDisplaySettings(devmode, flags)
