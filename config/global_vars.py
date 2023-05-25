# -*- coding: utf-8 -*-
# @Time    : 2023/5/25 14:52
# @Author  : chenyinhua
# @File    : global_vars.py
# @Software: PyCharm
# @Desc:
# 定义一个全局变量，用于存储运行过程中相关数据
GLOBAL_VARS = {}

ENV_VARS = {
    "common": {
        "report_title": "自动化测试报告",
        "project_name": "GitLink 确实开源",
        "tester": "陈银花",
        "department": "开源中心"
    },
    "test": {
        # 示例测试环境及示例测试账号
        "host": "https://testforgeplus.trustie.net/",
        "login": "auotest",
        "password": "12345678",
        "nickname": "AutoTest",
        "user_id": "84954",
        "project_id": "",
        "project": ""

    },
    "live": {
        "host": "https://www.gitlink.org.cn",
        "login": "******",
        "password": "******",
        "nickname": "******",
        "user_id": "******",
        "project_id": "",
        "project": ""
    }
}
