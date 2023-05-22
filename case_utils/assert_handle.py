# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/2/1 14:31
# @Author  : chenyinhua
# @File    : assert_handle.py
# @Software: PyCharm
# @Desc: 断言

from case_utils.allure_handle import allure_step
from requests import Response
from common_utils.data_handle import json_extractor, re_extract
from loguru import logger
from case_utils.request_data_handle import response_type
from common_utils.mysql_handle import MysqlServer
from config.settings import db_info


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
        logger.info("当前用例无响应断言！")
        allure_step(step_title='判断是否存在响应断言',
                    content='当前用例无响应断言！')
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
            allure_step(step_title=f'第{index}个响应断言数据',
                        content=f'预期结果: {_k}: {_v}, {type(_v)}   {k}   实际结果: {actual}, {type(actual)}')
            try:
                if k == "eq":  # 预期结果 = 实际结果
                    assert _v == actual
                    logger.debug(f"预期结果: {_k}: {_v} ==  实际结果: {actual}, 断言成功！")
                elif k == "in":  # 实际结果 包含 预期结果
                    assert _v in actual
                    logger.debug(f"预期结果: {_k}: {_v} in  实际结果: {actual}, 断言成功！")
                elif k == "gt":  # 预期结果 > 实际结果 (值应该为数值型)
                    assert _v > actual
                    logger.debug(f"预期结果: {_k}: {_v} >  实际结果: {actual}, 断言成功！")
                elif k == "lt":  # 预期结果 < 实际结果 (值应该为数值型)
                    assert _v < actual
                    logger.debug(f"预期结果: {_k}: {_v} <  实际结果: {actual}, 断言成功！")
                elif k == "not":  # 预期结果 != 实际结果
                    assert _v != actual
                    logger.debug(f"预期结果: {_k}: {_v} !=  实际结果: {actual}, 断言成功！")
                else:
                    logger.error(f"判断关键字: {k} 错误！, 目前仅支持如下关键字：eq, in, gt, lt, not")
                    allure_step(step_title=f'判断关键字: {k} 错误！',
                                content='目前仅支持如下关键字：eq, in, gt, lt, not')
            except AssertionError:
                logger.error(f"第{index}个响应断言失败 -|- 预期结果: {_k}: {_v}, {type(_v)}   {k}   实际结果: {actual}, {type(actual)}")
                allure_step(step_title=f'第{index}个响应断言失败',
                            content=f'预期结果: {_k}: {_v}, {type(_v)}   {k}   实际结果: {actual}, {type(actual)}')
                logger.info('\n-------------End：响应断言--------------------\n' \
                            "=====================================================")
                raise AssertionError(
                    f"第{index}个响应断言失败 -|- 预期结果: {_k}: {_v}, {type(_v)}   {k}   实际结果: {actual}, {type(actual)}")

    logger.info('\n-------------End：响应断言--------------------\n' \
                "=====================================================")


def assert_sql(env, expected: dict):
    """
    数据库断言
    :param env: 当前所处环境
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
        logger.info("当前用例无数据库断言！")
        allure_step(step_title='判断是否存在数据库断言',
                    content='当前用例无数据库断言')
        return
    try:
        # 拿不到数据库配置，则不进行数据库断言
        db = db_info["test" if env.lower() == "test" else "live"]
        db_host = db["db_host"]
    except KeyError:
        logger.error("当前环境无数据库配置，跳过数据库断言！")
        allure_step(step_title='判断是否存在数据库配置',
                    content='当前环境无数据库配置，跳过数据库断言！}')
        logger.info('\n-------------End：数据库断言--------------------\n' \
                    "=====================================================")
        return
    for k, v in expected.items():
        sql_result = None
        for _k, _v in v.items():
            if _k == "sql":
                try:
                    # 查询数据库，获取查询结果
                    sql_result = MysqlServer(**db).query_one(_v)
                    logger.info(f'数据库响应断言 -|- SQL：{_v} || 查询结果：{sql_result}')
                    allure_step(step_title=f'数据库断言',
                                content=f'SQL：{_v} || 查询结果：{sql_result}')
                except Exception as e:
                    logger.error(f'数据库服务报错：{e}')
                    allure_step(step_title=f'数据库服务报错',
                                content=f'{e} ')
                    logger.info('\n-------------End：数据库断言--------------------\n' \
                                "=====================================================")
                    raise AssertionError(f"数据库服务报错：{e}")

            try:
                if k == "eq":  # 预期结果 = 实际结果
                    if _k == "len":
                        assert _v == len(sql_result)
                        logger.info(f"预期结果: {_v} ==  实际结果: {len(sql_result)}, 断言成功！")
                        allure_step(step_title=f'---->数据库断言结果',
                                    content=f'预期结果: {_v} ==  实际结果: {len(sql_result)}, 断言成功！')
                    # 如果时$.开头，则从数据库查询结果中提取相应的值作为实际结果
                    elif _k.startswith("$."):
                        actual = json_extractor(sql_result, _k)
                        assert _v == actual
                        logger.info(f"预期结果: {_v} ==  实际结果: {actual}, 断言成功！")
                        allure_step(step_title=f'---->数据库断言结果',
                                    content=f'预期结果: {_v} ==  实际结果: {actual}, 断言成功！')
            except AssertionError:
                logger.error(f"数据库断言失败 -|- 预期结果:{_v}  {k}   实际结果: {sql_result})")
                allure_step(step_title=f'数据库断言失败',
                            content=f'预期结果:{_v}  {k}   实际结果: {sql_result}')
                logger.info('\n-------------End：数据库断言--------------------\n' \
                            "=====================================================")
                raise AssertionError(f"数据库断言失败 -|-预期结果: {_v}  {k}  实际结果: {sql_result}")

    logger.info('\n-------------End：数据库断言--------------------\n' \
                "=====================================================")
