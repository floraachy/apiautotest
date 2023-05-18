# -*- coding: utf-8 -*-
# @Time    : 2023/5/10 10:43
# @Author  : chenyinhua
# @File    : send_result_handle.py
# @Software: PyCharm
# @Desc:
from loguru import logger
from common_utils.yagmail_handle import YagEmailServe
from config.global_vars import NotificationType
from config.settings import SEND_RESULT_TYPE, email, ding_talk, wechat
from common_utils.bs4_handle import SoupAPI
from common_utils.dingding_handle import DingTalkBot
from common_utils.webchat_handle import WechatBot


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


def send_email(user, pwd, host, subject, contents, to, attachments):
    """
    发送邮件
    """
    try:
        yag = YagEmailServe(user=user, password=pwd, host=host)
        info = {
            "subject": subject,
            "contents": contents,
            "to": to,
            "attachments": attachments

        }
        yag.send_email(info)
    except Exception as e:
        logger.error(f"发送邮件通知异常， 错误信息：{e}")


def send_dingding(webhook_url, secret, title, text):
    """
    发送钉钉消息
    """
    try:
        dingding = DingTalkBot(webhook_url=webhook_url, secret=secret)
        res = dingding.send_markdown(title=title, text=text, is_at_all=True)
        if res:
            logger.info(f"发送钉钉通知成功~")
        else:
            logger.error(f"发送钉钉通知失败~")
    except Exception as e:
        logger.error(f"发送钉钉通知异常， 错误信息：{e}")


def send_wechat(webhook_url, content, attachment=None):
    """
    发送企业微信消息
    """
    try:
        wechat = WechatBot(webhook_url=webhook_url)
        msg = wechat.send_markdown(content=content)
        if msg:
            if attachment:
                file = wechat.send_file(wechat.upload_file(attachment))
                if file:
                    logger.info(f"发送企业微信通知(包括文本以及附件)成功~")
                else:
                    logger.error(f"发送企业微信通知(附件)失败~")
        else:
            logger.error(f"发送企业微信（文本）失败~")
    except Exception as e:
        logger.error(f"发送企业微信通知异常， 错误信息：{e}")


def send_result(results, attachment_path=None):
    """
    根据用户配置，采取指定方式，发送测试结果
    """
    # 通知内容
    subject = f"{results.get('project_name', None)} 接口自动化报告_{results.get('start_time', None)}"
    content = f"""
            各位同事, 大家好:

            ### 自动化用例于{results.get('start_time', None)}开始运行，运行时长：{results.get('runs_time', None)}， 目前已执行完成。
            -----------------------------------------------------------------------------------------------------------
            #### 测试人：{results.get('tester', None)} / {results.get('dept', None)}
            #### 测试平台：{results.get('platform', None)} / {results.get('python_version', None)}
            #### 测试环境：{results.get('project_env', None)}
            ---------------------------------------------------------------------------------------------------------------
            #### 执行结果如下:
            - 用例运行总数: {results.get("total_cases", None)} 个
            - 通过用例个数（passed）: {results.get("passed", None)} 个
            - 失败用例个数（failed）: {results.get("failed", None)} 个
            - 异常用例个数（error）: {results.get("error", None)} 个
            - 跳过用例个数（skipped）: {results.get("skipped", None)} 个
            - 预期失败用例个数（xfailed）: {results.get("xfailed", None)} 个
            - 意外通过用例个数（xpassed）: {results.get("xpassed", None)} 个
            - 失败重试用例个数 * 次数之和（rerun）: {results.get("rerun", None)} 个
            - 成  功   率: {(results.get("passed") / results.get("total_cases")) * 100} %

            **********************************
            附件为具体的测试报告，详细情况可下载附件进程查看， 非相关负责人员可忽略此消息。谢谢。
        """

    # 默认不发送任何通知
    if SEND_RESULT_TYPE == NotificationType.DEFAULT.value:
        pass
    # 发送邮件通知
    elif SEND_RESULT_TYPE == NotificationType.EMAIL.value:
        send_email(user=email.get("user"), pwd=email.get("password"), host=email.get("host"), subject=subject,
                   contents=content, to=email.get("to"), attachments=attachment_path)
    # 发送钉钉通知
    elif SEND_RESULT_TYPE == NotificationType.DING_TALK.value:
        send_dingding(webhook_url=ding_talk["webhook_url"], secret=ding_talk["secret"], title=subject, text=content)
    # 发送企业微信通知
    elif SEND_RESULT_TYPE == NotificationType.WECHAT.value:
        send_wechat(webhook_url=wechat["webhook_url"], content=content, attachment=attachment_path)
    # 全部渠道都发送通知
    else:
        # 发送邮件
        send_email(user=email.get("user"), pwd=email.get("password"), host=email.get("host"), subject=subject,
                   contents=content, to=email.get("to"), attachments=attachment_path)
        # 发送钉钉通知
        send_dingding(webhook_url=ding_talk["webhook_url"], secret=ding_talk["secret"], title=subject, text=content)
        # 发送企业微信
        send_wechat(webhook_url=wechat["webhook_url"], content=content, attachment=attachment_path)


