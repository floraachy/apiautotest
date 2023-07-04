# -*- coding: utf-8 -*-
# @Time    : 2023/3/28 23:17
# @Author  : Flora.Chen
# @File    : conftest.py
# @Software: PyCharm
# @Desc:

# 标准库导入
import json
# 第三方库导入
import pytest
import requests
import allure
from loguru import logger
# 本地应用/模块导入
from config.global_vars import GLOBAL_VARS
from common_utils.base_request import BaseRequest


@pytest.fixture(scope="function", autouse=True)
def case_skip(request):
    """处理跳过用例"""
    # 使用 request.getfixturevalue() 方法来获取测试用例函数的参数值
    # 注意这里的"case"需要与@pytest.mark.parametrize("case", cases)中传递的保持一致
    case = request.getfixturevalue("case")
    if case.get("run") is None or case.get("run") is False:
        reason = f"{case.get('title')}: 标记了该用例为false，不执行\\n"
        logger.warning(f"{reason}")
        pytest.skip(reason)


def pytest_collection_modifyitems(config, items):
    for item in items:
        # 注意这里的"case"需要与@pytest.mark.parametrize("case", cases)中传递的保持一致
        parameters = item.callspec.params["case"]
        # print(f"测试参数：{type(parameters)}     {parameters}")
        if parameters.get("severity"):
            if parameters["severity"].upper() == "TRIVIAL":
                item.add_marker(allure.severity(allure.severity_level.TRIVIAL))
            elif parameters["severity"].upper() == "MINOR":
                item.add_marker(allure.severity(allure.severity_level.MINOR))
            elif parameters["severity"].upper() == "CRITICAL":
                item.add_marker(allure.severity(allure.severity_level.CRITICAL))
            elif parameters["severity"].upper() == "BLOCKER":
                item.add_marker(allure.severity(allure.severity_level.BLOCKER))
            else:
                item.add_marker(allure.severity(allure.severity_level.NORMAL))
        else:
            item.add_marker(allure.severity(allure.severity_level.NORMAL))


@pytest.fixture(scope="session")
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
        "request_type": "json",
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
