# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/1/9 16:41
# @Author  : chenyinhua
# @File    : test_login_demo.py
# @Software: PyCharm
# @Desc: python脚本编写的测试用例文件


import pytest
import os
from common_utils.yaml_handle import HandleYaml
from config.settings import DATA_DIR
from common_utils.base_request import BaseRequest
from case_utils.assert_handle import assert_response, assert_sql
from loguru import logger
from case_utils.request_data_handle import RequestPreDataHandle, after_extract, case_data_replace, eval_data_process
from pytest_html import extras  # 往pytest-html报告中填写额外的内容
from common_utils.func_handle import add_docstring

# 读取用例数据
cases = HandleYaml(filename=os.path.join(DATA_DIR, "test_login_demo.yaml")).read_yaml


@pytest.mark.test_login_demo
@pytest.mark.parametrize("case", cases)
def test_login_demo(case, extra, request):
    logger.info("-----------------------------START-开始执行用例-----------------------------")
    logger.debug(f"当前执行的用例数据:{case}")
    try:
        # 获取命令行参数，判断当前处于哪个环境
        env = request.config.getoption("--env")
        # 给当前测试方法添加文档注释
        add_docstring(case.get("title", ""))(test_login)
        if case.get("run", None):
            # 处理请求前的用例数据
            case_data = RequestPreDataHandle(case).request_data_handle()
            # 将用例数据显示在pytest-html报告中
            extra.append(extras.text(str(case_data), name="用例数据"))
            # 发送请求
            response = BaseRequest.send_request(case_data)
            # 将响应数据显示在pytest-html报告中
            extra.append(extras.text(str(response.text), name="响应数据"))
            # 请求后，提取后置参数作为全局变量
            after_extract(response, case_data["extract"])
            # 从全局变量中获取最新值，替换数据库断言中的参数
            case_data["assert_sql"] = eval_data_process(case_data_replace(case_data["assert_sql"]))
            # 进行响应断言
            assert_response(response, case_data["assert_response"])
            # 进行数据库断言
            assert_sql(env, case_data["assert_sql"])
        else:
            reason = f"标记了该用例为false，不执行\\n"
            logger.warning(f"{reason}")
            pytest.skip(reason)
    except Exception as e:
        logger.error(f"用例执行过程中报错：{e}")
        raise e
    finally:
        logger.info("-----------------------------END-用例执行结束-----------------------------")
