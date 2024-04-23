import os
import yaml

def load_config():
    script_path = os.path.dirname(__file__)

    with open(os.path.join(script_path, "..\config.yaml"), "r") as stream:
        loaded = yaml.safe_load(stream)

        return loaded

config = load_config()
