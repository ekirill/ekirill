import psutil
import logging
import sys


def file_is_free(fpath):
    # if any process has file handle opened for this file, than it is not free
    for proc in psutil.process_iter():
        try:
            for item in proc.open_files():
                if fpath == item.path:
                    return False
        except Exception:
            pass

    return True


def get_logger(name, prefix):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(prefix + ': %(asctime)s\t%(levelname)s\t%(message)s')
    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger
