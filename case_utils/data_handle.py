# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/2/1 14:16
# @Author  : chenyinhua
# @File    : data_handle.py
# @Software: PyCharm
# @Desc: 数据处理

import re
from string import Template
from jsonpath import jsonpath
from loguru import logger
from faker import Faker

faker = Faker()


def data_handle(obj, source):
    """
    递归处理字典、列表中的字符串，将${}占位符替换成source中的值
    """
    obj = eval_data_process(obj)
    if isinstance(obj, str):
        # 寻找${}， 在source中找到对应的关键字进行替换，如obj=${user_id}, 去寻找source中对应键user_id的值（假设user_id=1），使得obj=1
        obj = Template(obj).safe_substitute(source)
        # 寻找${python表达式}， 将Python表达式eval得出其具体值
        for func in re.findall('\\${(.*?)}', obj):
            obj = obj.replace('${%s}' % func, eval_data_process(func))
            obj = eval_data_process(obj)
            return obj
        return eval_data_process(obj)
    elif isinstance(obj, list):
        for index, item in enumerate(obj):
            obj[index] = data_handle(item, source)
        return obj

    elif isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = data_handle(value, source)
        return obj

    else:
        return obj


# 将"[1,2,3]" 或者"{'k':'v'}" -> [1,2,3], {'k':'v'}
def eval_data(data):
    """
    执行一个字符串表达式，并返回其表达式的值
    """
    try:
        if hasattr(eval(data), "__call__"):
            return data
        else:
            return eval(data)
    except Exception:
        return data


def eval_data_process(data):
    """
    将数据中的字符串表达式处理后更新其值为表达式
    """
    # 如果目标数据是字符串，直接尝试eval
    if isinstance(data, str):
        data = eval_data(data)
    # 如果目标数据是列表，遍历列表的每一个数据，再用递归的方法处理每一个item
    if isinstance(data, list):
        for index, item in enumerate(data):
            data[index] = eval_data_process(eval_data(item))
    # 如果目标数据是字典，遍历字典的每一个值，再用递归的方法处理每一个value
    elif isinstance(data, dict):
        for key, value in data.items():
            data[key] = eval_data_process(eval_data(value))
    return data


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
