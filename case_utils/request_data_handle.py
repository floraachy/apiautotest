# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/1/31 14:31
# @Author  : chenyinhua
# @File    : request_data_handle.py
# @Software: PyCharm
# @Desc: 处理request请求前后的用例数据


from common_utils.data_handle import eval_data_process, data_replace
from config.global_vars import GLOBAL_VARS
from requests import Response
from loguru import logger
from common_utils.data_handle import json_extractor, re_extract
from case_utils.allure_handle import allure_step
from common_utils.base_request import BaseRequest


# ---------------------------------------- 请求前的数据处理----------------------------------------#

class RequestPreDataHandle:
    """
    请求前处理用例数据
    """

    def __init__(self, request_data):
        logger.info(f"\n======================================================\n" \
                    "-------------Start：处理用例数据前--------------------\n"
                    f"用例标题: {request_data.get('title', None)}\n" \
                    f"请求路径: {request_data.get('url', None)}\n" \
                    f"请求方式: {request_data.get('method', None)}\n" \
                    f"请求头:   {request_data.get('headers', None)}\n" \
                    f"请求cookies: {request_data.get('cookies', None)}\n" \
                    f"请求关键字: {request_data.get('pk', None)}\n" \
                    f"请求内容: {request_data.get('payload', None)}\n" \
                    f"请求文件: {request_data.get('files', None)}\n" \
                    f"后置提取参数: {request_data.get('extract', None)}\n" \
                    f"响应断言: {request_data.get('assert_response', None)}\n" \
                    f"数据库断言: {request_data.get('assert_sql', None)}\n" \
                    "=====================================================")
        self.request_data = request_data

    def request_data_handle(self):
        """
        针对用例数据进行处理，识别用例数据中的关键字${xxxx}，使用全局变量进行替换或者执行关键字中的方法替换为具体值
        """
        self.url_handle()
        self.method_handle()
        self.headers_handle()
        self.cookies_handle()
        self.payload_handle()
        self.files_handle()
        self.extract_handle()
        self.assert_handle()
        logger.info(f"\n======================================================\n" \
                    "-------------End：处理用例数据后--------------------\n"
                    f"用例标题: {self.request_data.get('title', None)}\n" \
                    f"请求路径: {self.request_data.get('url', None)}\n" \
                    f"请求方式: {self.request_data.get('method', None)}\n" \
                    f"请求头:   {self.request_data.get('headers', None)}\n" \
                    f"请求cookies:   {self.request_data.get('cookies', None)}\n" \
                    f"请求关键字: {self.request_data.get('pk', None)}\n" \
                    f"请求内容: {self.request_data.get('payload', None)}\n" \
                    f"请求文件: {self.request_data.get('files', None)}\n" \
                    f"后置提取参数: {self.request_data.get('extract', None)}\n" \
                    f"响应断言: {self.request_data.get('assert_response', None)}\n" \
                    f"数据库断言: {self.request_data.get('assert_sql', None)}\n" \
                    "=====================================================")
        return self.request_data

    def url_handle(self):
        """
        用例数据中获取到的url(一般是不带host的，个别特殊的带有host，则不进行处理)
        """
        host = GLOBAL_VARS.get("host", "")
        url = self.request_data.get("url", "")
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

    def method_handle(self):
        # TODO 暂时不需要处理，后续有需要在处理
        pass

    def cookies_handle(self):
        # 从用例数据中获取cookies， 处理cookies
        if self.request_data.get("cookies", None):
            self.request_data["cookies"] = eval_data_process(
                data_replace(content=self.request_data.get("cookies", None), source=GLOBAL_VARS))

    def headers_handle(self):
        # 从用例数据中获取header， 处理header
        if self.request_data.get("headers", None):
            self.request_data["headers"] = eval_data_process(
                data_replace(content=self.request_data.get("headers", None), source=GLOBAL_VARS))

    def payload_handle(self):
        # 处理请求参数payload
        if self.request_data.get("payload", None):
            self.request_data["payload"] = eval_data_process(
                data_replace(content=self.request_data.get("payload", None), source=GLOBAL_VARS))

    def files_handle(self):
        # 处理文件
        # TODO 暂时还没想好怎么处理
        pass

    def extract_handle(self):
        # 处理后置提取参数
        if self.request_data.get("extract", None):
            # 仅提取参数中的python表达式，不需要进行数据替换
            self.request_data["extract"] = eval_data_process(self.request_data.get("extract", None))

    def assert_handle(self):
        # 处理响应断言参数
        if self.request_data.get("assert_response", None):
            self.request_data["assert_response"] = eval_data_process(
                data_replace(content=self.request_data.get("assert_response", None), source=GLOBAL_VARS))


