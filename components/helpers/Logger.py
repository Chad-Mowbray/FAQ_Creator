import logging

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO,)


class Logger():

    INFO = logging.INFO
    WARN = logging.WARN
    ERROR = logging.ERROR

    @staticmethod
    def log_message(level, message):
        if level == 20: logging.info('%s', message)
        if level == 30: logging.warning('%s', message)
        if level == 40: logging.error('%s', message)
