# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/1/12 15:22
# @Author  : chenyinhua
# @File    : case_handle.py
# @Software: PyCharm
# @Desc: 生成测试用例文件并返回用例数据

import os
from config.project_path import CONF_DIR, DATA_DIR, AUTO_CASE_DIR
from common_utils.excel_handle import ReadExcel
from common_utils.yaml_handle import HandleYaml
from config.global_vars import CaseFileType
from config.settings import CASE_FILE_TYPE
from string import Template
from loguru import logger
from common_utils.files_handle import get_files


def get_case_data():
    """
    根据配置文件，从指定类型文件中读取用例数据，并调用生成用例文件方法，生成用例文件
    """
    cases = []
    # 判断配置文件里面CASE_DATA_TYPE,判断用例数据是从excel还是yaml文件中读取
    # 从excel中读取用例数据
    if CASE_FILE_TYPE == CaseFileType.EXCEL.value:
        # 在用例数据"DATA_DIR"目录中寻找后缀是xlsx, xls的文件
        files = get_files(target=DATA_DIR, start="test_", end=".xlsx") + get_files(target=DATA_DIR, start="test_",
                                                                                   end=".xls")
        for file in files:
            # 这里file文件绝对路径，filename才是文件名称
            filename = os.path.basename(file)
            # 读取excel文件中的用例数据，存储到data中
            data = ReadExcel(file).read()
            # 将用例数据的名称作为测试用例文件名称
            func_name = os.path.splitext(filename)[0]
            # 测试用例test_demo.py的类名是TestDemo
            class_name = func_name.split("_")[0].title() + func_name.split("_")[1].title()
            # 调用gen_case方法生成测试用例test_demo.py
            gen_case_file(func_name, data, class_name)
            # 将excel中读取的用例数据放到cases列表中
            cases.extend(data)
        logger.debug(f"从excel中读取到的用例数据是：{cases}")
        return cases
    # 从yaml中读取用例数据
    elif CASE_FILE_TYPE == CaseFileType.YAML.value:
        # 在用例数据"DATA_DIR"目录中寻找后缀是yaml, yml的文件
        files = get_files(target=DATA_DIR, start="test_", end=".yaml") + get_files(target=DATA_DIR, start="test_",
                                                                                   end=".yml")
        for file in files:
            filename = os.path.basename(file)
            # 读取yaml/yml文件中的用例数据，存储到data中
            data = HandleYaml(file).read_yaml
            # 将用例数据的名称作为测试用例文件名称
            func_name = os.path.splitext(filename)[0]
            # 测试用例test_demo.py的类名是TestDemo
            class_name = func_name.split("_")[0].title() + func_name.split("_")[1].title()
            # 调用gen_case方法生成测试用例test_demo.py
            gen_case_file(func_name, data, class_name)
            # 将excel中读取的用例数据放到cases列表中
            cases.extend(data)
        logger.debug(f"从yaml中读取到的用例数据是：{cases}")
        return cases
    else:
        # 在用例数据"DATA_DIR"目录中寻找后缀是xlsx,xls, yaml, yml的文件
        files = get_files(target=DATA_DIR, start="test_", end=".xlsx") + get_files(target=DATA_DIR, start="test_",
                                                                                   end=".xls") + get_files(
            target=DATA_DIR, start="test_", end=".yaml") + get_files(target=DATA_DIR, start="test_",
                                                                     end=".yml")
        for file in files:
            filename = os.path.basename(file)
            if os.path.splitext(file)[1] == ".xlsx" or os.path.splitext(file)[1] == ".xls":
                data = ReadExcel(file).read()
                func_name = os.path.splitext(filename)[0]
                cases.extend(data)
            else:
                data = HandleYaml(file).read_yaml
                func_name = os.path.splitext(filename)[0]
                cases.extend(data)

            class_name = func_name.split("_")[0].title() + func_name.split("_")[1].title()
            gen_case_file(func_name, data, class_name)
        logger.debug(f"从excel以及yaml中读取到的用例数据是：{cases}")
        return cases


def gen_case_file(func_name, case_data, class_name):
    """
    根据定义的模板生成测试用例文件
    """
    # 如果自动生成用例的目录不存在则自动创建一个
    if not os.path.exists(AUTO_CASE_DIR):
        os.makedirs(AUTO_CASE_DIR)
    """
    string.Template是将一个string设置为模板，通过替换变量的方法，最终得到想要的string。
    """
    # 定义生成的测试用例的模板
    with open(file=os.path.join(CONF_DIR, "case_template.txt"), mode="r", encoding="utf-8") as f:
        case_template = f.read()
    my_case = Template(case_template).safe_substitute({"case_data": case_data,
                                                       "func_title": func_name,
                                                       "class_title": class_name})
    with open(os.path.join(AUTO_CASE_DIR, func_name + '.py'), "w", encoding="utf-8") as fp:
        fp.write(my_case)
