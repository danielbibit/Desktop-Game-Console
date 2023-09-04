import requests
import time
import json

class HomeAssistant():
    def __init__(self, api_key: str, server_url: str):
        self.api_key = api_key
        self.server_url = server_url
        self.last_light_state = None
        self.last_tv_state = None

    def call_home_assistant(self, method: str, endpoint: str, payload: dict|None) -> requests.Response:
        url = self.server_url + "/api/" + endpoint

        headers = {
            "Authorization": "Bearer " + self.api_key,
        }

        response = requests.request(method, url, headers=headers, json=payload)

        return response

    def turn_on_tv(self):
        print('Turning on TV')

        response = self.call_home_assistant('GET', 'states/media_player.tv_daniel', None)
        print(json.loads(response.text))

        tv_status = json.loads(response.text)['state']

        if tv_status == 'off':
            self.last_tv_state = 'off'

            self.call_home_assistant(
                'POST',
                'services/media_player/turn_on',
                {
                    "entity_id": "media_player.tv_daniel"
                }
            )

            time.sleep(15)
        else:
            self.last_tv_state = 'on'

            print('TV already on')

        response = self.call_home_assistant('GET', 'states/media_player.tv_daniel', None)
        current_source = json.loads(response.text)['attributes']['source']

        if current_source != 'PC':
            print('Switching output to PC')

            self.call_home_assistant(
                'POST',
                'services/media_player/select_source',
                {
                    "entity_id": "media_player.tv_daniel",
                    "source": "PC"
                }
            )

            time.sleep(10)
        else:
            print('Output already set to PC')

    def turn_off_tv(self):
        print('Turning off TV')

        self.call_home_assistant(
            'POST',
            'services/media_player/turn_off',
            {
                "entity_id": "media_player.tv_daniel"
            }
        )

    def restore_tv_state(self):
        if self.last_tv_state == 'off':
            print('TV was off before, restoring state')
            self.call_home_assistant(
                'POST',
                'services/media_player/turn_off',
                {
                    "entity_id": "media_player.tv_daniel"
                }
            )
        else:
            print('TV was on before, keeping state')

    def turn_off_monitor(self):
        self.call_home_assistant(
            'POST',
            'services/switch/turn_off',
            {
                "entity_id": "switch.tasmota_monitor"
            }
        )

    def turn_on_monitor(self):
        self.call_home_assistant(
            'POST',
            'services/switch/turn_on',
            {
                "entity_id": "switch.tasmota_monitor"
            }
        )

    def turn_on_light(self):
        response = self.call_home_assistant('GET', 'states/light.luz', None)
        self.last_light_state = json.loads(response.text)['state']
        print(self.last_light_state)

        self.call_home_assistant('POST', 'services/light/turn_on', {"entity_id": "light.luz"})

    def turn_off_light(self):
        response = self.call_home_assistant('GET', 'states/light.luz', None)
        self.last_light_state = json.loads(response.text)['state']
        print(self.last_light_state)

        self.call_home_assistant('POST', 'services/light/turn_off', {"entity_id": "light.luz"})

    def restore_light_state(self):
        # TODO prompt user to restore light state
        if self.last_light_state == 'on':
            self.turn_on_light()
