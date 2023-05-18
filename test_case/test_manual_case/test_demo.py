# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/1/9 16:41
# @Author  : chenyinhua
# @File    : test_login_demo.py
# @Software: PyCharm
# @Desc: python脚本编写的测试用例文件


import pytest
from loguru import logger
from pytest_html import extras  # 往pytest-html报告中填写额外的内容
from common_utils.func_handle import add_docstring

# 读取用例数据
cases = [{"title": "demo cese_01", "user": "flora", "age": 17, "run": False}]


@pytest.mark.test_login_demo
@pytest.mark.parametrize("case", cases)
def test_demo(case, extra):
    logger.info("-----------------------------START-开始执行用例-----------------------------")
    logger.debug(f"当前执行的用例数据:{case}")
    # 给当前测试方法添加文档注释
    add_docstring(case.get("title", ""))(test_demo)
    if case.get("run", None):
        assert case["user"] == "flora"
        # 将用例数据显示在pytest-html报告中
        extra.append(extras.json(case, name="用例数据"))
    else:
        reason = f"标记了该用例为false，不执行\\n"
        logger.warning(f"{reason}")
        pytest.skip(reason)
    logger.info("-----------------------------END-用例执行结束-----------------------------")
