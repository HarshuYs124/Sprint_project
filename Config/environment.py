import os
import yaml

class ConfigReader:

    @staticmethod
    def read_config():
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "Config",
            "config.yaml"
        )
        with open(config_path, "r") as file:
            return yaml.safe_load(file)
