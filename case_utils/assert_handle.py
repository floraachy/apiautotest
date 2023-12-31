# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/2/1 14:31
# @Author  : chenyinhua
# @File    : assert_handle.py
# @Software: PyCharm
# @Desc: 断言

# 第三方库导入
from loguru import logger
from requests import Response
import allure
# 本地应用/模块导入
from case_utils.extract_data_handle import json_extractor, re_extract
from case_utils.request_data_handle import response_type
from case_utils.allure_handle import custom_allure_step
from common_utils.mysql_handle import MysqlServer


@allure.step("响应断言")
def assert_response(response: Response, expected: dict) -> None:
    """ 断言方法
    :param response: 实际响应对象
    :param expected: 预期响应内容，从excel中或者yaml读取、或者手动传入,格式如下：
    {
    'eq':
        {'http_code': 200, '$.user_id': '85392'},
    "in":
        {'message': "success"}
    }
    return None
    """
    logger.info("\n======================================================\n" \
                f"-------------Start：响应断言--------------------\n")
    if expected is None:
        logger.info("判断是否存在响应断言---->当前用例无响应断言！")
        custom_allure_step(step_title='判断是否存在响应断言---->当前用例无响应断言！')
        return
    logger.debug(f"响应断言预期结果：{expected}, {type(expected)}")
    index = 0
    for k, v in expected.items():
        # 获取需要断言的实际结果部分
        for _k, _v in v.items():
            if _k == "http_code":
                actual = response.status_code
            else:
                if response_type(response) == "json":
                    # 如果响应数据是json格式
                    actual = json_extractor(response.json(), _k)
                else:
                    # 响应数据不是json格式
                    actual = re_extract(response.text, _k)
            index += 1
            logger.info(f'第{index}个响应断言 -|- 预期结果: {_k}: {_v}, {type(_v)}   {k}   实际结果: {actual}, {type(actual)}')
            custom_allure_step(
                step_title=f'第{index}个响应断言数据---->预期结果: {_k}: {_v}, {type(_v)}   {k}   实际结果: {actual}, {type(actual)}')
            try:
                if k == "eq":  # 预期结果 = 实际结果
                    assert _v == actual
                    logger.success(f"预期结果: {_k}: {_v} ==  实际结果: {actual}, 断言成功！")
                elif k == "in":  # 实际结果 包含 预期结果
                    assert _v in actual
                    logger.success(f"预期结果: {_k}: {_v} in  实际结果: {actual}, 断言成功！")
                elif k == "gt":  # 预期结果 > 实际结果 (值应该为数值型)
                    assert _v > actual
                    logger.success(f"预期结果: {_k}: {_v} >  实际结果: {actual}, 断言成功！")
                elif k == "lt":  # 预期结果 < 实际结果 (值应该为数值型)
                    assert _v < actual
                    logger.success(f"预期结果: {_k}: {_v} <  实际结果: {actual}, 断言成功！")
                elif k == "not":  # 预期结果 != 实际结果
                    assert _v != actual
                    logger.success(f"预期结果: {_k}: {_v} !=  实际结果: {actual}, 断言成功！")
                else:
                    logger.error(f"判断关键字: {k} 错误！, 目前仅支持如下关键字：eq, in, gt, lt, not")
                    custom_allure_step(step_title=f'判断关键字: {k} 错误！',
                                       content='目前仅支持如下关键字：eq, in, gt, lt, not')
            except AssertionError:
                logger.error(f"第{index}个响应断言失败 -|- 预期结果: {_k}: {_v}, {type(_v)}   {k}   实际结果: {actual}, {type(actual)}")
                custom_allure_step(
                    step_title=f'第{index}个响应断言失败---->预期结果: {_k}: {_v}, {type(_v)}   {k}   实际结果: {actual}, {type(actual)}')
                logger.info('\n-------------End：响应断言--------------------\n' \
                            "=====================================================")
                raise AssertionError(
                    f"第{index}个响应断言失败 -|- 预期结果: {_k}: {_v}, {type(_v)}   {k}   实际结果: {actual}, {type(actual)}")

    logger.info('\n-------------End：响应断言--------------------\n' \
                "=====================================================")


@allure.step("数据库断言")
def assert_sql(db_info, expected: dict):
    """
    数据库断言
    :param db_info: 数据库配置信息
    :param expected: 预期结果，从excel中或者yaml读取、或者手动传入,格式如下：
    {
    'eq':
        {'sql': 'select count(*) from users where user_id=1;', 'len': '1'},
    'eq':
        {'sql': 'select * from users where user_id=1;', '$.username': '${username}'},
    }
    """
    logger.info("\n======================================================\n" \
                f"-------------Start：数据库断言--------------------")
    if expected is None:
        logger.info("判断是否存在数据库断言---->当前用例无数据库断言")
        custom_allure_step(step_title='判断是否存在数据库断言---->当前用例无数据库断言')
        return
    if not db_info:
        logger.error("判断是否存在数据库配置---->当前环境无数据库配置，跳过数据库断言！")
        custom_allure_step(step_title='判断是否存在数据库配置---->当前环境无数据库配置，跳过数据库断言！')
        logger.info('\n-------------End：数据库断言--------------------\n'
                    "=====================================================")
        return
    for k, v in expected.items():
        sql_result = None
        for _k, _v in v.items():
            if _k == "sql":
                try:
                    # 查询数据库，获取查询结果
                    sql_result = MysqlServer(**db_info).query_one(_v)
                    logger.info(f'数据库响应断言 -|- SQL：{_v} || 查询结果：{sql_result}')
                    custom_allure_step(step_title=f'数据库断言---->SQL：{_v} ',
                                       content=f'查询结果：{sql_result}')
                except Exception as e:
                    logger.error(f'数据库服务报错：{e}')
                    custom_allure_step(step_title=f'数据库服务报错',
                                       content=f'{e} ')
                    logger.info('\n-------------End：数据库断言--------------------\n'
                                "=====================================================")
                    raise AssertionError(f"数据库服务报错：{e}")

            try:
                if k == "eq":  # 预期结果 = 实际结果
                    if _k == "len":
                        assert _v == len(sql_result)
                        logger.success(f"预期结果: {_v} ==  实际结果: {len(sql_result)}, 断言成功！")
                        custom_allure_step(step_title=f'数据库断言结果---->预期结果: {_v} ==  实际结果: {len(sql_result)}, 断言成功！')
                    # 如果时$.开头，则从数据库查询结果中提取相应的值作为实际结果
                    elif _k.startswith("$."):
                        actual = json_extractor(sql_result, _k)
                        assert _v == actual
                        logger.success(f"预期结果: {_v} ==  实际结果: {actual}, 断言成功！")
                        custom_allure_step(step_title=f'数据库断言结果---->预期结果: {_v} ==  实际结果: {actual}, 断言成功！')
            except AssertionError:
                logger.error(f"数据库断言失败 -|- 预期结果:{_v}  {k}   实际结果: {sql_result})")
                custom_allure_step(step_title=f'数据库断言失败---->预期结果:{_v}  {k}   实际结果: {sql_result}')
                logger.info('\n-------------End：数据库断言--------------------\n' \
                            "=====================================================")
                raise AssertionError(f"数据库断言失败 -|-预期结果: {_v}  {k}  实际结果: {sql_result}")

    logger.info('\n-------------End：数据库断言--------------------\n' \
                "=====================================================")
