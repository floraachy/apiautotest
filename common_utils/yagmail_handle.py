# -*- coding: utf-8 -*-
# @Time    : 2021/8/14 12:21
# @Author  : Flora.Chen
# @File    : yagmail_handle.py
# @Software: PyCharm
# @Desc: 通过第三方模块yagmail发送邮件

import yagmail
from loguru import logger
import os


class YagEmailServe:
    def __init__(self, host, user, password):
        """
        user(发件人邮箱), password(邮箱授权码), host(发件人使用的邮箱服务 例如：smtp.163.com)
        """
        self.host = host
        self.user = user
        self.password = password

    def send_email(self, info: dict):
        """
        发送邮件
        :param info:包括,contents(内容), to(收件人列表), subject(邮件标题), attachments(附件列表)
        info = {
            "subject": "",
            "contents": "",
            "to": "",
            "attachments": ""
        }
        :return:
        """
        logger.debug("------------ 连接邮件服务器 ---------------")
        yag = yagmail.SMTP(
            user=self.user,
            password=self.password,
            host=self.host)
        logger.debug("------------ 开始发送邮件 ---------------")
        # 如果存在附件，则与邮件内容一起发送附件，否则仅发送邮件内容
        if os.path.exists(info['attachments']):
            yag.send(
                to=info['to'],
                subject=info['subject'],
                contents=info['contents'],
                attachments=info['attachments'])
        else:
            yag.send(
                to=info['to'],
                subject=info['subject'],
                contents=info['contents'])
        logger.debug("------------ 邮件发送完毕，关闭邮件服务器连接 ---------------")
        yag.close()
