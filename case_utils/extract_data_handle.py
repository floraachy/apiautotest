# -*- coding: utf-8 -*-
# @Time    : 2023/6/28 14:35
# @Author  : chenyinhua
# @File    : extract_data_handle.py
# @Software: PyCharm
# @Desc: 提取数据的一些方法

# 标准库导入
import re
# 第三方库导入
from jsonpath import jsonpath
from loguru import logger


def json_extractor(obj: dict, expr: str = '.'):
    """
    :param obj :json/dict类型数据
    :param expr: 表达式, . 提取字典所有内容， $.test_api_case 提取一级字典case， $.test_api_case.data 提取case字典下的data
    :return result: 提取的结果，未提取到返回 None
    """
    try:
        result = jsonpath(obj, expr)[0]
        logger.debug("\n======================================================\n" \
                     "-------------Start：json_extractor--------------------\n"
                     f"提取表达式为： {expr} \n"
                     f"提取值为： {result}\n"
                     "=====================================================")
        print("提取响应内容成功，提取表达式为： {} 提取值为 {}".format(expr, result))
    except Exception as e:
        logger.debug("\n======================================================\n" \
                     "-------------End：json_extractor--------------------\n"
                     f"提取表达式为： {expr}\n"
                     f"提取数据为： {obj}\n"
                     f"错误信息为：{e}\n"
                     "=====================================================")
        print(f'未提取到内容，请检查表达式是否错误！提取表达式为：{expr} 提取数据为 {obj}， 错误信息为：{e}')
        result = None
    return result


def re_extract(obj: str, expr: str = '.'):
    """
    :param obj : 字符串数据
    :param expr: 正则表达式
    :return result: 提取的结果，未提取到返回 None
    """
    try:
        result = re.findall(expr, obj)[0]
        logger.debug("\n======================================================\n" \
                     "-------------Start：re_extract--------------------\n"
                     f"提取表达式为： {expr}\n" \
                     f"提取值为： {result}\n" \
                     "=====================================================")
        print("提取响应内容成功，提取表达式为： {} 提取值为： {}".format(expr, result))
    except Exception as e:
        logger.debug(f"\n======================================================\n" \
                     "-------------End：re_extract--------------------\n"
                     f"提取表达式为： {expr}\n" \
                     f"提取数据为： {obj}\n" \
                     f"错误信息为：{e}\n" \
                     "=====================================================")
        print(f'未提取到内容，请检查表达式是否错误！提取表达式为：{expr} 提取数据为 {obj}， 错误信息为：{e}')
        result = None
    return result
