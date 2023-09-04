import os
import threading
import keyboard

import yaml
import time

import pystray
from PIL import Image
from automation.event_engine import EventEngine

import automation.services.windows.xinput as xinput
import automation.services.windows.audio as win_audio
import automation.windows as windows
from automation.home_assistant import HomeAssistant
from automation.xbox_controller import xboxController

def load_config():
    with open("config.yaml", "r") as stream:
        return yaml.safe_load(stream)


def tray_icon_click(icon, query):
    if str(query) == "Exit":
        icon.stop()
        os._exit(1)
    elif str(query) == "Launch":
        print('launching')


def action_callback(foo):
    print(foo)


def action_launch(system, ha, audio, config):
    system.unlock(bytes(config['desktop_password'].encode()), config['com_port'])

    ha.turn_on_tv()

    system.switch_display('external')

    system.process_launch(config['playnite_path'])

    ha.turn_off_light()

    audio.set_default_external()


def action_restore(system, ha, audio):
    system.switch_display('internal')

    audio.set_default_internal()

    time.sleep(5)

    ha.restore_tv_state()

    ha.restore_light_state()


if __name__ == '__main__':
    print('Starting script')

    config = load_config()

    ha = HomeAssistant(config['home_assistant_api_key'], config['home_assistant_url'])

    audio = win_audio.Audio(config)

    system = windows.Windows(config)

    event_engine = EventEngine()
    event_engine.run()

    controller_listner = xboxController(0, event_engine)
    controller_listner.run()

    # xboxHome + home(start)
    event_engine.add_subscriber('0x410', action_launch, system, ha, audio, config)

    # xboxHome + view(select)
    event_engine.add_subscriber('0x420', action_restore, system, ha, audio)

    # xboxHome + A
    event_engine.add_subscriber('0x1400', action_callback, 'debug')

    # xboxHome + B
    event_engine.add_subscriber('0x2400', keyboard.press_and_release, 'alt+f4')

    # xboxHome + X
    event_engine.add_subscriber('0x4400', keyboard.press_and_release, 'alt+tab')

    # xboxHome + Y
    event_engine.add_subscriber('0x8400', system.move_mouse_out_screen)

    # xboxHome + dpad up
    event_engine.add_subscriber('0x401', keyboard.press_and_release, 'volume up')

    # xboxHome + dpad down
    event_engine.add_subscriber('0x402', keyboard.press_and_release, 'volume down')

    # xboxHome + dpad left
    event_engine.add_subscriber('0x404', keyboard.press_and_release, 'ctrl+alt+f1')

    # xboxHome + dpad right
    event_engine.add_subscriber('0x408', keyboard.press_and_release, 'ctrl+alt+f1')

    image = Image.open("tray_icon.png")

    icon = pystray.Icon(
        "DGA",
        image,
        "Game Automation",
        menu=pystray.Menu(
            pystray.MenuItem("Launch", tray_icon_click),
            pystray.MenuItem("Exit", tray_icon_click)
        )
    )

    # Safe to call icon.run() on a thread when using Windows (per docs)
    thread_icon = threading.Thread(target=icon.run, daemon=True).start()

    while True:
        time.sleep(1)
