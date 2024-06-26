import threading
import time
import automation.services.windows.xinput as xinput


class xboxController():
    def __init__(self, controller_number, event_engine):
        self.controller_number = controller_number
        self.event_engine = event_engine

    def worker(self):
        last_input = None

        while True:
            time.sleep(0.05)

            try:
                current_input = hex(xinput.get_state(self.controller_number).Gamepad.wButtons)

                if last_input != current_input:
                    self.event_engine.new_event(current_input)

                last_input = current_input

            except Exception:
                pass

    def run(self):
        threading.Thread(target=self.worker, daemon=True).start()


