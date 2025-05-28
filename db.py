from config import Config

def get_db_config():
    try:
        config = Config.from_yaml('config.yaml')
        return {
            'hostname': config.db_hostname,
            'username': config.db_username,
            'password': config.db_password
        }
    except (FileNotFoundError, ValueError) as e:
        print(f"Error loading database configuration: {str(e)}")
        raise

def read_db(config:dict):
    pass

def write_db(config:dict):
    pass