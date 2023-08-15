# -*- coding: utf-8 -*-
# @Time    : 2023/6/7 10:07
# @Author  : chenyinhua
# @File    : case_fun_handle.py
# @Software: PyCharm
# @Desc:
# 标准库导入
import os
from string import Template
import datetime
import re
# 第三方库导入
from xpinyin import Pinyin  # 纯 Python 编写的中文字符串拼音转换模块，不需要依赖外部程序和词库。
from loguru import logger
# 本地应用/模块导入
from common_utils.excel_handle import ExcelHandle
from common_utils.yaml_handle import YamlHandle
from common_utils.files_handle import get_files, get_relative_path
from config.models import CaseFileType
from config.settings import CASE_FILE_TYPE
from config.path_config import DATA_DIR, CASE_TEMPLATE_DIR, AUTO_CASE_DIR
from config.global_vars import CUSTOM_MARKERS
from case_utils.case_data_analysis import CaseDataCheck

"""
主要步骤：
1. 从用例数据文件（EXCEL/YAML）中获取用例数据
2. 分析用例数据是否符合规范
3. 确认符合规范后，获取所有用例数据，自动生成测试用例方法（PY）
"""


def handle_excel_data(file):
    """
    读取excel用例数据生成测试用例
    """
    if os.path.isfile(file):
        # 读取excel文件中的用例数据，存储到data中
        data = ExcelHandle(file).read()
        for index, v in enumerate(data):
            excel_case = {}
            """
            将excel读取到的用例数据，适配allure格式
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
            excel_case["case_info"] = v["data"]
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
            if os.path.samefile(DATA_DIR, os.path.dirname(file)):
                # 用例文件的直接父级目录是DATA_DIR，则直接在AUTO_CASE_DIR下生成测试用例方法
                gen_case_file(
                    filename=os.path.splitext(os.path.basename(file))[0] + "_" + _name,
                    case_template_path=CASE_TEMPLATE_DIR,
                    case_common=excel_case["case_common"],
                    case_data=tested_case,
                    target_case_path=AUTO_CASE_DIR
                )
            else:
                # 用例文件的直接父级目录不是DATA_DIR， 则保留其直接父级目录，再在AUTO_CASE_DIR下生成测试用例方法
                gen_case_file(
                    filename=os.path.splitext(os.path.basename(file))[0] + "_" + _name,
                    case_template_path=CASE_TEMPLATE_DIR,
                    case_common=excel_case["case_common"],
                    case_data=tested_case,
                    target_case_path=os.path.join(AUTO_CASE_DIR,
                                                  get_relative_path(file_path=file, directory_path=DATA_DIR))
                )
        return True
    else:
        logger.error(f"{file}不是一个正确的文件路径！")
        return False


def handle_yaml_data(file):
    """
    读取yaml用例数据生成测试用例
    """
    if os.path.isfile(file):
        # 读取yaml/yml文件中的用例数据，存储到data中
        yaml_data = YamlHandle(file).read_yaml
        # 检查用例数据是否符合规范
        tested_case = CaseDataCheck().case_process(yaml_data)
        if os.path.samefile(DATA_DIR, os.path.dirname(file)):
            gen_case_file(
                # 用例文件的直接父级目录是DATA_DIR，则直接在AUTO_CASE_DIR下生成测试用例方法
                filename=os.path.splitext(os.path.basename(file))[0],
                case_template_path=CASE_TEMPLATE_DIR,
                case_common=yaml_data["case_common"],
                case_data=tested_case,
                target_case_path=AUTO_CASE_DIR
            )
        else:
            # 用例文件的直接父级目录不是DATA_DIR， 则保留其直接父级目录，再在AUTO_CASE_DIR下生成测试用例方法
            os.makedirs(os.path.dirname(file), exist_ok=True)
            gen_case_file(
                filename=os.path.splitext(os.path.basename(file))[0],
                case_template_path=CASE_TEMPLATE_DIR,
                case_common=yaml_data["case_common"],
                case_data=tested_case,
                target_case_path=os.path.join(AUTO_CASE_DIR,
                                              get_relative_path(file_path=file, directory_path=DATA_DIR))
            )
        return True
    else:
        logger.error(f"{file}不是一个正确的文件路径！")
        return False


def generate_cases():
    """
    根据配置文件，从指定类型文件中读取所有用例数据，并自动生成测试用例
    """
    excel_files = []
    yaml_files = []
    if CASE_FILE_TYPE == CaseFileType.EXCEL.value:
        # 在用例数据"DATA_DIR"目录中寻找后缀是xlsx, xls的文件
        excel_files = get_files(target=DATA_DIR, start="test_", end=".xlsx") \
                      + get_files(target=DATA_DIR, start="test_", end=".xls")
    elif CASE_FILE_TYPE == CaseFileType.YAML.value:
        # 在用例数据"DATA_DIR"目录中寻找后缀是yaml, yml的文件
        yaml_files = get_files(target=DATA_DIR, start="test_", end=".yaml") \
                     + get_files(target=DATA_DIR, start="test_", end=".yml")
    elif CASE_FILE_TYPE == CaseFileType.ALL.value:
        # 在用例数据"DATA_DIR"目录中寻找后缀是xlsx,xls, yaml, yml的文件
        excel_files = get_files(target=DATA_DIR, start="test_", end=".xlsx") + get_files(target=DATA_DIR, start="test_",
                                                                                         end=".xls")
        yaml_files = get_files(target=DATA_DIR, start="test_", end=".yaml") + get_files(target=DATA_DIR, start="test_",
                                                                                        end=".yml")
    else:
        logger.error(f"{CASE_FILE_TYPE}不在CaseFileType内，不能自动生成用例！")
    # 自动生成测试用例
    for file in excel_files:
        handle_excel_data(file=file)
    for file in yaml_files:
        handle_yaml_data(file=file)


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
    if not os.path.exists(target_case_path):
        """
        exist_ok=True 是一个可选参数，用于指定在目录已经存在的情况下是否忽略错误。
        如果设置为 True，则不论目录是否已存在，os.makedirs 都不会报错；如果设置为 False（默认值），则在目录已存在时会引发 FileExistsError 异常。
        """
        os.makedirs(target_case_path, exist_ok=True)
    # 获取用例数据中的标记
    case_markers = case_common.get("case_markers", []) or []
    logger.debug(f"从用例中拿到的标记有：{case_markers}， {type(case_markers)}")
    # 先读取用例模板中每一行的内容
    with open(file=case_template_path, mode="r", encoding="utf-8") as f:
        case_template = f.readlines()
    current_case_template = []
    for line_num, content in enumerate(case_template):
        current_case_template.append(content)
        # 这里是预计往 @pytest.mark.parametrize( 这一行的上面插入标记
        if content.strip().startswith('@pytest.mark.parametrize('):
            # 往测试用例模板中插入自定义标记
            logger.debug(f"获取到的case_markers：{case_markers}， {type(case_markers)}")
            for case_marker in case_markers:
                # 获取符合要求格式的自定义标记名称，并插入到测试模板中
                marker = is_valid_marker(case_marker)
                if marker and isinstance(marker, str):
                    # ！！ 注意这里的4个空格，必须要有4个空格！！
                    current_case_template.append(f"    @pytest.mark.{marker}\n")
                if marker and isinstance(marker, dict):
                    for k, v in marker.items():
                        # ！！ 注意这里的4个空格，必须要有4个空格！！
                        current_case_template.append(f"    @pytest.mark.{k}('{v}')\n")
    # 将用例数据的名称作为测试用例文件名称, 如test_login_demo
    func_name = filename
    # 方法名test_demo的类名是TestDemo
    class_name = "".join([word.capitalize() for word in func_name.split("_")])
    # 根据模板，生成测试用例方法
    """
    string.Template是将一个string设置为模板，通过替换变量的方法，最终得到想要的string。
    """
    current_template = ''.join(current_case_template)
    my_case = Template(current_template).safe_substitute(
        {
            "allure_epic": case_common["allure_epic"],
            "allure_feature": case_common["allure_feature"],
            "allure_story": case_common["allure_story"],
            "case_markers": case_markers,
            "case_data": case_data,
            "func_title": func_name,
            "class_title": class_name,
            "now": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    )

    # 将测试用例方法写入py文件中
    with open(os.path.join(target_case_path, func_name + '.py'), "w", encoding="utf-8") as fp:
        fp.write(my_case)


def is_valid_marker(markers):
    """
    检查标记名称是否合法：仅支持非数字/下划线开头，由数字，字母，下划线组成的标记名称
    """
    pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
    if isinstance(markers, str):
        if re.match(pattern, markers):
            # 将自定义标记放到CUSTOM_MARKERS， 方便后续统一注册
            if markers not in ("skip", "skipif", "parametrize", "usefixtures", "xfail", "filterwarings"):
                CUSTOM_MARKERS.append(markers)
            # 返回合法有效的标记名称，用于添加到测试方法中
            return markers
        else:
            logger.error(f"{markers} 格式不合法， 建议仅输入数字，字母，下划线组合，且不能以数字，下划线开头")
            return False
    elif isinstance(markers, dict):
        if len(markers) == 1:
            marker_name = list(markers.keys())[0]
            if re.match(pattern, marker_name):
                # 将自定义标记放到CUSTOM_MARKERS， 方便后续统一注册
                if marker_name not in ("skip", "skipif", "parametrize", "usefixtures", "xfail", "filterwarings"):
                    CUSTOM_MARKERS.append(markers)
                return markers
            else:
                logger.error(f"{markers} 格式不合法， 建议仅输入数字，字母，下划线组合，且不能以数字，下划线开头")
                return None
        else:
            logger.error(f"{markers} 格式不合法， 只能存在一对键值对")
            return None

    else:
        logger.error(f"{markers} 仅支持字符串或者字典格式")
        return None
