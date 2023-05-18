# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/1/31 14:31
# @Author  : chenyinhua
# @File    : request_data_handle.py
# @Software: PyCharm
# @Desc: 处理request请求前后的用例数据


from case_utils.data_handle import eval_data_process, case_data_replace
from config.global_vars import GLOBAL_VARS
from requests import Response
from loguru import logger
from case_utils.data_handle import json_extractor, re_extract


# ---------------------------------------- 请求前的数据处理----------------------------------------#

class RequestPreDataHandle:
    """
    请求前处理用例数据
    """

    def __init__(self, request_data):
        self.request_data = request_data

    def request_data_handle(self):
        """
        针对用例数据进行处理，识别用例数据中的关键字${xxxx}，使用全局变量进行替换或者执行关键字中的方法替换为具体值
        """
        self.url_handle()
        self.headers_handle()
        self.payload_handle()
        self.extract_handle()
        self.assert_handle()
        return self.request_data

    def url_handle(self):
        """
        用例数据中获取到的url(一般是不带host的，个别特殊的带有host，则不进行处理)
        """
        host = GLOBAL_VARS.get("host", "")
        url = self.request_data.get("url", "")
        logger.info(
            f"-----Start-----处理前的host： {GLOBAL_VARS.get('host', '')} || 处理前的url： {self.request_data.get('url', '')}")
        # 从用例数据中获取url，如果键url不存在，则返回空字符串
        # 如果url是以http开头的，则直接使用该url，不与host进行拼接
        if url.lower().startswith("http"):
            full_url = url
        else:
            # 如果host以/结尾 并且 url以/开头
            if host.endswith("/") and url.startswith("/"):
                full_url = host[0:len(host) - 1] + url
            # 如果host以/结尾 并且 url不以/开头
            elif host.endswith("/") and (not url.startswith("/")):
                full_url = host + url
            elif (not host.endswith("/")) and url.startswith("/"):
                # 如果host不以/结尾 且 url以/开头，则将host和url拼接起来，组成新的url
                full_url = host + url
            else:
                # 如果host不以/结尾 且 url不以/开头，则将host和url拼接起来的时候增加/，组成新的url
                full_url = host + "/" + url
        self.request_data["url"] = full_url
        logger.info(f"-----End-----处理完成后的full_url：{self.request_data['url']}")

    def headers_handle(self):
        # 从用例数据中获取header， 处理header
        logger.info(
            f"-----Start-----处理前的headers： {type(self.request_data.get('headers', None))} ||  {self.request_data.get('headers', None)}")
        if self.request_data.get("headers", None):
            self.request_data["headers"] = eval_data_process(case_data_replace(self.request_data.get("headers", None)))
            logger.info(
                f"-----End-----处理完成后的headers： {type(self.request_data['headers'])} ||  {self.request_data['headers']}")

    def payload_handle(self):
        # 处理请求参数payload
        logger.info(
            f"-----Start-----处理前的payload： {type(self.request_data.get('payload', None))} ||  {self.request_data.get('payload', None)}")
        if self.request_data.get("payload", None):
            self.request_data["payload"] = eval_data_process(case_data_replace(self.request_data.get("payload", None)))
            logger.info(
                f"-----End-----处理完成后的payload： {type(self.request_data['payload'])} ||  {self.request_data['payload']}")

    def extract_handle(self):
        # 处理后置提取参
        logger.info(
            f"-----Start-----处理前的extract： {type(self.request_data.get('extract', None))} ||  {self.request_data.get('extract', None)}")
        if self.request_data.get("extract", None):
            # 仅提取参数中的python表达式，不需要进行数据替换
            self.request_data["extract"] = eval_data_process(self.request_data.get("extract", None))
            logger.info(
                f"-----End-----处理完成后的extract： {type(self.request_data['extract'])} ||  {self.request_data['extract']}")

    def assert_handle(self):
        # 处理响应断言参数
        logger.info(
            f"-----Start-----处理前的assert_response： {type(self.request_data.get('assert_response', None))} ||  {self.request_data.get('assert_response', None)}")
        if self.request_data.get("assert_response", None):
            self.request_data["assert_response"] = eval_data_process(
                case_data_replace(self.request_data.get("assert_response", None)))
            logger.info(
                f"-----End-----处理完成后的assert_response： {type(self.request_data['assert_response'])} ||  {self.request_data['assert_response']}")


# ---------------------------------------- 请求后的参数提取处理----------------------------------------#
def after_extract(response: Response, extract) -> None:
    """
    从响应数据中提取请求后的参数，并保存到全局变量中
    :param response: request 响应对象
    :param extract: 需要提取的参数字典 '{"k1": "$.data"}' 或 '{"k1": "data:(.*?)$"}'
    :return:
    """
    logger.info(f"-----Start-----请求后的参数提取处理，需要提取的参数：{extract}-----")
    if extract:
        if response_type(response) == "json":
            # 如果响应数据是json格式，则将按照json方式对后置提取参数进行处理
            res = response.json()
            for k, v in extract.items():
                GLOBAL_VARS[k] = json_extractor(res, v)
        else:
            # 如果响应数据是str格式，则将按照str方式对后置提取参数进行处理
            res = response.text
            for k, v in extract.items():
                GLOBAL_VARS[k] = re_extract(res, v)
    logger.info(f"-----End-----参数提取后，打印当前的全局变量:{GLOBAL_VARS}")


def response_type(response: Response) -> str:
    """
    :param response: requests 返回
    :return: 返回响应数据类型 json或者str
    """
    try:
        response.json()
        return "json"
    except:
        return "str"
