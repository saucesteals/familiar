# https://stackoverflow.com/a/56944256
import logging

class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;21m"
    cyan = "\033[96m"
    green = "\x1b[1;32m"
    yellow = "\033[93m"
    red = "\033[91m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: cyan + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)