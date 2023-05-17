# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/1/31 14:31
# @Author  : chenyinhua
# @File    : requests_handle.py
# @Software: PyCharm
# @Desc: 处理request请求


import requests
from config.global_vars import GLOBAL_VARS
from requests import Response
from loguru import logger
from case_utils.data_handle import json_extractor, re_extract


# ---------------------------------------- 进行请求----------------------------------------#
class BaseRequest:
    """
    进行请求
    """
    session = None

    @classmethod
    def get_session(cls):
        """
        单例模式保证测试过程中使用的都是一个session对象；
        requests.session可以自动处理cookies，做状态保持。
        """
        if cls.session is None:
            cls.session = requests.Session()
        return cls.session

    @classmethod
    def send_request(cls, req_data: dict) -> Response:
        """
        处理case数据，转换成可用数据发送请求
        :param case: 读取出来的每一行用例内容
        return: 响应对象
        """
        logger.info(f"-----Start-----进行接口请求，并获取接口响应数据，请求数据：{type(req_data)} || {req_data}-----")
        # 进行接口请求，并获取接口响应数据
        res = cls.send_api(
            url=req_data["url"],
            method=req_data["method"],
            pk=req_data["pk"],
            header=req_data.get("headers", None),
            data=req_data.get("payload", None),
            file=req_data.get("files", None)
        )
        logger.info(f"-----End-----接口请求结束，请求响应数据：{res.text}-----")
        # 对用例数据中需要提取的后置参数，基于接口响应数据进行处理
        after_extract(res, req_data.get("extract", None))

        return res

    @classmethod
    def send_api(cls, url, method, pk, header=None, data=None, file=None) -> Response:
        """
        根据pk参数的不同，决定请求参数是使用params,data还是json
        :param method: 请求方法
        :param url: 请求url
        :param pk: 入参关键字， params(查询参数类型，明文传输，一般在url?参数名=参数值), data(一般用于form表单类型参数)
        json(一般用于json类型请求参数)
        :param data: 参数数据，默认等于None
        :param file: 文件对象
        :param header: 请求头
        :return: 返回res对象
        """
        session = cls.get_session()
        pk = pk.lower()
        if pk == 'params':
            res = session.request(method=method, url=url, params=data, headers=header)
        elif pk == 'data':
            res = session.request(method=method, url=url, data=data, files=file, headers=header)
        elif pk == 'json':
            res = session.request(method=method, url=url, json=data, files=file, headers=header)
        else:
            raise ValueError('pk可选关键字为params, json, data')
        return res


# ---------------------------------------- 请求后的参数提取处理----------------------------------------#
def after_extract(response: Response, extract: dict) -> None:
    """
    从响应数据中提取请求后的参数，并保存到全局变量中
    :param response: request 响应对象
    :param extract: 需要提取的参数字典 '{"k1": "$.data"}' 或 '{"k1": "data:(.*?)$"}'
    :return:
    """
    logger.info("-----Start-----请求后的参数提取处理-----")
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
