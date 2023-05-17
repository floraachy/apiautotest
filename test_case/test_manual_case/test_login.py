# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/1/9 16:41
# @Author  : chenyinhua
# @File    : test_login.py
# @Software: PyCharm
# @Desc: python脚本编写的测试用例文件


import pytest
import os
from common_utils.yaml_handle import HandleYaml
from config.project_path import DATA_DIR
from case_utils.requests_handle import BaseRequest
from case_utils.assert_handle import assert_result
from loguru import logger
from case_utils.request_data_handle import RequestPreDataHandle
from config.global_vars import GLOBAL_VARS

# 读取用例数据
cases = HandleYaml(filename=os.path.join(DATA_DIR, "test_login.yaml")).read_yaml


@pytest.mark.test_login
class TestLogin:
    """
    登录模块
    """

    @pytest.mark.parametrize("case", cases)
    def test_login(self, case):
        logger.info("-----------------------------START-开始执行用例-----------------------------")
        logger.debug(f"当前执行的用例数据:{case}")
        # 将用例标题title作为全局变量，方便后续写入到测试报告report.description中
        GLOBAL_VARS["title"] = case.get("title", "")
        if case.get("run", None):
            # 获取处理完成的用例数据
            case_data = RequestPreDataHandle(case).request_data_handle()
            # 发送请求
            response = BaseRequest.send_request(case_data)
            # 进行断言
            assert_result(response, case_data["expected"])
        else:
            reason = f"标记了该用例为false，不执行\\n"
            logger.warning(f"{reason}")
            pytest.skip(reason)
        logger.info("-----------------------------END-用例执行结束-----------------------------")
