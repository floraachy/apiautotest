import requests
from requests import Response
from requests_toolbelt import MultipartEncoder  # 第三方模块：pip install requests_toolbelt
from typing import Dict, Union
import time
from loguru import logger


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
    def send_request(cls, req_data: Dict[str, Union[str, Dict, MultipartEncoder]]) -> Response:
        """
        处理请求数据，转换成可用数据发送请求
        :param req_data: 请求数据
        :return: 响应对象
        """
        try:
            logger.info(f"\n======================================================\n" \
                        "-------------Start：请求前--------------------\n"
                        f"用例标题: {req_data.get('title', None)}\n" \
                        f"请求路径: {req_data.get('url', None)}\n" \
                        f"请求方式: {req_data.get('method', None)}\n" \
                        f"请求头:   {req_data.get('headers', None)}\n" \
                        f"请求关键字: {req_data.get('pk', None)}\n" \
                        f"请求内容: {req_data.get('payload', None)}\n" \
                        f"请求文件: {req_data.get('files', None)}\n" \
                        "=====================================================")
            res = cls.send_api_request(
                url=req_data.get("url"),
                method=req_data.get("method").lower(),
                pk=req_data.get("pk", None),
                header=req_data.get("headers"),
                payload=req_data.get("payload"),
                files=req_data.get("files")
            )
            logger.info(f"\n======================================================\n" \
                        "-------------End：请求后--------------------\n"
                        f"响应数据: {res.text}\n" \
                        "=====================================================")
        except requests.exceptions.RequestException as e:
            logger.error(f"请求出错，{str(e)}")
            raise ValueError(f"请求出错，{str(e)}")

        return res

    @classmethod
    def send_api_request(cls, url: str, method: str, pk: str, header: Dict[str, str] = None, payload=None,
                         files=None) -> Response:
        """
        发送请求
        :param method: 请求方法
        :param url: 请求url
        :param pk: 请求参数类型，可选值为params，json，data
        :param payload: 请求数据，对于不同请求类型，可以为dict，MultipartEncoder等
        :param files: 请求上传的文件
        :param header: 请求头
        :return: 返回res对象
        """
        headers = header or {}
        session = cls.get_session()

        if pk.lower() == 'params':
            res = session.request(method=method, url=url, params=payload, headers=headers)
        elif pk.lower() == 'data':
            if files:
                if not isinstance(files, dict):
                    raise ValueError('data参数必须为dict')
                encoder = MultipartEncoder(fields=files, boundary='------------------------' + str(time.time()))
                headers['Content-Type'] = encoder.content_type
                res = session.request(method=method, url=url, data=encoder.to_string(), headers=headers)
            else:
                headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
                res = session.request(method=method, url=url, data=payload, headers=headers)
        elif pk.lower() == 'json':
            if files:
                if not isinstance(files, dict):
                    raise ValueError('json参数必须为dict')
                encoder = MultipartEncoder(fields=files, boundary='------------------------' + str(time.time()))
                headers['Content-Type'] = encoder.content_type
                res = session.request(method=method, url=url, json=encoder.to_string(), headers=headers)
            else:
                headers['Content-Type'] = 'application/json'
                res = session.request(method=method, url=url, json=payload, headers=headers)
        else:
            raise ValueError('pk可选关键字为params, json, data')

        return res
