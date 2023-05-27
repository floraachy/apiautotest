# -*- coding: utf-8 -*-
# @Time    : 2023/3/28 23:17
# @Author  : Flora.Chen
# @File    : conftest.py
# @Software: PyCharm
# @Desc:

import json
import pytest
import requests
from config.global_vars import GLOBAL_VARS
from loguru import logger
from common_utils.base_request import BaseRequest


@pytest.fixture(scope="session", autouse=True)
def login_init():
    """
    获取登录的cookie
    :return:
    """
    host = GLOBAL_VARS.get("host")
    login = GLOBAL_VARS.get('login')
    password = GLOBAL_VARS.get('password')
    # 兼容一下host后面多一个斜线的情况
    if host[-1] == "/":
        host = host[:len(host) - 1]
    req_data = {
        "url": host + "/api/accounts/login.json",
        "method": "POST",
        "pk": "json",
        "headers": {"Content-Type": "application/json; charset=utf-8;"},
        "payload": {"login": login, "password": password, "autologin": 1}
    }
    # 请求登录接口
    try:
        res = BaseRequest.send_request(req_data=req_data)
        res.raise_for_status()
        # 将cookies转成字典,再转成字符串
        cookies = json.dumps(requests.utils.dict_from_cookiejar(res.cookies))
        GLOBAL_VARS["login_cookie"] = cookies
        GLOBAL_VARS["login"] = res.json()["login"]
        GLOBAL_VARS["nickname"] = res.json()["username"]
        GLOBAL_VARS["user_id"] = res.json()["user_id"]
        logger.debug(f"获取用户：{login}登录的cookies成功：{type(cookies)} || {cookies}")
    except Exception as e:
        GLOBAL_VARS["login_cookie"] = None
        logger.error(f"获取用户：{login}登录的cookies失败：{e}")
