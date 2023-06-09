# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/1/31 14:31
# @Author  : chenyinhua
# @File    : models.py
# @Software: PyCharm
# @Desc: 全局变量

from enum import Enum, unique  # python 3.x版本才能使用
from typing import Text, Dict, Callable, Union, Optional, List, Any
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


class TestCaseEnum(Enum):
    FEATURE = ("feature", False)
    TITLE = ("title", True)
    URL = ("url", True)
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
    feature: Union[None, Text] = None
    title: Text
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
