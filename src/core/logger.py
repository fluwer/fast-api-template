import logging
from logging.config import fileConfig

fileConfig("src/core/logging.conf", disable_existing_loggers=False)


class Logger:
    @staticmethod
    def get_logger(name: str = "root") -> logging.Logger:
        return logging.getLogger(name)


logger = Logger().get_logger("custom_logger")
