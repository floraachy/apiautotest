# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/1/9 16:41
# @Author  : chenyinhua
# @File    : test_login_demo.py
# @Software: PyCharm
# @Desc: python脚本编写的测试用例文件


import pytest
import os
from common_utils.yaml_handle import YamlHandle
from config.path_config import DATA_DIR
from case_utils.assert_handle import assert_response, assert_sql
from loguru import logger
from case_utils.request_data_handle import RequestPreDataHandle, RequestHandle, after_request_extract
from pytest_html import extras  # 往pytest-html报告中填写额外的内容
from common_utils.func_handle import add_docstring
from case_utils.allure_handle import allure_title
import allure
from config.settings import db_info
from config.global_vars import GLOBAL_VARS

# 读取用例数据
cases = YamlHandle(filename=os.path.join(DATA_DIR, "test_login_demo.yaml")).read_yaml


@allure.story(f'{cases["case_common"]["allure_story"]}')
@pytest.mark.test_login_demo
@pytest.mark.parametrize("case", cases.get("case_info"))
def test_login_demo(case, extra):
    logger.info("-----------------------------START-开始执行用例-----------------------------")
    logger.debug(f"当前执行的用例数据:{case}")
    # 给当前测试方法添加文档注释
    add_docstring(case.get("title", ""))(test_login_demo)
    # 添加用例标题作为allure中显示的用例标题
    allure_title(case.get("title", ""))
    if case.get("run", None):
        # 处理请求前的用例数据
        case_data = RequestPreDataHandle(case).request_data_handle()
        # 将用例数据显示在pytest-html报告中
        extra.append(extras.text(str(case_data), name="用例数据"))
        # 发送请求
        response = RequestHandle(case_data).http_request()
        # 将响应数据显示在pytest-html报告中
        extra.append(extras.text(str(response.text), name="响应数据"))
        # 进行响应断言
        assert_response(response, case_data["assert_response"])
        # 进行数据库断言
        assert_sql(db_info[GLOBAL_VARS["env_key"]], case_data["assert_sql"])
        # 断言成功后进行参数提取
        after_request_extract(response, case_data.get("extract", None))
    else:
        reason = f"标记了该用例为false，不执行\\n"
        logger.warning(f"{reason}")
        pytest.skip(reason)
    logger.info("-----------------------------END-用例执行结束-----------------------------")
