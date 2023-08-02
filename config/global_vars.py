# -*- coding: utf-8 -*-
# @Time    : 2023/5/25 14:52
# @Author  : chenyinhua
# @File    : global_vars.py
# @Software: PyCharm
# @Desc:

# 定义一个全局变量，用于存储运行过程中相关数据
GLOBAL_VARS = {}

# 定义一个变量。存储自定义的标记markers
CUSTOM_MARKERS = []

ENV_VARS = {
    "common": {
        "报告标题": "自动化测试报告",
        "项目名称": "GitLink 确实开源",
        "测试人": "陈银花",
        "所属部门": "开源中心"
    },
    "test": {
        # 示例测试环境及示例测试账号
        "host": "https://testforgeplus.trustie.net/",
        "glcc_host": "https://testglcc.trustie.net",
        "login": "auotest",
        "password": "12345678",
        "nickname": "AutoTest",
        "user_id": "84954",
        "project_id": "",
        "project": ""

    },
    "live": {
        "host": "https://www.gitlink.org.cn",
        "glcc_host": "https://glcc.gitlink.org.cn",
        "login": "******",
        "password": "******",
        "nickname": "******",
        "user_id": "******",
        "project_id": "",
        "project": ""
    }
}
