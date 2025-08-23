import os
import yaml

def get_config():
    config_path = "config.yaml"
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return yaml.load(f, Loader=yaml.FullLoader)
    return None

CONFIG = get_config()