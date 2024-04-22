import time
import sys
import os
import yaml

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import automation.windows as windows


def load_config():
    with open("C:\Daniel\Code\desktop_gaming_automation\config.yaml", "r") as stream:
        return yaml.safe_load(stream)

if __name__ == '__main__':
    config = load_config()

    system = windows.Windows(config)

    system.set_display_resolution(3840, 2160)

    time.sleep(1)

    system.switch_display('internal')

    time.sleep(1)

    system.lock()
