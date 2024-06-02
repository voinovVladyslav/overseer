from typing import override
import logging
from pydantic import BaseModel


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
