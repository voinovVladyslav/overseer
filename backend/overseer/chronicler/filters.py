from typing import override
import logging

from pydantic import BaseModel


class Colors:
    LIGHT_BLUE = "\033[38;5;39m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    LIGHT_YELLOW = "\033[93m"
    RED = "\033[31m"
    ORANGE = "\033[38;5;208m"
    RESET = "\033[0m"


class FilterConfig(BaseModel):
    keywords: list[str]
    level: str

    @property
    def level_number(self) -> int:
        return logging.getLevelName(self.level.upper())


class KeywordLevelFilter(logging.Filter):
    def __init__(self, filters: list[dict[str, str | list[str]]]) -> None:
        self.filters = [FilterConfig(**f) for f in filters]
        super().__init__()

    @override
    def filter(self, record: logging.LogRecord) -> bool | logging.LogRecord:
        for filter in self.filters:
            for keyword in filter.keywords:
                if record.name.startswith(keyword):
                    return record.levelno >= filter.level_number
        return True


class ColorFilter(logging.Filter):
    @override
    def filter(self, record: logging.LogRecord) -> bool | logging.LogRecord:
        if record.levelno >= logging.CRITICAL:
            record.levelname = f"{Colors.ORANGE}{record.levelname}{Colors.RESET}"  # noqa

        elif record.levelno >= logging.ERROR:
            record.levelname = f"{Colors.RED}{record.levelname}{Colors.RESET}"

        elif record.levelno >= logging.WARNING:
            record.levelname = f"{Colors.YELLOW}{record.levelname}{Colors.RESET}"  # noqa

        elif record.levelno >= logging.INFO:
            record.levelname = f"{Colors.GREEN}{record.levelname}{Colors.RESET}"

        elif record.levelno >= logging.DEBUG:
            record.levelname = f"{Colors.LIGHT_BLUE}{record.levelname}{Colors.RESET}"  # noqa

        record.name = f"{Colors.LIGHT_YELLOW}{record.module}{Colors.RESET}"
        return record
