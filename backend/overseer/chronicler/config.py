import json
import logging
import logging.config
from pathlib import Path


def setup_logging():
    config_path = Path(__file__).parent / 'logging_config' / 'config.json'
    with open(config_path) as f:
        config = json.load(f)
    logging.config.dictConfig(config)

