# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/1/9 17:08
# @Author  : chenyinhua
# @File    : settings.py
# @Software: PyCharm
# @Desc: 项目配置文件

# ------------------------------------ 配置信息 ----------------------------------------------------#
# 0代表执行Excel和yaml两种格式的用例， 1 代表 yaml文件，2 用例代表Excel用例
CASE_FILE_TYPE = 0

# 0表示默认不发送任何通知， 1代表钉钉通知，2代表企业微信通知， 3代表邮件通知， 4代表所有途径都发送通知
SEND_RESULT_TYPE = 3

# 测试报告的定制化信息展示
REPORT_TITLE = "自动化测试报告"
REPORT_NAME = f"apiautotest-report-"
PROJECT_NAME = "GitLink 确实开源"
TESTER = "测试人员：陈银花"
DEPARTMENT = "所属部门: 开源中心"

# 指定日志收集级别
LOG_LEVEL = "INFO"

# ------------------------------------ 测试数据 ----------------------------------------------------#
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

# ------------------------------------ 邮件配置信息 ----------------------------------------------------#

# 发送邮件的相关配置信息
email = {
    "user": "******",  # 发件人邮箱
    "password": "******",  # 发件人邮箱授权码
    "host": "smtp.qq.com",
    "to": ["******", "******"]  # 收件人邮箱
}

# ------------------------------------ 钉钉相关配置 ----------------------------------------------------#
ding_talk = {
    "webhook_url": "https://oapi.dingtalk.com/robot/send?access_token=***********",
    "secret": "***********"
}

# ------------------------------------ 企业微信相关配置 ----------------------------------------------------#
wechat = {
    "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=********",
}

# ------------------------------------ 数据库相关配置 ----------------------------------------------------#
db_info = {
    "test": {
         "db_host": "xx.xx.xx.xx",
        "db_port": 3306,
        "db_user": "root",
        "db_pwd": "**********",
        "db_database": "test**********",
        "ssh": True,
        "ssh_host": "xx.xx.xx.xx",
        "ssh_port": 3306,
        "ssh_user": "root",
        "ssh_pwd": "**********"

    },
    "live": {


    }

}