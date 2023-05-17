# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/1/9 16:41
# @Author  : chenyinhua
# @File    : handle_eval_data.py
# @Software: PyCharm
# @Desc: 将内容eval一下

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
        return eval_data(data)
    # 如果目标数据是列表，遍历列表的每一个数据，再用递归的方法处理每一个item
    elif isinstance(data, list):
        for index, item in enumerate(data):
            data[index] = eval_data_process(eval_data(item))
    # 如果目标数据是字典，遍历字典的每一个值，再用递归的方法处理每一个value
    elif isinstance(data, dict):
        for key, value in data.items():
            data[key] = eval_data_process(eval_data(value))
    return data
