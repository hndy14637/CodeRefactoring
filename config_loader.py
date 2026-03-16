import os
from configparser import ConfigParser
from pathlib import Path

_config = None

def get_config():
    global _config
    if _config is None:
        _config = ConfigParser()
        _config.read(Path(__file__).parent / 'task_config.ini')
    return _config


def get_output_dir() -> Path:
    config = get_config()

    output_dir = Path(
        config.get(
            'settings',
            'output_dir',
            fallback=os.getenv('PROJECT_OUTPUT_DIR', 'output')
        )
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def get(section, key, fallback=None):
    return get_config().get(section, key, fallback=fallback)

def get_int(section, key, fallback=None):
    return get_config().getint(section, key, fallback=fallback)

def get_boolean(section, key, fallback=None):
    return get_config().getboolean(section, key, fallback=fallback)
