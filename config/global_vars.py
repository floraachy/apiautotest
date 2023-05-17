# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/1/31 14:31
# @Author  : chenyinhua
# @File    : global_vars.py
# @Software: PyCharm
# @Desc: 全局变量

from enum import Enum

# 定义一个全局变量，作用于接口关联数据存储
GLOBAL_VARS = {}


class CaseFileType(Enum):
    """
    用例数据可存储文件的类型枚举
    """
    YAML = 1
    EXCEL = 2
    ALL = 0


class NotificationType(Enum):
    """ 自动化通知方式 """
    DEFAULT = 0
    DING_TALK = 1
    WECHAT = 2
    EMAIL = 3
    ALL = 4

