# -*- coding: utf-8 -*-
# @Time    : 2023/9/29 9:04
# @Author  : Flora.Chen
# @File    : run_no_html_report.py
# @Software: PyCharm
# @Desc: 框架主入口

"""
说明：
1、用例创建原则，测试文件名必须以“test”开头，测试函数必须以“test”开头。
2、运行方式：
  > python run.py  (默认在test环境运行测试用例, 报告采用allure)
  > python run.py -m demo 在test环境仅运行打了标记demo用例， 默认报告采用allure
  > python run.py -env live 在live环境运行测试用例
  > python run.py -env=test 在test环境运行测试用例

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

# 标准库导入
import os
import shutil
from datetime import datetime
# 第三方库导入
import pytest
from loguru import logger
import click
# 本地应用/模块导入
from case_utils.case_fun_handle import generate_cases
from config.path_config import LOG_DIR, AUTO_CASE_DIR, ALLURE_RESULTS_DIR
from config.settings import LOG_LEVEL
from config.global_vars import GLOBAL_VARS, ENV_VARS


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
            os.path.join(LOG_DIR, "runtime_{time}_all.log"),
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
def run_pytest(mark_param):
    arg_list = []

    # 执行指定的测试用例
    if mark_param is not None:
        arg_list.append(f"-m {mark_param}")

    current_time = datetime.now().strftime("%Y-%m-%d+%H_%M_%S")

    # 生成 Allure 报告
    arg_list.extend(
        [
            "-q",
            "--cache-clear",
            f'--alluredir={ALLURE_RESULTS_DIR}',
            "--clean-alluredir",
        ]
    )
    pytest.main(args=arg_list)


# 主函数
@click.command()
@click.option("-env", default="test", help="输入运行环境：test 或 live")
@click.option("-m", default=None, help="选择需要运行的用例：python.ini配置的名称")
def run(env, m):
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
        run_pytest(mark_param=m)

    except Exception as e:
        raise e


if __name__ == "__main__":
    run()
