# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/1/9 17:08
# @Author  : chenyinhua
# @File    : settings.py
# @Software: PyCharm
# @Desc: 项目配置文件


# 0代表执行Excel和yaml两种格式的用例， 1 代表 yaml文件，2 用例代表Excel用例
CASE_FILE_TYPE = 0
# 测试报告的定制化信息展示
REPORT_TITLE = "自动化测试报告"
REPORT_NAME = f"apiautotest-report-"
PROJECT_NAME = "GitLink 确实开源"
TESTER = "测试人员：陈银花"
DEPARTMENT = "所属部门: 开源中心"

# 指定日志收集级别
LOG_LEVEL = "INFO"

# 测试数据
test = [
    {
        # 示例测试环境及示例测试账号
        "host": "https://testforgeplus.trustie.net/",
        "login": "auotest",
        "password": "12345678",
        "nickname": "AutoTest",
        "user_id": "84954",
        "project_id": "",
        "project": ""

    }
]
live = [
    {
        "host": "https://www.gitlink.org.cn",
        "login": "******",
        "password": "******",
        "nickname": "******",
        "user_id": "******",
        "project_id": "",
        "project": ""
    }
]
