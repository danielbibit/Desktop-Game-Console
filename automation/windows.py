import subprocess
import time
import pyautogui
import automation.services.serial_keyboard as serial_keyboard
import automation.interfaces.os as os_interface

pyautogui.FAILSAFE = False
class Windows(os_interface.OSInterface):
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


    def process_launch(self, playnite_path: str):
        # Miminize all windows, solve focus issues
        pyautogui.hotkey('winleft', 'm')
        time.sleep(0.5)

        results = subprocess.Popen([playnite_path])

    def is_locked(self) -> bool:
        return self.process_exists('LogonUI.exe')

    def lock():
        pass

    def unlock(self, desktop_password: bytes, com_port: str):
        if self.is_locked():
            try:
                usb_keyboard = serial_keyboard.new_arduino_connection(com_port)

                # https://www.arduino.cc/reference/en/language/functions/usb/keyboard/keyboardmodifiers/
                with usb_keyboard:
                    # 27 ascii - escape
                    usb_keyboard.write(b'write:27\n')

                    usb_keyboard.write(b'print:' + desktop_password + b'\n')

                    # 10 ascii line feed
                    usb_keyboard.write(b'write:10\n')
            except:
                pass

    def switch_display(self, mode: str):
        print('switch_display ' + mode)
        if mode == 'external':
            subprocess.call('displayswitch.exe 4')

        elif mode == 'internal':
            subprocess.call('displayswitch.exe 1')

        elif mode == 'extend':
            subprocess.call('displayswitch.exe /extend')


    def move_mouse():
        pass

    def switch_audio():
        pass

    def move_mouse_out_screen(self):
        pyautogui.moveRel(8000, 8000)
