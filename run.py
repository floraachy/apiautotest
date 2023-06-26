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

 allure相关参数：
    –-alluredir这个选项用于指定存储测试结果的路径
"""

import os
import shutil
import pytest
from loguru import logger
import click
from datetime import datetime
from case_utils.case_fun_handle import generate_cases
from case_utils.platform_handle import PlatformHandle
from case_utils.send_result_handle import send_result
from case_utils.allure_handle import AllureReportBeautiful
from config.path_config import REPORT_DIR, LOG_DIR, AUTO_CASE_DIR, CONF_DIR, LIB_DIR, ALLURE_RESULTS_DIR, \
    ALLURE_HTML_DIR
from config.settings import LOG_LEVEL
from config.global_vars import GLOBAL_VARS, ENV_VARS
from common_utils.files_handle import zip_file, copy_file


def capture_all_logs(level=LOG_LEVEL):
    logger.info("""
                     _    _         _      _____         _
      __ _ _ __ (_)  / \\  _   _| |_ __|_   _|__  ___| |_
     / _` | "_ \\| | / _ \\| | | | __/ _ \\| |/ _ \\/ __| __|
    | (_| | |_) | |/ ___ \\ |_| | || (_) | |  __/\\__ \\ |_
     \\__,_| .__/|_/_/   \\_\\__,_|\\__\\___/|_|\\___||___/\\__|
          |_|
          Starting      ...     ...     ...
        """)
    if level:
        # 仅捕获指定级别日志
        logger.add(
            os.path.join(LOG_DIR, "runtime_{time}.log"),
            enqueue=True,
            encoding="utf-8",
            rotation="00:00",
            level=LOG_LEVEL.upper(),
            format="{time:YYYY-MM-DD HH:mm:ss} {level} From {module}.{function} : {message}",
        )
    else:
        # 捕获所有日志
        logger.add(
            os.path.join(LOG_DIR, "runtime_{time}_{level}.log"),
            enqueue=True,
            encoding="utf-8",
            rotation="00:00",
            format="{time:YYYY-MM-DD HH:mm:ss} {level} From {module}.{function} : {message}",
        )


# 封装生成测试用例的函数
def auto_generate_test_cases():
    # 删除原有的测试用例，以便生成新的测试用例
    if os.path.exists(AUTO_CASE_DIR):
        shutil.rmtree(AUTO_CASE_DIR)

    # 根据data里面的yaml/excel文件，自动生成测试用例
    generate_cases()


# 封装执行 pytest 的函数
def run_pytest(report_type, mark_param):
    arg_list = []

    # 执行指定的测试用例
    if mark_param is not None:
        arg_list.append(f"-m {mark_param}")

    current_time = datetime.now().strftime("%Y-%m-%d+%H_%M_%S")

    # 生成 Allure 报告
    if report_type.lower() == "allure":
        arg_list.extend(
            [
                "-q",
                "--cache-clear",
                f'--alluredir={ALLURE_RESULTS_DIR}',
                "--clean-alluredir",
            ]
        )
        pytest.main(args=arg_list)

        # ------------------------ 使用allure生成测试报告 ------------------------

        # 从LIB_DIR目录中寻找以allure开头的目录作为allure模块的目录，并进入bin目录下
        allure_path = os.path.join(LIB_DIR, [i for i in os.listdir(LIB_DIR) if i.startswith("allure")][0], "bin")
        # 根据windows或linux环境判断, 执行指定的命令。
        cmd = PlatformHandle().allure[1].format(
            os.path.join(allure_path, PlatformHandle().allure[0]),
            ALLURE_RESULTS_DIR,
            ALLURE_HTML_DIR,
        )
        os.popen(cmd).read()
        # ------------------------ 美化allure测试报告 ------------------------
        # 设置allure报告窗口标题
        AllureReportBeautiful(allure_html_path=ALLURE_HTML_DIR).set_windows_title(
            new_title=ENV_VARS["common"]["project_name"]
        )
        # 设置allure报告名称
        AllureReportBeautiful(allure_html_path=ALLURE_HTML_DIR).set_report_name(
            new_name=ENV_VARS["common"]["report_title"]
        )
        # 往allure测试报告中写入环境配置相关信息
        env_info = ENV_VARS["common"]
        env_info["run_env"] = GLOBAL_VARS.get("host", "")
        AllureReportBeautiful(allure_html_path=ALLURE_HTML_DIR).set_report_env_on_html(
            env_info=env_info
        )
        # 复制http_server.exe以及双击查看报告.bat文件到allure-html根目录下，用于支撑电脑在未安装allure服务的情况下打开allure-html报告
        # 注意：ZIP文件的名称包含某些特殊字符，会导致无法使用.bat文件打开allure-html报告， 例如空格，/ 等
        allure_config_path = os.path.join(CONF_DIR, "allure_config")

        copy_file(src_file_path=os.path.join(allure_config_path,
                                             [i for i in os.listdir(allure_config_path) if i.endswith(".exe")][0]),
                  dest_dir_path=ALLURE_HTML_DIR)
        copy_file(src_file_path=os.path.join(allure_config_path,
                                             [i for i in os.listdir(allure_config_path) if i.endswith(".bat")][0]),
                  dest_dir_path=ALLURE_HTML_DIR)

        # ------------------------ allure测试报告生成完毕，压缩allure测试报告为ZIP文件 ------------------------
        # report_path以及attachment_path，后面发送测试结果需要用到
        report_path = ALLURE_HTML_DIR
        attachment_path = os.path.join(REPORT_DIR, f'autotest_{str(current_time)}.zip')
        # 压缩allure-html报告为一个压缩文件zip
        zip_file(in_path=report_path, out_path=attachment_path)

    # 生成 pytest-html 报告
    else:
        report_path = os.path.join(REPORT_DIR, "autotest_" + str(current_time) + ".html")
        attachment_path = report_path
        pytest_html_config_path = os.path.join(CONF_DIR, "pytest_html_config")
        report_css = os.path.join(pytest_html_config_path, "pytest_html_report.css")
        arg_list.extend([f"--html={report_path}", f"--css={report_css}"])
        pytest.main(args=arg_list)

    return report_path, attachment_path


# 主函数
@click.command()
@click.option("-report", default="allure", help="选择需要生成的测试报告：pytest-html, allure")
@click.option("-env", default="test", help="输入运行环境：test 或 live")
@click.option("-m", default=None, help="选择需要运行的用例：python.ini配置的名称")
def run(report, env, m):
    try:
        # ------------------------ 捕获日志----------------------------
        capture_all_logs()

        # ------------------------ 设置全局变量 ------------------------
        # 根据指定的环境参数，将运行环境所需相关配置数据保存到GLOBAL_VARS
        GLOBAL_VARS["env_key"] = env.lower()
        if ENV_VARS.get(env.lower()):
            GLOBAL_VARS.update(ENV_VARS[env.lower()])

        # ------------------------ 自动生成测试用例 ------------------------
        auto_generate_test_cases()

        # ------------------------ pytest执行测试用例 ------------------------
        report_path, attachment_path = run_pytest(report_type=report, mark_param=m)

        # ------------------------ 发送测试结果 ------------------------
        # 发送通知
        send_result(report_path, report_type=report, attachment_path=attachment_path)

    except Exception as e:
        raise e


if __name__ == "__main__":
    run()
