# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/1/31 14:31
# @Author  : chenyinhua
# @File    : request_data_handle.py
# @Software: PyCharm
# @Desc: 处理request请求前后的用例数据

# 标准库导入
import json
import os
import http.cookiejar
# 第三方库导入
from requests import Response
from loguru import logger
import allure
# 本地应用/模块导入
from common_utils.files_handle import get_file_field
from common_utils.base_request import BaseRequest
from case_utils.data_handle import data_handle
from case_utils.extract_data_handle import json_extractor, re_extract
from case_utils.allure_handle import custom_allure_step
from config.global_vars import GLOBAL_VARS
from config.path_config import FILES_DIR


# ---------------------------------------- 请求前的数据处理----------------------------------------#

class RequestPreDataHandle:
    """
    请求前处理用例数据
    """

    def __init__(self, request_data):
        logger.debug(f"\n======================================================\n" \
                     "-------------Start：处理用例数据前--------------------\n"
                     f"用例标题(title): {type(request_data.get('title', None))} || {request_data.get('title', None)}\n" \
                     f"用例优先级(severity): {type(request_data.get('severity', None))} || {request_data.get('severity', None)}\n" \
                     f"请求路径(url): {type(request_data.get('url', None))} || {request_data.get('url', None)}\n" \
                     f"请求方式(method): {type(request_data.get('method', None))} || {request_data.get('method', None)}\n" \
                     f"请求头(headers):   {type(request_data.get('headers', None))} || {request_data.get('headers', None)}\n" \
                     f"请求cookies: {type(request_data.get('cookies', None))} || {request_data.get('cookies', None)}\n" \
                     f"请求类型(request_type): {type(request_data.get('request_type', None))} || {request_data.get('request_type', None)}\n" \
                     f"请求参数(payload): {type(request_data.get('payload', None))} || {request_data.get('payload', None)}\n" \
                     f"请求文件(files): {type(request_data.get('files', None))} || {request_data.get('files', None)}\n" \
                     f"后置提取参数(extract): {type(request_data.get('extract', None))} || {request_data.get('extract', None)}\n" \
                     f"响应断言(assert_response): {type(request_data.get('assert_response', None))} || {request_data.get('assert_response', None)}\n" \
                     f"数据库断言(assert_sql): {type(request_data.get('assert_sql', None))} || {request_data.get('assert_sql', None)}\n" \
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
        self.assert_handle()
        logger.debug(f"\n======================================================\n" \
                     "-------------End：处理用例数据后--------------------\n"
                     f"用例标题(title):  {type(self.request_data.get('title', None))} || {self.request_data.get('title', None)}\n" \
                     f"用例优先级(severity): {type(self.request_data.get('severity', None))} || {self.request_data.get('severity', None)}\n" \
                     f"请求路径(url): {type(self.request_data.get('url', None))} || {self.request_data.get('url', None)}\n" \
                     f"请求方式(method): {type(self.request_data.get('method', None))} || {self.request_data.get('method', None)}\n" \
                     f"请求头(headers):   {type(self.request_data.get('headers', None))} || {self.request_data.get('headers', None)}\n" \
                     f"请求cookies: {type(self.request_data.get('cookies', None))} || {self.request_data.get('cookies', None)}\n" \
                     f"请求类型(request_type): {type(self.request_data.get('request_type', None))} || {self.request_data.get('request_type', None)}\n" \
                     f"请求参数(payload): {type(self.request_data.get('payload', None))} || {self.request_data.get('payload', None)}\n" \
                     f"请求文件(files): {type(self.request_data.get('files', None))} || {self.request_data.get('files', None)}\n" \
                     f"后置提取参数(extract): {type(self.request_data.get('extract', None))} || {self.request_data.get('extract', None)}\n" \
                     f"响应断言(assert_response): {type(self.request_data.get('assert_response', None))} || {self.request_data.get('assert_response', None)}\n" \
                     f"数据库断言(assert_sql): {type(self.request_data.get('assert_sql', None))} || {self.request_data.get('assert_sql', None)}\n" \
                     "=====================================================")
        return self.request_data

    def url_handle(self):
        try:
            """
            用例数据中获取到的url(一般是不带host的，个别特殊的带有host，则不进行处理)
            """
            # 检测url中是否存在需要替换的参数，如果存在则进行替换
            url = data_handle(obj=self.request_data.get("url", None), source=GLOBAL_VARS)
            # 进行url处理，最终得到full_url
            host = GLOBAL_VARS.get("host", "")
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
        except Exception as e:
            logger.error(f"处理url报错了：{e}")
            raise TypeError(f"处理url报错了：{e}")

    def method_handle(self):
        # TODO 暂时不需要处理，后续有需要在处理
        pass

    def cookies_handle(self):
        """
        requests模块中，cookies参数要求是Dict or CookieJar object
        """
        cookies = self.request_data.get("cookies", None)

        # 从用例数据中获取cookies， 处理cookies
        if cookies:
            logger.debug(f"打印一下全局变量的值：{GLOBAL_VARS}")
            print(f"打印一下全局变量的值：{GLOBAL_VARS}")
            # 通过全局变量替换cookies，得到的是一个str类型
            cookies = data_handle(obj=cookies, source=GLOBAL_VARS)
            try:
                cookies = json.loads(cookies)
            except Exception as e:
                cookies = cookies
                logger.debug(f"处理{cookies}报错了：{e}")
                print(f"处理{cookies}报错了：{e}")
            if isinstance(cookies, dict) or isinstance(cookies, http.cookiejar.CookieJar):
                self.request_data["cookies"] = cookies
            else:
                logger.error(f"cookies参数要求是Dict or CookieJar object， 目前cookies类型是：{type(cookies)}， cookies值是：{cookies}")
                raise TypeError(f"cookies参数要求是Dict or CookieJar object， 目前cookies类型是：{type(cookies)}， cookies值是：{cookies}")

    def headers_handle(self):
        """
        headers里面传cookies，要求cookies类型是str
        """
        headers = self.request_data.get("headers", None)
        try:
            # 从用例数据中获取header， 处理header
            if headers:
                self.request_data["headers"] = data_handle(obj=headers, source=GLOBAL_VARS)
                # 如果请求头中有cookies，需要进行单独处理
                if self.request_data["headers"].get("cookies", None):
                    cookies = self.request_data["headers"]["cookies"]
                    if isinstance(cookies, dict):
                        # 如果是字典类型，就转成字符串
                        self.request_data["headers"]["cookies"] = json.dumps(cookies)
                    else:
                        self.request_data["headers"]["cookies"] = cookies
        except Exception as e:
            logger.error(f"处理{headers}报错了：{e}")
            raise TypeError(f"处理{headers}报错了：{e}")

    def payload_handle(self):
        # 处理请求参数payload
        payload = self.request_data.get("payload", None)
        try:
            if payload:
                self.request_data["payload"] = data_handle(obj=payload, source=GLOBAL_VARS)
        except Exception as e:
            logger.error(f"处理{payload}报错了：{e}")
            raise TypeError(f"处理{payload}报错了：{e}")

    def files_handle(self):
        """
        格式：接口中文件参数的名称:"文件路径地址"/["文件地址1", "文件地址2"]
        例如：{"file": "test_demo.py"}
        或者
        {"file": ["test_demo_01.py", "test_demo_02.py"]}
        """
        # 处理请求参数files参数
        files = self.request_data.get("files", None)
        try:
            if files:
                for k, v in files.items():
                    # ------------------ 处理多文件的情况 ------------------
                    # 这里需要注意：不一定所有接口都支持多文件上传
                    _files = []
                    if isinstance(v, list):
                        for file in v:
                            # 处理文件绝对路径
                            file_path = os.path.join(FILES_DIR, file)
                            # 多文件上传需要是元祖[('file', (filename, file_content)), ('file', (filename, file_content))]
                            _files.append((k, get_file_field(file_path)))
                        self.request_data["files"] = _files
                    else:
                        # ------------------ 处理单文件的情况 ------------------
                        # 处理文件绝对路径
                        file_path = os.path.join(FILES_DIR, v)
                        # 单文件上传需要是字典{'file': (filename, file_content)}
                        self.request_data["files"] = {k: get_file_field(file_path)}
                logger.debug(f"处理完成后的file:{self.request_data['files']}")
        except Exception as e:
            logger.error(f"处理{files}报错了：{e}")
            raise TypeError(f"处理{files}报错了：{e}")

    def assert_handle(self):
        # 处理响应断言参数
        assert_response = self.request_data.get("assert_response", None)
        try:
            if assert_response:
                self.request_data["assert_response"] = data_handle(obj=assert_response, source=GLOBAL_VARS)
            # 由于数据库断言里面的变量需要请求响应后进行提取，因此目前不进行处理
        except Exception as e:
            logger.error(f"处理{assert_response}报错了：{e}")
            raise TypeError(f"处理{assert_response}报错了：{e}")


# ---------------------------------------- 进行请求，请求后的参数提取处理----------------------------------------#
class RequestHandle:
    """
    进行请求，请求后的参数提取处理
    """

    def __init__(self, case_data):
        self.case_data = case_data

    @allure.step("发送请求")
    def http_request(self):
        """
        发送请求并进行后置参数提取操作
        """
        response = BaseRequest.send_request(self.case_data)
        # 处理数据库断言 - 从全局变量中获取最新值，替换数据库断言中的参数
        if self.case_data.get('assert_sql', None):
            self.case_data["assert_sql"] = data_handle(obj=self.case_data["assert_sql"], source=GLOBAL_VARS)
        logger.info(f"\n======================================================\n"
                    "-------------执行请求获取响应数据--------------------\n"
                    f"用例标题(title): {type(self.case_data.get('title', None))} || {self.case_data.get('title', None)}\n"
                    f"请求路径(url): {type(self.case_data.get('url', None))} || {self.case_data.get('url', None)}\n"
                    f"请求方式(method): {type(self.case_data.get('method', None))} || {self.case_data.get('method', None)}\n"
                    f"请求头(headers):   {type(self.case_data.get('headers', None))} || {self.case_data.get('headers', None)}\n"
                    f"请求cookies: {type(self.case_data.get('cookies', None))} || {self.case_data.get('cookies', None)}\n"
                    f"请求类型(request_type): {type(self.case_data.get('request_type', None))} || {self.case_data.get('request_type', None)}\n"
                    f"请求参数(payload): {type(self.case_data.get('payload', None))} || {self.case_data.get('payload', None)}\n")
        custom_allure_step(step_title=f"请求地址(url):{self.case_data['url']}")
        custom_allure_step(step_title=f"请求方式(method)：{self.case_data['method']}")
        custom_allure_step(step_title="请求头(headers)", content=self.case_data['headers'])
        custom_allure_step(step_title="请求Cookies", content=str(self.case_data['cookies']))
        custom_allure_step(step_title="请求参数(payload)", content=self.case_data['payload'])
        # 处理请求里面的files，使得日志以及allure中写入的是文件，而不是文件二进制内容
        if self.case_data.get('files', None):
            files = self.case_data["files"]
            if isinstance(files, list):
                for file in files:
                    _file = os.path.join(FILES_DIR, file[1][0])
                    logger.info(
                        f"\n请求文件(files): {type(_file)} || {_file}\n")
                    custom_allure_step(step_title="请求文件(files)", source=_file)
            elif isinstance(files, dict):
                dict_values = list(files.values())[0]
                _file = os.path.join(FILES_DIR, dict_values[0])
                logger.info(
                    f"\n请求文件(files): {type(_file)} || {_file}\n")
                custom_allure_step(step_title="请求文件(files)", source=_file)
        logger.info(
            f"\n请求响应数据(response): {response.text}\n"
            f"请求响应码(code): {response.status_code}\n"
            f"响应耗时: {round(response.elapsed.total_seconds(), 2)} s || {round(response.elapsed.total_seconds() * 1000, 2)} ms\n"
            "=====================================================")
        try:
            res = response.json()
            custom_allure_step(step_title="请求响应数据(response)", content=res)
        except:
            custom_allure_step(step_title="请求响应数据(response)", content=response.text)
        custom_allure_step(step_title=f"请求响应码(code):{response.status_code}")
        custom_allure_step(
            step_title=f"响应耗时:{round(response.elapsed.total_seconds(), 2)} s || {round(response.elapsed.total_seconds() * 1000, 2)} ms")
        return response


# ---------------------------------------- 请求后的参数提取处理----------------------------------------#
def after_request_extract(response: Response, extract):
    """
    从响应数据中提取请求后的参数，并保存到全局变量中
    :param response: request 响应对象
    :param extract: 需要提取的参数字典 '{"k1": "$.data"}' 或 '{"k1": "data:(.*?)$"}'
    :return:
    """
    logger.debug(f"\n======================================================\n" \
                 "-------------Start：从响应数据中提取后置参数保存到全局变量--------------------\n"
                 f"后置提取参数（原）: {extract}\n" \
                 "=====================================================")
    result = {}
    if extract:
        try:
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
        except Exception as e:
            logger.error(f"提取后置参数报错：{e}")
    logger.debug(f"\n======================================================\n" \
                 "-------------End：从响应数据中提取后置参数保存到全局变量--------------------\n"
                 f"后置提取参数（新）: {result}\n" \
                 "=====================================================")
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
