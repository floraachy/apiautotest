# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/1/31 14:31
# @Author  : chenyinhua
# @File    : request_data_handle.py
# @Software: PyCharm
# @Desc: 处理request请求前的用例数据


import re
from string import Template
from config.global_vars import GLOBAL_VARS
from loguru import logger
from case_utils.data_handle import exec_func
from case_utils.data_handle import eval_data_process


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
        logger.info(f"-----Start-----初始获取的测试用例数据：----- {type(self.request_data)} || {self.request_data}")

        # 从用例数据中获取url，如果键url不存在，则返回空字符串
        url = self.request_data.get("url", "")
        self.request_data["url"] = self.url_handle(url)

        # 从用例数据中获取files，如果键files不存在，则返回None
        files = self.request_data.get("files", None)
        self.request_data["files"] = self.files_handle(files)

        request_data = eval_data_process(case_data_replace(self.request_data))

        logger.info(f"-----End-----处理完成后的测试用例数据：-----{type(request_data)} ||  {request_data}")
        return request_data

    def url_handle(self, url):
        """
        用例数据中获取到的url(一般是不带host的，个别特殊的带有host，则不进行处理)
        """
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
        return full_url

    def files_handle(self, files):
        """
        格式：接口中文件参数的名称:"文件路径地址"/["文件地址1", "文件地址2"]
        """

        if files is None:
            return

        if files != "" and files is not None:
            files = eval(files)
            for k, v in files.items():
                # 多文件上传
                if isinstance(v, list):
                    files = []
                    for path in v:
                        files.append((k, (open(path, 'rb'))))
                else:
                    # 单文件上传
                    files = {k: open(v, 'rb')}

        return files


def case_data_replace(content):
    """
    用例数据替换的方法
    :param content: 原始的字符串内容
    return content： 替换表达式后的字符串
    """
    if content is None:
        return None
    if len(content) != 0:
        logger.debug(f"开始进行字符串替换: 替换字符串为：{content}")
        content = Template(str(content)).safe_substitute(GLOBAL_VARS)
        logger.debug(f"使用模板函数Template替换字符串完成。 替换后的字符串如下：{content}")
        for func in re.findall('\\${(.*?)}', content):
            try:
                content = content.replace('${%s}' % func, exec_func(func))
                logger.debug(f"通过执行函数替换用例数据值 替换字符串后为：{content}")
            except Exception as e:
                logger.exception(e)
        return content
