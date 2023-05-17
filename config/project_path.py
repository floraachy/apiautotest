# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/1/31 17:27
# @Author  : chenyinhua
# @File    : project_path.py
# @Software: PyCharm
# @Desc: 项目相关路径
import os

# ------------------------------------ 项目路径 ----------------------------------------------------#
# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 通用模块目录
COMMON_DIR = os.path.join(BASE_DIR, "common_utils")

# 配置模块目录
CONF_DIR = os.path.join(BASE_DIR, "config")

# 数据模块目录
DATA_DIR = os.path.join(BASE_DIR, "data")

# 日志/报告保存目录
OUT_DIR = os.path.join(BASE_DIR, "outputs")
if not os.path.exists(OUT_DIR):
    os.mkdir(OUT_DIR)

# 报告保存目录
REPORT_DIR = os.path.join(OUT_DIR, "report")
if not os.path.exists(REPORT_DIR):
    os.mkdir(REPORT_DIR)

# 报日志保存目录
LOG_DIR = os.path.join(OUT_DIR, "log")
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

# 测试用例模块
CASE_DIR = os.path.join(BASE_DIR, "test_case")

# 手动生成测试用例模块
MANUAL_CASE_DIR = os.path.join(CASE_DIR, "test_manual_case")
if not os.path.exists(MANUAL_CASE_DIR):
    os.mkdir(MANUAL_CASE_DIR)

# 自动生成测试用例模块
AUTO_CASE_DIR = os.path.join(CASE_DIR, "test_auto_case")

