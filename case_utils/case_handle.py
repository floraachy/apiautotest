# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/1/12 15:22
# @Author  : chenyinhua
# @File    : case_handle.py
# @Software: PyCharm
# @Desc: 生成测试用例文件并返回用例数据

import os
from config.project_path import CASE_TEMPLATE_DIR, DATA_DIR, AUTO_CASE_DIR
from common_utils.excel_handle import ExcelHandle
from common_utils.yaml_handle import YamlHandle
from config.global_vars import CaseFileType
from config.settings import CASE_FILE_TYPE
from string import Template
from loguru import logger
from common_utils.files_handle import get_files


def get_yaml_data(file_path):
    """
    从yaml/yml文件中获取用例数据
    :param file_path: yaml/yml文件绝对路径
    """
    if os.path.isfile(file_path):
        # 读取yaml/yml文件中的用例数据，存储到data中
        return YamlHandle(file_path).read_yaml


def get_excel_data(file_path):
    """
    从xlsx/xls文件中获取用例数据
    :param file_path: xlsx/xls文件绝对路径
    """
    if os.path.isfile(file_path):
        # 读取xlsx/xls文件中的用例数据，存储到data中
        return ExcelHandle(file_path).read()


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
            # 读取excel文件中的用例数据，存储到data中
            data = ExcelHandle(file).read()
            for _data in data:
                # 将excel读取到的用例数据，适配allure格式
                excel_data = {
                    'case_common': {'allure_epic': 'GitLink接口', 'allure_feature': _data["sheet_name"],
                                    'allure_story': _data["sheet_name"]},
                    'case_info': _data["data"]
                }
                # 调用gen_case方法生成测试用例, 例如：test_demo.py
                gen_case_file(case_file_path=file, case_template_path=CASE_TEMPLATE_DIR, case_data=excel_data,
                              target_case_path=AUTO_CASE_DIR)
                # 将获取到的用例数据统一保存到cases中
                cases.extend([excel_data])
                logger.debug(f"从{file}中读取到的用例数据是：{excel_data}")
        return cases
    # 从yaml中读取用例数据
    elif CASE_FILE_TYPE == CaseFileType.YAML.value:
        # 在用例数据"DATA_DIR"目录中寻找后缀是yaml, yml的文件
        files = get_files(target=DATA_DIR, start="test_", end=".yaml") + get_files(target=DATA_DIR, start="test_",
                                                                                   end=".yml")
        for file in files:
            # 从yaml/yml中读取用例数据
            yaml_data = get_yaml_data(file)
            # 调用gen_case方法生成测试用例, 例如：test_demo.py
            gen_case_file(case_file_path=file, case_template_path=CASE_TEMPLATE_DIR, case_data=yaml_data,
                          target_case_path=AUTO_CASE_DIR)
            # 将获取到的用例数据统一保存到cases中
            cases.extend([yaml_data])
            logger.debug(f"从{file}中读取到的用例数据是：{yaml_data}")
        return cases
    else:
        # 在用例数据"DATA_DIR"目录中寻找后缀是xlsx,xls, yaml, yml的文件
        files = get_files(target=DATA_DIR, start="test_", end=".xlsx") + get_files(target=DATA_DIR, start="test_",
                                                                                   end=".xls") + get_files(
            target=DATA_DIR, start="test_", end=".yaml") + get_files(target=DATA_DIR, start="test_",
                                                                     end=".yml")
        for file in files:
            if os.path.splitext(file)[1] == ".xlsx" or os.path.splitext(file)[1] == ".xls":
                # 读取excel文件中的用例数据，存储到data中
                data = ExcelHandle(file).read()
                for _data in data:
                    # 将excel读取到的用例数据，适配allure格式
                    excel_data = {
                        'case_common': {'allure_epic': 'GitLink接口', 'allure_feature': _data["sheet_name"],
                                        'allure_story': _data["sheet_name"]},
                        'case_info': _data["data"]
                    }
                    # 调用gen_case方法生成测试用例, 例如：test_demo.py
                    gen_case_file(case_file_path=file, case_template_path=CASE_TEMPLATE_DIR, case_data=excel_data,
                                  target_case_path=AUTO_CASE_DIR)
                    # 将获取到的用例数据统一保存到cases中
                    cases.extend([excel_data])
                    logger.debug(f"从{file}中读取到的用例数据是：{excel_data}")
            else:
                # 从yaml/yml中读取用例数据
                yaml_data = get_yaml_data(file)
                # 调用gen_case方法生成测试用例, 例如：test_demo.py
                gen_case_file(case_file_path=file, case_template_path=CASE_TEMPLATE_DIR, case_data=yaml_data,
                              target_case_path=AUTO_CASE_DIR)
                # 将获取到的用例数据统一保存到cases中
                cases.extend([yaml_data])
        return cases


def gen_case_file(case_file_path, case_template_path, case_data, target_case_path):
    """
    根据测试用例文件(yaml/yml/xlsx/xls)，以及事先定义的测试用例模板，实际用例数据，生成测试用例方法(.py)
    :param case_file_path: 测试用例文件(yaml/yml/xlsx/xls)的绝对路径
    :param case_template_path: 测试用例模板的绝对路径
    :param case_data: 实际用例数据
    :param target_case_path: 测试用例方法(.py)的绝对路径
    """
    # 如果自动生成用例的目录不存在则自动创建一个
    if not os.path.exists(AUTO_CASE_DIR):
        os.makedirs(AUTO_CASE_DIR)
    """
    string.Template是将一个string设置为模板，通过替换变量的方法，最终得到想要的string。
    """
    filename = os.path.basename(case_file_path)
    # 将用例数据的名称作为测试用例文件名称
    func_name = os.path.splitext(filename)[0]
    # 测试用例test_demo.py的类名是TestDemo
    class_name = func_name.split("_")[0].title() + func_name.split("_")[1].title()
    # 定义生成的测试用例的模板
    with open(file=case_template_path, mode="r", encoding="utf-8") as f:
        case_template = f.read()
    # 根据模板，生成测试用例方法
    my_case = Template(case_template).safe_substitute({"case_data": case_data,
                                                       "func_title": func_name,
                                                       "class_title": class_name})
    # 将测试用例方法写入py文件中
    with open(os.path.join(target_case_path, func_name + '.py'), "w", encoding="utf-8") as fp:
        fp.write(my_case)
