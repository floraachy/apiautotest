# -*- coding: utf-8 -*-
# @Time    : 2023/5/10 10:43
# @Author  : chenyinhua
# @File    : send_result_handle.py
# @Software: PyCharm
# @Desc: 根据配置文件，发送指定通知

from loguru import logger
from common_utils.yagmail_handle import YagEmailServe
from config.global_vars import NotificationType
from config.settings import SEND_RESULT_TYPE, email, ding_talk, wechat, email_subject, email_content, ding_talk_title, \
    ding_talk_content, wechat_content
from common_utils.dingding_handle import DingTalkBot
from common_utils.webchat_handle import WechatBot
from common_utils.data_handle import data_replace


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
    # -----------------------邮件通知内容-----------------------

    # 默认不发送任何通知
    if SEND_RESULT_TYPE == NotificationType.DEFAULT.value:
        pass
    # 发送邮件通知
    elif SEND_RESULT_TYPE == NotificationType.EMAIL.value:
        content = data_replace(content=email_content, source=results)
        send_email(user=email.get("user"), pwd=email.get("password"), host=email.get("host"), subject=email_subject,
                   contents=content, to=email.get("to"), attachments=attachment_path)
    # 发送钉钉通知
    elif SEND_RESULT_TYPE == NotificationType.DING_TALK.value:
        content = data_replace(content=ding_talk_content, source=results)
        send_dingding(webhook_url=ding_talk["webhook_url"], secret=ding_talk["secret"], title=ding_talk_title,
                      text=content)
    # 发送企业微信通知
    elif SEND_RESULT_TYPE == NotificationType.WECHAT.value:
        content = data_replace(content=wechat_content, source=results)
        send_wechat(webhook_url=wechat["webhook_url"], content=content, attachment=attachment_path)
    # 全部渠道都发送通知
    else:
        # 发送邮件
        content = data_replace(content=email_content, source=results)
        send_email(user=email.get("user"), pwd=email.get("password"), host=email.get("host"), subject=email_subject,
                   contents=content, to=email.get("to"), attachments=attachment_path)
        # 发送钉钉通知
        content = data_replace(content=ding_talk_content, source=results)
        send_dingding(webhook_url=ding_talk["webhook_url"], secret=ding_talk["secret"], title=ding_talk_title,
                      text=content)
        # 发送企业微信
        content = data_replace(content=wechat_content, source=results)
        send_wechat(webhook_url=wechat["webhook_url"], content=content, attachment=attachment_path)
