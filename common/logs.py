# -*- coding: utf-8 -*-
import logging
import os
import time


def _path(relative_path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), relative_path))


LOG_DIR = _path("../log")
os.makedirs(LOG_DIR, exist_ok=True)


class log:
    """Small compatibility wrapper around a shared project logger."""

    _logger = None

    def __init__(self):
        if log._logger is None:
            log._logger = self._build_logger()
        self.logger = log._logger

    @staticmethod
    def _build_logger():
        filename = "Appium-" + time.strftime("%Y%m%d") + ".txt"
        log_file = os.path.join(LOG_DIR, filename)

        logger = logging.getLogger("appium_ui_auto")
        logger.setLevel(logging.DEBUG)
        logger.propagate = False

        if logger.handlers:
            return logger

        formatter = logging.Formatter("[%(asctime)s] - [%(levelname)s] - %(message)s")

        file_handler = logging.FileHandler(log_file, "a", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        return logger

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warn(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)
