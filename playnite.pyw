import time

from automation.event_engine import EventEngine

import automation.services.windows.audio as win_audio
import automation.services.mqtt as mqtt
import automation.windows as windows

from automation.xbox_controller import xboxController
from automation.config import config
from automation.system_tray import WxApp


def action_restore(system, audio):
    system.switch_display('internal')

    audio.set_default_internal()

    time.sleep(3)

    system.lock()


if __name__ == '__main__':
    print('Starting script')

    audio = win_audio.Audio(config)

    system = windows.Windows(config)

    event_engine = EventEngine()
    event_engine.run()

    controller_listner = xboxController(0, event_engine)
    controller_listner.run()

    mqtt_service = mqtt.MqttService(config, event_engine)
    mqtt_service.run()

    # # xboxHome + view(select)
    # L3 + view(select)
    event_engine.add_subscriber('0x60', action_restore, system, audio)

    event_engine.add_subscriber('MQTT_UNLOCK', system.unlock, bytes(config['desktop_password'].encode()), config['com_port'])

    event_engine.add_subscriber('MQTT_DISPLAY_EXTERNAL', system.switch_display, 'external')

    event_engine.add_subscriber('MQTT_LAUNCH', system.launch_steam_big_picture)

    event_engine.add_subscriber('MQTT_DISPLAY_INTERNAL', system.switch_display, 'internal')


    # Safe to call icon.run() on a thread when using Windows (per docs)
    # thread_icon = threading.Thread(target=icon.run, daemon=True).start()
    app = WxApp(event_engine=event_engine)
    app.MainLoop()
