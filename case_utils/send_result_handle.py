# -*- coding: utf-8 -*-
# @Time    : 2023/5/10 10:43
# @Author  : chenyinhua
# @File    : send_result_handle.py
# @Software: PyCharm
# @Desc:
from common_utils.yagmail_handle import YagEmailServe
from config.settings import email
from config.global_vars import NotificationType
from config.settings import SEND_RESULT_TYPE
from common_utils.bs4_handle import SoupAPI


def get_test_info_from_html_report(html_report_path):
    """
    从html测试报告中获取测试情况
    """
    bs = SoupAPI(html_report_path)
    results = {}

    # -------------- 获取测试环境信息 --------------
    environment_info = bs.get_element_by_id("environment").get_text()
    new_environment_info = [element for element in environment_info.split("\n") if element != '']
    for key, value in enumerate(new_environment_info):
        if value == "Platform":
            results['platform'] = new_environment_info[key + 1]

        if value == "Python":
            results['python_version'] = f"Python {new_environment_info[key + 1]}"

        if value == "开始时间":
            results['start_time'] = new_environment_info[key + 1]

        if value == "项目名称":
            results['project_name'] = new_environment_info[key + 1]

        if value == "项目环境":
            results['project_env'] = new_environment_info[key + 1]

    # -------------- 获取测试人员，所属部门，测试用例总数，运行时长 --------------
    p_elements = bs.get_elements_by_tag("p")
    for p_element in p_elements:
        res = p_element.get_text()
        if "测试人员：" in res:
            results['tester'] = res.replace("测试人员：", "")
        if "所属部门: " in res:
            results['dept'] = res.replace("所属部门: ", "")
        if "tests ran" in res:
            new_list = res.split(" ")
            results['runs_time'] = f"{new_list[4]} 秒"

    # -------------- 获取具体结果 --------------
    # 通过的用例个数
    passed = bs.select_element('span.passed')[0]
    results["passed"] = int(passed.get_text().split(" ")[0])
    # 跳过的用例个数
    skipped = bs.select_element('span.skipped')[0]
    results["skipped"] = int(skipped.get_text().split(" ")[0])
    # 失败的用例个数
    failed = bs.select_element('span.failed')[0]
    results["failed"] = int(failed.get_text().split(" ")[0])
    # 错误的用例个数
    error = bs.select_element('span.error')[0]
    results["error"] = int(error.get_text().split(" ")[0])
    # 预期失败的用例个数
    xfailed = bs.select_element('span.xfailed')[0]
    results["xfailed"] = int(xfailed.get_text().split(" ")[0])
    # 意外通过的用例个数
    xpassed = bs.select_element('span.xpassed')[0]
    results["xpassed"] = int(xpassed.get_text().split(" ")[0])
    # 重跑的用例个数
    rerun = bs.select_element('span.rerun')[0]
    results["rerun"] = int(rerun.get_text().split(" ")[0])
    # 用例总数
    results['total_cases'] = results["passed"] + results["skipped"] + results["failed"] + results["error"] + results[
        "xfailed"] + results["xpassed"]
    return results


def send_result(results, attachment_path=None):
    """
    根据用户配置，采取指定方式，发送测试结果
    """

    # 默认不发送任何通知
    if SEND_RESULT_TYPE == NotificationType.DEFAULT.value:
        pass
    # 发送邮件通知
    elif SEND_RESULT_TYPE == NotificationType.EMAIL.value:
        email_settings = email
        yag = YagEmailServe(user=email_settings.get("user"), password=email_settings.get("password"),
                            host=email_settings.get("host"))
        info = {
            "subject": f"{results.get('project_name', None)} 接口自动化报告_{results.get('start_time', None)}",
            "contents": f"""
        各位同事, 大家好:

        &nbsp;&nbsp;&nbsp;&nbsp;自动化用例于{results.get('start_time', None)}开始运行，运行时长：{results.get('runs_time', None)}， 目前已执行完成。
        -----------------------------------------------------------------------------------------------------------
        &nbsp;&nbsp;&nbsp;&nbsp;测试人：{results.get('tester', None)} / {results.get('dept', None)}
        &nbsp;&nbsp;&nbsp;&nbsp;测试平台：{results.get('platform', None)} / {results.get('python_version', None)}
        &nbsp;&nbsp;&nbsp;&nbsp;测试环境：{results.get('project_env', None)}
        ---------------------------------------------------------------------------------------------------------------
        &nbsp;&nbsp;&nbsp;&nbsp;执行结果如下:
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;用例运行总数: {results.get("total_cases", None)} 个
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;通过用例个数（passed）: {results.get("passed", None)} 个
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;失败用例个数（failed）: {results.get("failed", None)} 个
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;异常用例个数（error）: {results.get("error", None)} 个
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;跳过用例个数（skipped）: {results.get("skipped", None)} 个
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期失败用例个数（xfailed）: {results.get("xfailed", None)} 个
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;意外通过用例个数（xpassed）: {results.get("xpassed", None)} 个
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;失败重试用例个数 * 次数之和（rerun）: {results.get("rerun", None)} 个
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;成  功   率: {(results.get("passed") / results.get("total_cases")) * 100} %

        **********************************
        jenkins地址：https://xxxxxxxxx
        详细情况可登录jenkins平台查看，非相关负责人员可忽略此消息。谢谢。
        """,
            "to": email.get("to"),
            "attachments": attachment_path

        }
        yag.send_email(info)
    # 发送钉钉通知
    elif SEND_RESULT_TYPE == NotificationType.DING_TALK.value:
        pass
    # 发送企业微信通知
    elif SEND_RESULT_TYPE == NotificationType.WECHAT.value:
        pass
    # 全部渠道都发送通知
    else:
        pass
