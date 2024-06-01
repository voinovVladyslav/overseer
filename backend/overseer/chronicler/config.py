import json
import logging
import logging.config
from pathlib import Path


def get_logging_config() -> dict:
    config_path = Path(__file__).parent / 'logging_config' / 'config.json'
    with open(config_path) as f:
        config = json.load(f)
    return config


def setup_logging():
    logging.config.dictConfig(get_logging_config())
