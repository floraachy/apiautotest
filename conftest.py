# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/2/2 16:05
# @Author  : chenyinhua
# @File    : conftest.py
# @Software: PyCharm
# @Desc: 这是文件的描述信息

# 标准库导入
import re
import time
from time import strftime
# 第三方库导入
from loguru import logger
from py._xmlgen import html  # 安装pytest-html，版本最好是2.1.1
import pytest
# 本地应用/模块导入
from config.global_vars import ENV_VARS, GLOBAL_VARS, CUSTOM_MARKERS


# ------------------------------------- START: pytest钩子函数处理---------------------------------------#
def pytest_configure(config):
    """
    1. 在测试运行前，修改Environment部分信息，配置测试报告环境信息
    2. 注册自定义标记
    """
    # 给环境表 添加项目名称及开始时间
    config._metadata["项目名称"] = ENV_VARS["common"]["project_name"]
    config._metadata['开始时间'] = strftime('%Y-%m-%d %H:%M:%S')
    # 给环境表 移除packages 及plugins
    config._metadata.pop("Packages")
    config._metadata.pop("Plugins")
    # 注册自定义标记
    print(f"需要注册的标记：{CUSTOM_MARKERS}")
    markers = list(set(CUSTOM_MARKERS))
    for custom_marker in markers:
        if isinstance(custom_marker, str):
            config.addinivalue_line('markers', f'{custom_marker}')
            print(f"注册了自定义标记：{custom_marker}")
        elif isinstance(custom_marker, dict):
            for k, v in custom_marker.items():
                config.addinivalue_line('markers', f'{k}:{v}')
            print(f"注册了自定义标记：{custom_marker}")


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    """
    在测试运行后，修改Environment部分信息
    """
    # 给环境表 添加 项目环境
    session.config._metadata['项目环境'] = GLOBAL_VARS.get("host", "")


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    """设置列"用例描述"的值为用例的标题title"""
    outcome = yield
    # 获取调用结果的测试报告，返回一个report对象
    # report对象的属性包括when（steup, call, teardown三个值）、nodeid(测试用例的名字)、outcome(用例的执行结果，passed,failed)
    report = outcome.get_result()
    # 将测试用例的title作为测试报告"用例描述"列的值。
    # 注意参数传递时需要这样写：@pytest.mark.parametrize("case", cases, ids=["{}".format(case["title"]) for case in cases])
    report.description = re.findall('\\[(.*?)\\]', report.nodeid)[0]
    report.func = report.nodeid.split("[")[0]


def pytest_terminal_summary(terminalreporter, config):
    """
    收集测试结果
    """
    _RERUN = len([i for i in terminalreporter.stats.get('rerun', []) if i.when != 'teardown'])
    try:
        # 获取pytest传参--reruns的值
        reruns_value = int(config.getoption("--reruns"))
        _RERUN = int(_RERUN / reruns_value)
    except Exception:
        reruns_value = "未配置--reruns参数"
        _RERUN = len([i for i in terminalreporter.stats.get('rerun', []) if i.when != 'teardown'])

    _PASSED = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
    _ERROR = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
    _FAILED = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
    _SKIPPED = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
    _XPASSED = len([i for i in terminalreporter.stats.get('xpassed', []) if i.when != 'teardown'])
    _XFAILED = len([i for i in terminalreporter.stats.get('xfailed', []) if i.when != 'teardown'])

    _TOTAL = terminalreporter._numcollected
    _TIMES = time.time() - terminalreporter._sessionstarttime
    logger.success(f"\n======================================================\n"
                   "-------------测试结果--------------------\n"
                   f"用例总数: {_TOTAL}\n"
                   f"跳过用例数: {_SKIPPED}\n"
                   f"实际执行用例总数: {_PASSED + _FAILED + _XPASSED + _XFAILED}\n\n"
                   f"异常用例数: {_ERROR}\n"
                   f"失败用例数: {_FAILED}\n"
                   f"重跑的用例数(--reruns的值): {_RERUN}({reruns_value})\n"
                   f"意外通过的用例数: {_XPASSED}\n"
                   f"预期失败的用例数: {_XFAILED}\n\n"
                   "用例执行时长: %.2f" % _TIMES + " s\n")
    try:
        _RATE = _PASSED / (_TOTAL - _SKIPPED) * 100
        logger.success(
            f"\n用例成功率: %.2f" % _RATE + " %\n"
                                       "=====================================================")
    except ZeroDivisionError:
        logger.critical(
            f"用例成功率: 0.00 %\n"
            "=====================================================")


# ------------------------------------- END: pytest钩子函数处理---------------------------------------#

# ------------------------------------- START: pytest-html钩子函数处理 ---------------------------------------#

def pytest_html_report_title(report):
    """
    修改报告标题
    """
    report.title = f'{ENV_VARS["common"]["project_name"]} {ENV_VARS["common"]["report_title"]}'


def pytest_html_results_summary(prefix, summary, postfix):
    """
    修改Summary部分的信息
    """
    prefix.extend([html.p(f'测试人员：{ENV_VARS["common"]["tester"]}')])
    prefix.extend([html.p(f'所属部门: ：{ENV_VARS["common"]["department"]}')])


def pytest_html_results_table_header(cells):
    """
    修改结果表的表头
    """
    cells.pop(1)  # 移除 "Test" 列
    # 往表格中增加一列"用例描述"，并且给"用例描述"增加排序
    cells.insert(0, html.th('用例描述', class_="sortable", col="name"))
    # 往表格中增加一列"用例方法"，并且给"用例方法"增加排序
    cells.insert(1, html.th('用例方法', class_="sortable", col="name"))
    # 往表格中增加一列"执行时间"，并且给"执行时间"增加排序
    cells.insert(2, html.th('执行时间', class_="sortable time", col="time"))


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    """
    修改结果表的表头后给对应的行增加值
    """
    cells.pop(1)  # 移除 "Test" 列
    # 往列"用例描述"插入每行的值
    cells.insert(0, html.td(report.description))
    # 往列"用例方法"插入每行的值
    cells.insert(1, html.td(report.func))
    # 往列"执行时间"插入每行的值
    cells.insert(2, html.td(strftime("%Y-%m-%d %H:%M:%S"), class_="col-time"))


def pytest_html_results_table_html(report, data):
    """如果测试通过，则显示这条用例通过啦！"""
    if report.passed:
        del data[:]
        data.append(html.div("这条用例通过啦！", class_="empty log"))

# ------------------------------------- END: pytest-html钩子函数处理 ---------------------------------------#
