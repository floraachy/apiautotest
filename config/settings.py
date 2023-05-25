# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/1/9 17:08
# @Author  : chenyinhua
# @File    : settings.py
# @Software: PyCharm
# @Desc: 项目配置文件

# ------------------------------------ 配置信息 ----------------------------------------------------#
# 0代表执行Excel和yaml两种格式的用例， 1 代表 yaml文件，2 用例代表Excel用例
CASE_FILE_TYPE = 1

# 0表示默认不发送任何通知， 1代表钉钉通知，2代表企业微信通知， 3代表邮件通知， 4代表所有途径都发送通知
SEND_RESULT_TYPE = 0

# 测试报告的定制化信息展示
ENV_INFO = {
        "report_title": "自动化测试报告",
        "report_name": "autotestreport_",
        "project_name": "GitLink 确实开源",
        "tester": "陈银花",
        "department": "开源中心"
    }

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

# ------------------------------------ 邮件通知内容 ----------------------------------------------------#
email_subject = f"{ENV_INFO.get('project_name', None)} 接口自动化报告"
email_content = """
           各位同事, 大家好:

           自动化用例于 <strong>${start_time} </strong> 开始运行，运行时长：<strong>${run_time} s</strong>， 目前已执行完成。
           ---------------------------------------------------------------------------------------------------------------
           测试人：<strong> ${tester} </strong> 
           所属部门：<strong> ${department} </strong>
           项目环境：<strong> ${project_env} </strong>
           ---------------------------------------------------------------------------------------------------------------
           执行结果如下:
           &nbsp;&nbsp;用例运行总数:<strong> ${total} 个</strong>
           &nbsp;&nbsp;通过用例个数（passed）: <strong><font color="green" >${passed} 个</font></strong>
           &nbsp;&nbsp;失败用例个数（failed）: <strong><font color="red" >${failed} 个</font></strong>
           &nbsp;&nbsp;异常用例个数（error）: <strong><font color="orange" >${broken} 个</font></strong>
           &nbsp;&nbsp;跳过用例个数（skipped）: <strong><font color="grey" >${skipped} 个</font></strong>
           &nbsp;&nbsp;失败重试用例个数 * 次数之和（rerun）: <strong>${rerun} 个</strong>
           &nbsp;&nbsp;成  功   率:<strong> <font color="green" >${pass_rate} %</font></strong>

           **********************************
           附件为具体的测试报告，详细情况可下载附件查看， 非相关负责人员可忽略此消息。谢谢。
       """
# ------------------------------------ 钉钉相关配置 ----------------------------------------------------#
ding_talk = {
    "webhook_url": "https://oapi.dingtalk.com/robot/send?access_token=***********",
    "secret": "***********"
}

# ------------------------------------ 钉钉通知内容 ----------------------------------------------------#
ding_talk_title = f"{ENV_INFO.get('project_name', None)} 接口自动化报告"
ding_talk_content = """
           各位同事, 大家好:

           ### 自动化用例于 ${start_time} 开始运行，运行时长：${run_time} s， 目前已执行完成。
            ---------------------------------------------------------------------------------------------------------------
           #### 测试人： ${tester}
           #### 所属部门： ${department}
           #### 项目环境：${project_env} 
           ---------------------------------------------------------------------------------------------------------------
           #### 执行结果如下:
           - 用例运行总数: ${total} 个
           - 通过用例个数（passed）: ${passed} 个
           - 失败用例个数（failed）: ${failed} 个
           - 异常用例个数（error）: ${broken} 个
           - 跳过用例个数（skipped）: ${skipped} 个
           - 失败重试用例个数 * 次数之和（rerun）: ${rerun} 个
           - 成  功   率: ${pass_rate} %

           **********************************
           附件为具体的测试报告，详细情况可下载附件查看， 非相关负责人员可忽略此消息。谢谢。
       """
# ------------------------------------ 企业微信相关配置 ----------------------------------------------------#
wechat = {
    "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=********",
}
# ------------------------------------ 企业微信通知内容 ----------------------------------------------------#
wechat_content = """
           各位同事, 大家好:

           ### 自动化用例于 ${start_time} 开始运行，运行时长：${run_time} s， 目前已执行完成。
           --------------------------------
           #### 测试人： ${tester}
           #### 所属部门： ${department}
           #### 项目环境：${project_env} 
           --------------------------------
           #### 执行结果如下:
           - 用例运行总数: ${total} 个
           - 通过用例个数（passed）:<font color=\"info\"> ${passed} 个</font>
           - 失败用例个数（failed）: <font color=\"warning\"> ${failed}  个</font>
           - 异常用例个数（error）: <font color=\"warning\"> ${broken} 个</font>
           - 跳过用例个数（skipped）: <font color=\"comment\"> ${skipped} 个</font>
           - 失败重试用例个数 * 次数之和（rerun）: <font color=\"comment\"> ${rerun} 个</font>
           - 成  功   率: <font color=\"info\"> ${pass_rate} % </font>

           **********************************
           附件为具体的测试报告，详细情况可下载附件查看， 非相关负责人员可忽略此消息。谢谢。
       """
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
