# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/2/2 16:05
# @Author  : chenyinhua
# @File    : conftest.py
# @Software: PyCharm
# @Desc: 这是文件的描述信息
import os.path

from config.global_vars import ENV_VARS, GLOBAL_VARS
import pytest
from py._xmlgen import html  # 安装pytest-html，版本最好是2.1.1
from time import strftime
import re


# ------------------------------------- START: 报告处理 ---------------------------------------#
@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    """设置列"用例描述"的值为用例的标题title"""
    outcome = yield
    # 获取调用结果的测试报告，返回一个report对象
    # report对象的属性包括when（steup, call, teardown三个值）、nodeid(测试用例的名字)、outcome(用例的执行结果，passed,failed)
    report = outcome.get_result()
    # 将测试用例的title作为测试报告"用例描述"列的值。
    # 注意参数传递时需要这样写：@pytest.mark.parametrize("case", cases, ids=["{}".format(case["title"]) for case in cases])
    report.description = re.findall('\[(.*?)\]', report.nodeid)[0]
    report.func = report.nodeid.split("[")[0]


def pytest_html_report_title(report):
    """
    修改报告标题
    """
    report.title = f'{ENV_VARS["common"]["project_name"]} {ENV_VARS["common"]["report_title"]}'


def pytest_configure(config):
    """
    # 在测试运行前，修改Environment部分信息，配置测试报告环境信息
    """
    # 给环境表 添加项目名称及开始时间
    config._metadata["项目名称"] = ENV_VARS["common"]["project_name"]
    config._metadata['开始时间'] = strftime('%Y-%m-%d %H:%M:%S')
    # 给环境表 移除packages 及plugins
    config._metadata.pop("Packages")
    config._metadata.pop("Plugins")


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    """
    在测试运行后，修改Environment部分信息
    """
    # 给环境表 添加 项目环境
    session.config._metadata['项目环境'] = GLOBAL_VARS.get("host", "")


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

# ------------------------------------- END: 报告处理 ---------------------------------------#
