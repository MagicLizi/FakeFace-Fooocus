# logger_mgr.py
#
# Author: MagicLizi
# Email: jiali@magiclizi.com | lizi@xd.com
# Created Time: 2023/4/28 14:57
import logging
import os
from logging.handlers import TimedRotatingFileHandler
import re
import traceback
# 日志
LOG_LEVEL = logging.DEBUG
LOG_INTERVAL = "D"

class ColoredFormatter(logging.Formatter):
    """自定义 Formatter 类，为日志添加颜色"""

    def __init__(self, fmt=None, datefmt=None, style='%'):
        super().__init__(fmt, datefmt, style)

        # 定义颜色代码
        self._colors = {
            'INFO': '\033[32m',  # 绿色
            'DEBUG': '\033[34m',  # 蓝色
            'WARNING': '\033[33m',  # 黄色
            'ERROR': '\033[31m',  # 红色
            'CRITICAL': '\033[35m',  # 紫色
            'RESET': '\033[0m'  # 清除颜色
        }

    def format(self, record):
        # 根据日志级别添加颜色
        color = self._colors.get(record.levelname, '')

        msg = trim_msg('%(message)s')
        # func = f"%(module)s:%(funcName)s"
        log_fmt = f"{color}[%(asctime)s - %(levelname)s] {msg} {self._colors['RESET']}"
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def trim_msg(msg):
    return re.sub(r'\n', '', msg)


__logger_map = {}


def __get_logger(logger_name):
    if logger_name in __logger_map:
        return __logger_map[logger_name]

    path = f"./logs/{logger_name}"
    # 尝试创建文件夹
    if not os.path.exists(path):
        os.makedirs(path)

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # %(module)s
    # create formatter
    msg = trim_msg('%(message)s')
    # func = f"%(module)s:%(funcName)s"
    formatter = logging.Formatter(f'[%(asctime)s - %(levelname)s] {msg}')

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(LOG_LEVEL)
    ch.setFormatter(ColoredFormatter())

    fh = TimedRotatingFileHandler(
        filename=f"./logs/{logger_name}/{logger_name}.log",
        when=LOG_INTERVAL,
        interval=1,
        backupCount=0
    )
    fh.setLevel(LOG_LEVEL)
    fh.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    __logger_map[logger_name] = logger

    return logger


def sys_log(msg, level="debug"):
    logger = __get_logger("sys")
    log_func = getattr(logger, level)
    log_func(msg)


def log(msg, user_id=None, level="info"):
    logger = __get_logger("main")
    log_msg = msg
    if user_id is not None:
        log_msg = f"[User:{user_id}] {msg}"
    log_func = getattr(logger, level)
    log_func(log_msg)


def except_hook(loop, context):
    exception = context.get('exception')
    logger = __get_logger("except")
    if exception:
        exc_traceback = "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))
        logger.error(f"except_hook - {exc_traceback}")
    else:
        logger.error(f"except_hook - 发生了一个未知错误")