# ---------------------------------------- 进行请求，请求后的参数提取处理----------------------------------------#
class RequestHandle:
    """
    进行请求，请求后的参数提取处理
    """

    def __init__(self, case_data):
        self.case_data = case_data

    def send_request_extract(self):
        """
        发送请求并进行后置参数提取操作
        """
        response = BaseRequest.send_request(self.case_data)
        self.case_data["extract"] = self.after_extract(response, self.case_data.get("extract", None))
        # 从全局变量中获取最新值，替换数据库断言中的参数
        if self.case_data.get('assert_sql', None):
            self.case_data["assert_sql"] = eval_data_process(
                data_replace(content=self.case_data["assert_sql"], source=GLOBAL_VARS))
        logger.info(f"\n======================================================\n" \
                    "-------------请求数据--------------------\n"
                    f"用例标题: {self.case_data.get('title', None)}\n" \
                    f"请求路径: {self.case_data.get('url', None)}\n" \
                    f"请求方式: {self.case_data.get('method', None)}\n" \
                    f"请求头:   {self.case_data.get('headers', None)}\n" \
                    f"请求cookies: {self.case_data.get('cookies', None)}\n" \
                    f"请求关键字: {self.case_data.get('pk', None)}\n" \
                    f"请求内容: {self.case_data.get('payload', None)}\n" \
                    f"请求文件: {self.case_data.get('files', None)}\n" \
                    f"请求响应数据: {response.text}\n" \
                    f"后置提取参数（新）: {self.case_data.get('extract', None)}\n" \
                    f"数据库断言: {self.case_data.get('assert_sql', None)}\n" \
                    "=====================================================")
        allure_step(step_title=f"请求地址:{self.case_data['url']}")
        allure_step(step_title=f"请求方式：{self.case_data['method']}")
        allure_step(step_title="请求头", content=self.case_data['headers'])
        allure_step(step_title="请求Cookies", content=self.case_data['cookies'])
        allure_step(step_title="请求参数", content=self.case_data['payload'])
        allure_step(step_title="请求文件", content=self.case_data['files'])
        allure_step(step_title="后置提取参数（新）", content=self.case_data['extract'])
        allure_step(step_title="响应断言参数", content=self.case_data['assert_response'])
        allure_step(step_title="数据库断言", content=self.case_data['assert_sql'])
        allure_step(step_title="请求响应数据", content=response.text)
        return response

    def after_extract(self, response: Response, extract):
        """
        从响应数据中提取请求后的参数，并保存到全局变量中
        :param response: request 响应对象
        :param extract: 需要提取的参数字典 '{"k1": "$.data"}' 或 '{"k1": "data:(.*?)$"}'
        :return:
        """
        logger.debug(f"-----Start-----请求后的参数提取处理，需要提取的参数：{extract}-----")
        result = {}
        if extract:
            if response_type(response) == "json":
                # 如果响应数据是json格式，则将按照json方式对后置提取参数进行处理
                res = response.json()
                for k, v in extract.items():
                    result[k] = json_extractor(res, v)
            else:
                # 如果响应数据是str格式，则将按照str方式对后置提取参数进行处理
                res = response.text
                for k, v in extract.items():
                    result[k] = re_extract(res, v)
        logger.debug(f"-----End-----参数提取后，打印提取到的变量:{result}")
        # 将提取到的变量保存在全局变量中
        if result:
            for k, v in result.items():
                GLOBAL_VARS[k] = v
        return result


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
