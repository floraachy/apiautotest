# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/2/1 14:16
# @Author  : chenyinhua
# @File    : data_handle.py
# @Software: PyCharm
# @Desc: 数据处理
from jsonpath import jsonpath
import re
from faker import Faker
from string import Template
from loguru import logger

faker = Faker()


def data_replace(content, source):
    """
    用例数据替换的方法
    :param content: 原始的字符串内容
    :param source: 需要替换字符串的来源
    return content： 替换表达式后的字符串
    """
    try:
        if content is None:
            return None
        logger.debug("\n======================================================\n" \
                     "-------------Start：数据替换--------------------\n"
                     f"初始字符串: {content}\n" \
                     "=====================================================")
        print(f"-----Start-----数据替换: 初始字符串为：{content}")
        if len(content) != 0:
            # safe_substitute() 方法会保留没有被替换的占位符，不会抛出 KeyError 异常。
            # 所以，如果 content 中不存在占位符，使用 safe_substitute() 方法进行替换后，得到的结果和原始字符串是一样的。
            content = Template(str(content)).safe_substitute(source)
            for func in re.findall('\\${(.*?)}', content):
                content = content.replace('${%s}' % func, exec_func(func))
                try:
                    content = content.replace('${%s}' % func, exec_func(func))
                except Exception as e:
                    logger.error(f"\n======================================================\n" \
                                 "-------------End：数据替换--------------------\n"
                                 f"替换数据时出现了异常：{e}" \
                                 "=====================================================")
                    print(f"-----END-----替换数据时出现了异常：{e}")
                    return e
            logger.debug("\n======================================================\n" \
                         "-------------End：数据替换--------------------\n"
                         f"新字符串：{content}\n" \
                         "=====================================================")
            print(f"-----End-----数据替换完成: 新字符串为：{type(content)} || {content}\n")
            return content
    except Exception as e:
        logger.error(f"进行数据替换时报错：{e}")
        print(f"进行数据替换时报错：{e}")


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
                     f"提取表达式为： {expr} 提取值为 {result}\n" \
                     "=====================================================")
        print("提取响应内容成功，提取表达式为： {} 提取值为 {}".format(expr, result))
    except Exception as e:
        logger.debug("\n======================================================\n" \
                     "-------------End：json_extractor--------------------\n"
                     f"提取表达式为： {expr} 提取数据为 {obj}\n， 错误信息为：{e}\n" \
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
                     f"提取表达式为： {expr} 提取值为： {result}\n" \
                     "=====================================================")
        print("提取响应内容成功，提取表达式为： {} 提取值为： {}".format(expr, result))
    except Exception as e:
        logger.debug(f"\n======================================================\n" \
                     "-------------End：re_extract--------------------\n"
                     f"提取表达式为： {expr} 提取数据为：{obj}\n， 错误信息为：{e}\n" \
                     "=====================================================")
        print(f'未提取到内容，请检查表达式是否错误！提取表达式为：{expr} 提取数据为 {obj}， 错误信息为：{e}')
        result = None
    return result


def exec_func(func) -> str:
    """
    :params func 字符的形式调用函数
    : return 返回的转换成函数执行的结果,已字符串格式返回
    """
    result = eval(func)
    logger.debug("\n======================================================\n" \
                 "-------------exec_func--------------------\n"
                 f"函数： {func} 执行结果： {result}\n" \
                 "=====================================================")
    return str(result)


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
