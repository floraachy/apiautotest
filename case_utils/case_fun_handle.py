# -*- coding: utf-8 -*-
# @Time    : 2023/6/7 10:07
# @Author  : chenyinhua
# @File    : case_fun_handle.py
# @Software: PyCharm
# @Desc:

import os
from string import Template
import datetime
from xpinyin import Pinyin  # 纯 Python 编写的中文字符串拼音转换模块，不需要依赖外部程序和词库。
from loguru import logger
from common_utils.excel_handle import ExcelHandle
from common_utils.yaml_handle import YamlHandle
from common_utils.files_handle import get_files
from config.models import CaseFileType
from config.settings import CASE_FILE_TYPE
from config.path_config import DATA_DIR, CASE_TEMPLATE_DIR, AUTO_CASE_DIR
from case_utils.case_data_analysis import CaseDataCheck

"""
主要步骤：
1. 从用例数据文件（EXCEL/YAML）中获取用例数据
2. 分析用例数据是否符合规范
3. 确认符合规范后，获取所有用例数据，自动生成测试用例方法（PY）
"""


def generate_case_from_excel(files: list):
    """
    读取excel用例数据生成测试用例
    """
    for file in files:
        # 读取excel文件中的用例数据，存储到data中
        if os.path.isfile(file):
            # 读取xlsx/xls文件中的用例数据，存储到data中
            data = ExcelHandle(file).read()
            # logger.debug(f"从{file}中读取到的用例数据是：{data}")
            for index, v in enumerate(data):
                excel_case = {}
                # 将excel读取到的用例数据，适配allure格式
                """
                表单名称以短横线隔开的情况下，左边部分作为allure_epic， 右边部分作为allure_feature以及allure_story。
                否则，表单名称全部作为allure_epic，allure_feature，allure_story
                """
                if "-" in v["sheet_name"]:
                    excel_case["case_common"] = {
                        "allure_epic": v["sheet_name"].split("-")[0],
                        "allure_feature": v["sheet_name"].split("-")[1],
                        "allure_story": v["sheet_name"].split("-")[1]
                    }
                else:
                    excel_case["case_common"] = {
                        "allure_epic": v["sheet_name"],
                        "allure_feature": v["sheet_name"],
                        "allure_story": v["sheet_name"]
                    }
                # 处理excel用例数据
                for case in v["data"]:
                    excel_case[case["id"]] = case
                # 检查用例数据是否符合规范
                tested_case = CaseDataCheck().case_process(excel_case)
                # 生成测试方法
                """
                由于excel涉及到多个表单，每一个表单都会生成一个测试方法。因此会将表单名称的首字母拼接到测试方法上。
                excel名称：test_demo
                例如表单名称："GitLink-登录模块" 或 "登录模块"，都是取关键字"登录模块"首字母
                测试文件：test_demo_dl.py
                测试方法名称: TestDemoDl.test_demo_dl
                """
                pin_yin = Pinyin()
                _name = pin_yin.get_initials(excel_case["case_common"]["allure_feature"], "").lower()
                gen_case_file(filename=os.path.splitext(os.path.basename(file))[0] + "_" + _name,
                              case_template_path=CASE_TEMPLATE_DIR,
                              case_common=excel_case["case_common"], case_data=tested_case,
                              target_case_path=AUTO_CASE_DIR)
        else:
            logger.error(f"{file}不是一个正确的文件路径！")


def generate_case_from_yaml(files: list):
    """
    读取yaml用例数据生成测试用例
    """
    for file in files:
        # 从yaml/yml中读取用例数据
        if os.path.isfile(file):
            # 读取yaml/yml文件中的用例数据，存储到data中
            yaml_data = YamlHandle(file).read_yaml
            # logger.debug(f"从{file}中读取到的用例数据是：{yaml_data}")
            # 检查用例数据是否符合规范
            tested_case = CaseDataCheck().case_process(yaml_data)
            # 生成测试方法
            gen_case_file(filename=os.path.splitext(os.path.basename(file))[0], case_template_path=CASE_TEMPLATE_DIR,
                          case_common=yaml_data["case_common"], case_data=tested_case,
                          target_case_path=AUTO_CASE_DIR)
        else:
            logger.error(f"{file}不是一个正确的文件路径！")


def generate_cases():
    """
    根据配置文件，从指定类型文件中读取所有用例数据，并自动生成测试用例
    """
    # 判断配置文件里面CASE_DATA_TYPE,判断用例数据是从excel还是yaml文件中读取
    # 从excel中读取用例数据
    if CASE_FILE_TYPE == CaseFileType.EXCEL.value:
        # 在用例数据"DATA_DIR"目录中寻找后缀是xlsx, xls的文件
        files = get_files(target=DATA_DIR, start="test_", end=".xlsx") \
                + get_files(target=DATA_DIR, start="test_", end=".xls")
        # 自动生成测试用例
        generate_case_from_excel(files)
    # 从yaml中读取用例数据
    elif CASE_FILE_TYPE == CaseFileType.YAML.value:
        # 在用例数据"DATA_DIR"目录中寻找后缀是yaml, yml的文件
        files = get_files(target=DATA_DIR, start="test_", end=".yaml") \
                + get_files(target=DATA_DIR, start="test_", end=".yml")
        # 自动生成测试用例
        generate_case_from_yaml(files)
    else:
        # 在用例数据"DATA_DIR"目录中寻找后缀是xlsx,xls, yaml, yml的文件
        excel_files = get_files(target=DATA_DIR, start="test_", end=".xlsx") \
                      + get_files(target=DATA_DIR, start="test_", end=".xls")
        yaml_files = get_files(target=DATA_DIR, start="test_", end=".yaml") \
                     + get_files(target=DATA_DIR, start="test_", end=".yml")
        # 自动生成测试用例
        generate_case_from_excel(excel_files)
        generate_case_from_yaml(yaml_files)


def gen_case_file(filename, case_template_path, case_common, case_data, target_case_path):
    """
    根据测试用例文件(yaml/yml/xlsx/xls)，以及事先定义的测试用例模板，实际用例数据，生成测试用例方法(.py)
    :param filename: 测试用例文件(yaml/yml/xlsx/xls)的名称，用作生成测试用例类名，方法名
    :param case_template_path: 测试用例模板的绝对路径
    :param case_common: 用例公共参数
    :param case_data: 实际用例数据
    :param target_case_path: 测试用例方法(.py)的绝对路径
    """
    # 如果自动生成用例的目录不存在则自动创建一个
    if not os.path.exists(AUTO_CASE_DIR):
        os.makedirs(AUTO_CASE_DIR)
    """
    string.Template是将一个string设置为模板，通过替换变量的方法，最终得到想要的string。
    """
    # 将用例数据的名称作为测试用例文件名称, 如test_login_demo
    func_name = filename
    # 方法名test_demo的类名是TestDemo
    class_name = "".join([word.capitalize() for word in func_name.split("_")])
    # 定义生成的测试用例的模板
    with open(file=case_template_path, mode="r", encoding="utf-8") as f:
        case_template = f.read()
    # 根据模板，生成测试用例方法
    my_case = Template(case_template).safe_substitute({"allure_epic": case_common["allure_epic"],
                                                       "allure_feature": case_common["allure_feature"],
                                                       "allure_story": case_common["allure_story"],
                                                       "case_data": case_data,
                                                       "func_title": func_name,
                                                       "class_title": class_name,
                                                       "now": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
    # 将测试用例方法写入py文件中
    with open(os.path.join(target_case_path, func_name + '.py'), "w", encoding="utf-8") as fp:
        fp.write(my_case)
