# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/1/31 15:02
# @Author  : chenyinhua
# @File    : loguru_handle.py
# @Software: PyCharm
# @Desc: 配置loguru日志值生成错误日志的方法

from loguru import logger


def error_only(record):
    """
    error日志判断
    Args:
        record:
    Returns: 若日志级别为ERROR，输出True
    """
    return record["level"].name == "ERROR"

