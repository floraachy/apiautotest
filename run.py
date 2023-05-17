# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/1/9 17:09
# @Author  : chenyinhua
# @File    : run.py
# @Software: PyCharm
# @Desc: 框架主入口
"""
说明：
1、用例创建原则，测试文件名必须以“test”开头，测试函数必须以“test”开头。
2、运行方式：
  > python run.py  (默认在test环境运行测试用例)
  > python run.py -env live 在live环境运行测试用例
  > python run.py -env=test 在test环境运行测试用例
"""

import os
import shutil
import pytest
from config.project_path import REPORT_DIR, LOG_DIR, AUTO_CASE_DIR, CONF_DIR
from case_utils.case_handle import get_case_data
from loguru import logger
import click
from config.settings import REPORT_NAME, LOG_LEVEL
from datetime import datetime


@click.command()
@click.option("-env", default=None, help="输入运行环境：test 或 live")
@click.option("-m", default=None, help="选择需要运行的用例：python.ini配置的名称")
def run(env, m):
    # 捕获所有日志
    logger.add(os.path.join(LOG_DIR, "runtime_{time}_all.log"), enqueue=True, encoding="utf-8", rotation="00:00",
               format="{time:YYYY-MM-DD HH:mm:ss} {level} From {module}.{function} : {message}")
    # 仅捕获指定级别日志
    logger.add(os.path.join(LOG_DIR, "runtime_{time}_all.log"), enqueue=True, encoding="utf-8", rotation="00:00",
               level=LOG_LEVEL.upper(),
               format="{time:YYYY-MM-DD HH:mm:ss} {level} From {module}.{function} : {message}")
    logger.info("""
                     _    _         _      _____         _
      __ _ _ __ (_)  / \\  _   _| |_ __|_   _|__  ___| |_
     / _` | "_ \\| | / _ \\| | | | __/ _ \\| |/ _ \\/ __| __|
    | (_| | |_) | |/ ___ \\ |_| | || (_) | |  __/\\__ \\ |_
     \\__,_| .__/|_/_/   \\_\\__,_|\\__\\___/|_|\\___||___/\\__|
          |_|
          Starting      ...     ...     ...
        """)
    # 生成case在执行
    if os.path.exists(AUTO_CASE_DIR):
        # 删除文件夹
        shutil.rmtree(AUTO_CASE_DIR)

    if os.path.exists('outputs/report/'):
        shutil.rmtree(path='outputs/report/')

    # 获取用例
    get_case_data()
    # 执行用例
    current_time = datetime.now().strftime("%Y-%m-%d %H_%M_%S")
    report_name = os.path.join(REPORT_DIR, REPORT_NAME + str(current_time) + ".html")
    report_css = os.path.join(CONF_DIR, "report.css")
    arg_list = [f'--html={report_name}', f"--css={report_css}"]
    if env == "live":
        arg_list.append("--env=live")
    # 执行指定测试用例
    if m is not None:
        arg_list.append(f"-m {m}")
    pytest.main(args=arg_list)


if __name__ == '__main__':
    run()
