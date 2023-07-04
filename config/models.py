# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/1/31 14:31
# @Author  : chenyinhua
# @File    : models.py
# @Software: PyCharm
# @Desc: 全局变量

# 标准库导入
from enum import Enum, unique  # python 3.x版本才能使用
from typing import Text, Dict, Union, Any
# 第三方库导入
from pydantic import BaseModel


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


@unique  # 枚举类装饰器，确保只有一个名称绑定到任何一个值。
class AllureAttachmentType(Enum):
    """
    allure 报告的文件类型枚举
    """
    TEXT = "txt"
    CSV = "csv"
    TSV = "tsv"
    URI_LIST = "uri"

    HTML = "html"
    XML = "xml"
    JSON = "json"
    YAML = "yaml"
    PCAP = "pcap"

    PNG = "png"
    JPG = "jpg"
    SVG = "svg"
    GIF = "gif"
    BMP = "bmp"
    TIFF = "tiff"

    MP4 = "mp4"
    OGG = "ogg"
    WEBM = "webm"

    PDF = "pdf"


class Severity(str, Enum):
    """
    测试用例优先级
    """
    BLOCKER = 'BLOCKER'  # blocker：阻塞缺陷（中断缺陷，客户端程序无响应，无法执行下一步操作）
    CRITICAL = 'CRITICAL'  # critical：严重缺陷（临界缺陷，功能点缺失）
    NORMAL = 'NORMAL'  # normal： 一般缺陷（边界情况，格式错误）
    MINOR = 'MINOR'  # minor：次要缺陷（界面错误与ui需求不符）
    TRIVIAL = 'TRIVIAL'  # trivial： 轻微缺陷（必须项无提示，或者提示不规范）


class TestCaseEnum(Enum):
    """
    测试用例中字段
    """
    FEATURE = ("feature", False)
    TITLE = ("title", True)
    URL = ("url", True)
    SEVERITY = ("severity", False)
    METHOD = ("method", True)
    HEADERS = ("headers", True)
    COOKIES = ("cookies", False)
    RUN = ("run", False)
    REQUEST_TYPE = ("request_type", True)
    PAYLOAD = ("payload", False)
    FILES = ("files", False)
    EXTRACT = ("extract", False)
    ASSERT_RESPONSE = ("assert_response", True)
    ASSERT_SQL = ("assert_sql", False)


class TestCase(BaseModel):
    """
    测试用例各数据格式要求
    """
    feature: Union[None, Text] = None
    title: Text
    severity: Text
    url: Text
    method: Text
    headers: Union[None, Dict, Text] = {}
    cookies: Union[None, Dict, Text]
    request_type: Text
    run: Union[None, bool, Text] = None
    payload: Any = None
    files: Any = None
    extract: Union[None, Dict, Text] = None
    assert_response: Union[None, Dict, Text]
    assert_sql: Union[None, Dict, Text] = None


class Method(Enum):
    """
    请求方式
    """
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTION = "OPTION"


class RequestType(Enum):
    """
    request请求发送，请求参数的数据类型
    """
    JSON = "JSON"
    PARAMS = "PARAMS"
    DATA = "DATA"
    FILE = 'FILE'
    EXPORT = "EXPORT"
    NONE = "NONE"
