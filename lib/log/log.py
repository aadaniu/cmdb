# -*- coding: utf-8 -*-
# 2017-11-29
# by why

import os
import sys
import time
import logging

# log dir

os.chdir(sys.path[0])
log_dir = os.path.dirname(__file__) + "/../../logs/"

# log level

try:
    log_level = {"info": logging.INFO,
                 "error": logging.ERROR,
                 "debug": logging.DEBUG}[os.environ['tagLogLevel']]
except OSError as e:
    log_level = logging.DEBUG

# log name

logger_name_list = [
    'info',
    'error',
    'debug',
    'slow_log',
]

# slow log
SLOW_LOG = logging.getLogger("slow")
SLOW_TIME = 500  # ms

# log format

LoggerFormatStr = "[%(asctime)s|%(name)s/%(filename)s:%(lineno)d] - %(message)s"

for logger_name in logger_name_list:
    log_filename = log_dir + logger_name + ".log"
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)
    if not os.path.isfile(log_filename):
        fobj = open(log_filename, 'w')
        fobj.close()
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    handler = logging.handlers.RotatingFileHandler(log_filename, maxBytes=20480000, backupCount=3)
    formatter_general = logging.Formatter(LoggerFormatStr)
    handler.setFormatter(formatter_general)

    logger.addHandler(handler)


class CcLogger(object):
    def __init__(self):
        self.info_log = logging.getLogger("info")
        self.error_log = logging.getLogger("error")
        self.debug_log = logging.getLogger("debug")

    def set_uuid(self, uuid=""):
        for name in ["info", "error", "debug"]:
            log_file_name = log_dir + name + ".log"
            _logger = logging.getLogger(name)
            _LoggerFormatStr = "[%(asctime)s|%(levelname)s|" + str(uuid) + "] - %(message)s"
            _handler = logging.handlers.RotatingFileHandler(log_file_name, maxBytes=20480000, backupCount=3)
            _formatter_general = logging.Formatter(_LoggerFormatStr)
            _handler.setFormatter(_formatter_general)
            _logger.handlers = []
            _logger.setLevel(log_level)
            _logger.addHandler(_handler)

    def debug(self, msg):
        self.debug_log.debug(msg)

    def info(self, msg):
        self.info_log.info(msg)
        self.debug_log.info(msg)

    def error(self, msg):
        self.info_log.error(msg)
        self.error_log.error(msg)
        self.debug_log.error(msg)


# slow func

def loggedSlowFuncRunTime(func):
    def __log(*args, **kwargs):
        # ret = func(*args, **kwargs)
        oldtime = time.time() * 1000
        ret = func(*args, **kwargs)
        runtime = int(time.time() * 1000 - oldtime)
        if runtime > SLOW_TIME:
            SLOW_LOG.info(
                """
                ClassName: [%s]
                FunctionName: [%s]
                Kwargs: %s
                RunTime : %d (ms)
                """ % (args, func.__name__, kwargs, runtime))
        return ret

    return __log


