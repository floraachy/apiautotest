# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/1/9 16:41
# @Author  : chenyinhua
# @File    : test_login_demo.py
# @Software: PyCharm
# @Desc: python脚本编写的测试用例文件

# 标准库导入
import os
# 第三方库导入
import pytest
import allure
from loguru import logger
# 本地应用/模块导入
from common_utils.yaml_handle import YamlHandle
from config.path_config import DATA_DIR
from config.settings import db_info
from config.global_vars import GLOBAL_VARS
from case_utils.assert_handle import assert_response, assert_sql
from case_utils.request_data_handle import RequestPreDataHandle, RequestHandle, after_request_extract
from case_utils.allure_handle import allure_title

# 读取用例数据
yaml_data = YamlHandle(filename=os.path.join(DATA_DIR, "gitlink", "login_demo.yaml")).read_yaml
case_common = yaml_data["case_common"]
cases = []
for k, v in yaml_data.items():
    if k != "case_common":
        cases.append(v)


@allure.epic(case_common["allure_epic"])
@allure.feature(case_common["allure_feature"])
class TestLoginDemo:

    @allure.story(case_common["allure_story"])
    @pytest.mark.test_demo
    @pytest.mark.parametrize("case", cases, ids=["{}".format(case["title"]) for case in cases])
    def test_login_demo_auto(self, case):
        logger.info("\n-----------------------------START-开始执行用例-----------------------------\n")
        logger.debug(f"当前执行的用例数据:{case}")
        # 添加用例标题作为allure中显示的用例标题
        allure_title(case.get("title", ""))
        # 处理请求前的用例数据
        case_data = RequestPreDataHandle(case).request_data_handle()
        # 发送请求
        response = RequestHandle(case_data).http_request()
        # 进行响应断言
        assert_response(response, case_data["assert_response"])
        # 进行数据库断言
        assert_sql(db_info[GLOBAL_VARS["env_key"]], case_data["assert_sql"])
        # 断言成功后进行参数提取
        after_request_extract(response, case_data.get("extract", None))
        logger.info("\n-----------------------------END-用例执行结束-----------------------------\n")
