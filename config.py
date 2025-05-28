import yaml
from typing import Dict, Any

class Config:
    def __init__(self):
        self.db_hostname = None
        self.db_username = None
        self.db_password = None

    @classmethod
    def from_yaml(cls, path: str) -> 'Config':
        try:
            with open(path, 'r') as file:
                config = yaml.safe_load(file)
                if not config or 'db' not in config:
                    raise ValueError("Invalid config file: missing 'db' section")
                
                instance = cls()
                db_config = config['db']
                instance.db_hostname = db_config.get('hostname')
                instance.db_username = db_config.get('username')
                instance.db_password = db_config.get('password')
                
                if not all([instance.db_hostname, instance.db_username, instance.db_password]):
                    raise ValueError("Missing required database configuration values")
                
                return instance
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML file: {str(e)}")
        