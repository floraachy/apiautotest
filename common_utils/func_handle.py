# -*- coding: utf-8 -*-
# @Time    : 2023/4/6 11:36
# @Author  : Flora.Chen
# @File    : helper.py
# @Software: PyCharm
# @Desc:

def add_docstring(docstring):
    """
    函数装饰器，它接受一个字符串参数docstring，
    并返回一个装饰器函数。装饰器函数接受一个函数参数func，
    并将func的__doc__属性设置为docstring。
    """
    def decorator(func):
        func.__doc__ = docstring
        return func

    return decorator