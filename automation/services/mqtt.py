import time
import paho.mqtt.client as mqtt
import threading
from automation.event_engine import EventEngine

class MqttService:
    def __init__(self, config, event_engine: EventEngine):
        self.config = config
        self.event_engine = event_engine

    def _on_connect(self, client, userdata, flags, rc):
        print("Mqtt connected with result code " + str(rc))
        client.subscribe("desktop_automation/command")

    def _on_disconnect(self, client, userdata, rc):
        print("Mqtt disconnected with result code " + str(rc))

    def _on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

        if msg.topic == "desktop_automation/command":
            self.event_engine.new_event(str(msg.payload.decode()))

    def worker(self):
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

        client.on_connect = self._on_connect
        client.on_message = self._on_message
        client.on_disconnect = self._on_disconnect

        client.username_pw_set(self.config['mqtt_username'], self.config['mqtt_password'])

        connected = False

        while not connected:
            try:
                client.connect(self.config['mqtt_broker'], 1883, 60)
                connected = True
            except Exception:
                print('Mqtt connection failed, retrying')
                time.sleep(5)

        client.loop_forever()

    def run(self):
        threading.Thread(target=self.worker, daemon=True).start()
