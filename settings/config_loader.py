import yaml

class DotDict:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                setattr(self, key, DotDict(value))
            else:
                setattr(self, key, value)

def load_config():
    config_path = "C:\\Users\\calcolatore\\Desktop\\violence-detector\\settings\\config.yaml"
    try:
        with open(config_path, 'r') as file:
            config_dict = yaml.safe_load(file)
        return DotDict(config_dict)
    except yaml.YAMLError as exc:
        print(f"Error reading YAML file: {exc}")
        return None

config = load_config()