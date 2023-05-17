# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/2/1 14:31
# @Author  : chenyinhua
# @File    : assert_handle.py
# @Software: PyCharm
# @Desc: 断言


from requests import Response
from case_utils.data_handle import json_extractor, re_extract
from loguru import logger
from case_utils.requests_handle import response_type
from case_utils.data_handle import eval_data_process


def assert_result(response: Response, expected: dict) -> None:
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
    if expected is None:
        logger.info("当前用例无断言！")
        return
    logger.info(f"预期结果：{expected}, {type(expected)}")
    index = 0
    for k, v in expected.items():
        # 获取需要断言的实际结果部分
        for _k, _v in v.items():
            if _k == "http_code":
                actual = response.status_code
            else:
                logger.debug("根据响应类型的不同，从响应数据中提取实际结果")
                if response_type(response) == "json":
                    # 如果响应数据是json格式
                    actual = json_extractor(response.json(), _k)
                else:
                    # 响应数据不是json格式
                    actual = re_extract(response.text, _k)
            index += 1
            # 对预期结果进行数据处理
            _v = eval_data_process(_v)
            logger.info(f'第{index}个断言 -|- 预期结果: {_v}, {type(_v)}   {k}   实际结果: {actual},{type(actual)}')
            try:
                if k == "eq":  # 预期结果 = 实际结果
                    assert _v == actual
                    logger.info("断言成功！")
                elif k == "in":  # 实际结果 包含 预期结果
                    assert _v in actual
                    logger.info("断言成功！")
                elif k == "gt":  # 预期结果 > 实际结果 (值应该为数值型)
                    assert actual < _v
                    logger.info("断言成功！")
                elif k == "lt":  # 预期结果 < 实际结果 (值应该为数值型)
                    assert actual > _v
                    logger.info("断言成功！")
                elif k == "not":  # 预期结果 != 实际结果
                    assert actual != _v
                    logger.info("断言成功！")
                else:
                    logger.error(f"判断关键字: {k} 错误！")
            except AssertionError:
                logger.error("断言失败")
                raise AssertionError(f"第{index}个断言 -|- 预期结果: {_v}, {type(_v)}   {k}   实际结果: {actual},{type(actual)}")
