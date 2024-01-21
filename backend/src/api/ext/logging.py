from fastapi import FastAPI
import logging
from typing import Union
from config import settings as s


def init_app(app: Union[FastAPI, None] = None):
    logger = logging.getLogger("CHICKIE_LOGGER")
    fmt = "%(asctime)s [%(levelname)s] %(message)s"
    datefmt = "[%d/%m/%Y] [%Hh%Mmin%Ss]"
    codes = {
        "CRITICAL": 50,
        "FATAL": 50,
        "ERROR": 40,
        "WARNING": 30,
        "WARN": 30,
        "INFO": 20,
        "DEBUG": 10,
        "NOTSET": 0,
        "OFF": 0,
    }

    codes_v2 = {
        50: "CRITICAL",
        40: "ERROR",
        30: "WARNING",
        20: "INFO",
        10: "DEBUG",
        0: "OFF",
    }
    try:
        log_level = codes.get(str(s.LOG_LEVEL)) or codes['INFO']
    except AttributeError:
        log_level = 10

    if log_level == 0:
        return None

    logging.basicConfig(format=fmt, datefmt=datefmt, level=log_level)
    logger.setLevel(log_level)

    logger.info(f"Logging inicializado em level {codes_v2[log_level]}")

    return logger
