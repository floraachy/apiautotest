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
  > python run.py  (默认在test环境运行测试用例, 报告采用allure)
  > python run.py -env live 在live环境运行测试用例
  > python run.py -env=test 在test环境运行测试用例
  > python run.py -report=pytest-html (默认在test环境运行测试用例, 报告采用pytest-html)
"""

import os
import shutil
import pytest
from config.project_path import REPORT_DIR, LOG_DIR, AUTO_CASE_DIR, CONF_DIR, LIB_DIR, ALLURE_RESULTS_DIR, \
    ALLURE_HTML_DIR
from case_utils.case_handle import get_case_data
from loguru import logger
import click
from config.settings import LOG_LEVEL, ENV_INFO
from datetime import datetime
from case_utils.platform_handle import PlatformHandle
from case_utils.get_results_handle import get_test_results_from_pytest_html_report, \
    get_test_results_from_from_allure_report
from case_utils.send_result_handle import send_result
from case_utils.allure_handle import AllureReportBeautiful
from common_utils.files_handle import zip_file


@click.command()
@click.option("-report", default="allure", help="选择需要生成的测试报告：pytest-html, allure")
@click.option("-env", default="test", help="输入运行环境：test 或 live")
@click.option("-m", default=None, help="选择需要运行的用例：python.ini配置的名称")
def run(env, m, report):
    try:
        # ------------------------ 捕获日志 ------------------------
        # 捕获所有日志
        logger.add(os.path.join(LOG_DIR, "runtime_{time}_all.log"), enqueue=True, encoding="utf-8", rotation="00:00",
                   format="{time:YYYY-MM-DD HH:mm:ss} {level} From {module}.{function} : {message}")
        # 仅捕获指定级别日志
        logger.add(os.path.join(LOG_DIR, "runtime_{time}.log"), enqueue=True, encoding="utf-8", rotation="00:00",
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
        # ------------------------ 自动生成测试用例 ------------------------
        # 删除原有的测试用例，以便生成新的测试用例
        if os.path.exists(AUTO_CASE_DIR):
            # 删除文件夹
            shutil.rmtree(AUTO_CASE_DIR)

        # 根据data里面的yaml/excel文件，自动生成测试用例
        get_case_data()

        # ------------------------ pytest执行测试用例 ------------------------
        """
            pytest相关参数：以下也可通过pytest.ini配置
             --reruns: 失败重跑次数
             --reruns-delay 失败重跑间隔时间
             --count: 重复执行次数
            -v: 显示错误位置以及错误的详细信息
            -s: 等价于 pytest --capture=no 可以捕获print函数的输出
            -q: 简化输出信息
            -m: 运行指定标签的测试用例
            -x: 一旦错误，则停止运行
            --cache-clear 清除pytest的缓存，包括测试结果缓存、抓取的fixture实例缓存和收集器信息缓存等
            --maxfail: 设置最大失败次数，当超出这个阈值时，则不会在执行测试用例
            "--reruns=3", "--reruns-delay=2"
        """
        arg_list = []
        if env.lower() == "live":
            arg_list.append("--env=live")
        # 执行指定测试用例
        if m is not None:
            arg_list.append(f"-m {m}")
        if report.lower() == "allure":
            arg_list.extend(['-q', '--cache-clear', f'--alluredir={ALLURE_RESULTS_DIR}', '--clean-alluredir'])
            """
                allure相关参数：
                –-alluredir这个选项用于指定存储测试结果的路径
            """
            pytest.main(args=arg_list)
            # ------------------------ 使用allure生成测试报告 ------------------------
            # 往allure测试结果集目录写入环境配置相关信息
            ENV_INFO["project_env"] = env
            AllureReportBeautiful(allure_results_path=ALLURE_RESULTS_DIR).set_report_env(env_info=ENV_INFO)
            logger.debug("-------开始生成allure测试报告-------")
            plat = PlatformHandle()
            # 从LIB_DIR目录中寻找以allure开头的目录作为allure模块的目录，并进入bin目录下
            allure_path = os.path.join(LIB_DIR, [i for i in os.listdir(LIB_DIR) if i.startswith("allure")][0], "bin")
            # 根据windows或linux环境判断, 执行指定的命令。plat.allure[0]=cmd, plat.allure[1]=cmd2
            cmd = plat.allure[1].format(os.path.join(allure_path, plat.allure[0]), ALLURE_RESULTS_DIR, ALLURE_HTML_DIR)
            # 执行命令行命令，并通过read()方法将命令的结果返回；os.popen() 方法用于从一个命令打开一个管道。在Unix，Windows中有效
            os.popen(cmd).read()
            logger.debug("-------美化allure测试报告-------")
            AllureReportBeautiful(allure_html_path=ALLURE_HTML_DIR).set_windows_title(
                new_title=ENV_INFO["project_name"])
            AllureReportBeautiful(allure_html_path=ALLURE_HTML_DIR).set_report_name(new_name=ENV_INFO["report_title"])
            logger.debug("-------allure测试报告生成完毕，开始发送测试报告-------")
            # 发送从allure-html获取的测试报告
            results = get_test_results_from_from_allure_report(ALLURE_HTML_DIR)
            # 压缩allure-html报告为一个压缩文件zip
            allure_zip_path = os.path.join(REPORT_DIR, f'{ENV_INFO["report_name"]}.zip')
            zip_file(in_path=ALLURE_HTML_DIR, out_path=allure_zip_path)
            send_result(results=results, attachment_path=allure_zip_path)
        else:
            current_time = datetime.now().strftime("%Y-%m-%d %H_%M_%S")
            report_path = os.path.join(REPORT_DIR, ENV_INFO["report_name"] + str(current_time) + ".html")
            report_css = os.path.join(CONF_DIR, "pytest_html_report.css")
            arg_list.extend([f'--html={report_path}', f"--css={report_css}"])
            pytest.main(args=arg_list)
            logger.debug("-------测试完成，发送测试报告-------")
            # 发送从pytest-html获取的测试报告
            results = get_test_results_from_pytest_html_report(report_path)
            send_result(results=results, attachment_path=report_path)
    except Exception as e:
        raise e


if __name__ == '__main__':
    run()
