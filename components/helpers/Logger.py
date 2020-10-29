import logging

logging.basicConfig(
    format='%(asctime)s: %(levelname)s: %(message)s',
    level=logging.INFO,
    datefmt='%H:%M:%S'
    )


class Logger():
    """
    Controls basic logging
    """

    INFO = logging.INFO
    WARN = logging.WARN
    ERROR = logging.ERROR

    @staticmethod
    def log_message(level, message):
        if level == 20: logging.info('%s', message)
        if level == 30: logging.warning('%s', message)
        if level == 40: logging.error('%s', message)
