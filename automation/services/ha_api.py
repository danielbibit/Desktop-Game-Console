import requests

def call_home_assistant(self, method: str, endpoint: str, payload: dict|None) -> requests.Response:
    url = self.server_url + "/api/" + endpoint

    headers = {
        "Authorization": "Bearer " + self.api_key,
    }

    response = requests.request(method, url, headers=headers, json=payload)

    return response

def get_state(self):
    pass

def turn_on(self):
    pass

def turn_off(self):
    pass

def toggle(self):
    pass
