# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/1/9 16:41
# @Author  : chenyinhua
# @File    : test_login_demo.py
# @Software: PyCharm
# @Desc: python脚本编写的测试用例文件

# 第三方库导入
import pytest
from loguru import logger
import allure
# 本地应用/模块导入
from case_utils.allure_handle import allure_title, custom_allure_step

# 读取用例数据
cases = [{"title": "demo用例01", "severity": "blocker1", "user": "flora", "age": 17, "run": True},
         {"title": "demo用例02", "severity": "TRIVIAL", "user": "flora", "age": 17, "run": True}]


@allure.story("demo模块(手动用例)")
@pytest.mark.test_demo
@pytest.mark.parametrize("case", cases, ids=["{}".format(case["title"]) for case in cases])
def test_demo(case):
    logger.info("\n-----------------------------START-开始执行用例-----------------------------\n")
    logger.debug(f"当前执行的用例数据:{case}")
    # 添加用例标题作为allure中显示的用例标题
    allure_title(case.get("title", ""))
    # 在allure报告中显示请求的用例数据
    custom_allure_step(step_title="用例数据", content=f"{case}")
    assert case["user"] == "flora"
    logger.info("\n-----------------------------END-用例执行结束-----------------------------\n")
