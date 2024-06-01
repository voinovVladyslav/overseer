from typing import override
import logging


class NoPyMongoInfoFilter(logging.Filter):
    @override
    def filter(self, record: logging.LogRecord) -> bool | logging.LogRecord:
        if 'pymongo' not in record.name:
            return True
        return record.levelno >= logging.WARNING
