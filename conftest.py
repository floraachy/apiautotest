# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/2/2 16:05
# @Author  : chenyinhua
# @File    : conftest.py
# @Software: PyCharm
# @Desc: 这是文件的描述信息


from config.global_vars import GLOBAL_VARS
from loguru import logger
import pytest
from py._xmlgen import html  # 安装pytest-html，版本最好是2.1.1
from time import strftime
from config.settings import test, live, REPORT_TITLE, PROJECT_NAME, TESTER, DEPARTMENT


# ------------------------------------- START: 配置运行环境 ---------------------------------------#
def pytest_addoption(parser):
    """
    pytest_addoption 可以让用户注册一个自定义的命令行参数，方便用户将数据传递给 pytest；
    这个 Hook 方法一般和 内置 fixture pytestconfig 配合使用，pytest_addoption 注册命令行参数，pytestconfig 通过配置对象读取参数的值；
    :param parser:
    :return:
    """

    parser.addoption(
        # action="store" 默认，只存储参数的值，可以存储任何类型的值，此时 default 也可以是任何类型的值，而且命令行参数多次使用也只能生效一个，最后一个值覆盖之前的值；
        # action="append"，将参数值存储为一个列表，用append模式将可以在pytest命令行方式执行测试用例的同时多次向程序内部传递自定义参数对应的参数值
        "--env", action="store",
        default="test",
        choices=["test", "live"],  # choices 只允许输入的值的范围
        type=str,
        help="将命令行参数--env添加到pytest配置对象中，通过--env设置当前运行的环境host"
    )


@pytest.fixture(scope="session", autouse=True)
def get_config(request):
    """
    从配置对象中读取自定义参数的值
    """
    # 根据指定的环境，获取指定环境的域名以及用例数据文件类型
    env = request.config.getoption("--env")
    if env.lower() == "live":
        config_data = live
    else:
        config_data = test
    for item in config_data:
        for k, v in item.items():
            GLOBAL_VARS[k] = v

    logger.info(f"当前环境变量为：{GLOBAL_VARS}")


# ------------------------------------- END: 配置运行环境 ---------------------------------------#
# ------------------------------------- START: 报告处理 ---------------------------------------#
def pytest_collection_modifyitems(items):
    """# 测试用例执行收集完成时，将收集到的item的name和nodeid的中文显示在控制台上"""
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode-escape")
        item._nodeid = item._nodeid.encode("utf-8").decode("unicode_escape")


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    """设置列"用例描述"的值为用例的标题title"""
    outcome = yield
    # 获取调用结果的测试报告，返回一个report对象
    # report对象的属性包括when（steup, call, teardown三个值）、nodeid(测试用例的名字)、outcome(用例的执行结果，passed,failed)
    report = outcome.get_result()
    # TODO：由于目前无法动态将用例数据中的title写入测试方法中的文档注释，因此该处理方法暂时搁置
    # 将测试方法的文档注释作为结果表的Description的值，如果文档注释为空，则测试方法名作为结果表的Description的值
    # if item.function.__doc__ is None:
    #     report.description = str(item.function.__doc__)
    # else:
    #     report.description = str(item.function.__name__)
    report.description = GLOBAL_VARS.get("title", "")
    report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")


def pytest_html_report_title(report):
    """
    修改报告标题
    """
    report.title = REPORT_TITLE


def pytest_configure(config):
    """
    # 在测试运行前，修改Environment部分信息，配置测试报告环境信息
    """
    # 给环境表 添加项目名称及开始时间
    config._metadata["项目名称"] = PROJECT_NAME
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
    prefix.extend([html.p(TESTER)])
    prefix.extend([html.p(DEPARTMENT)])


def pytest_html_results_table_header(cells):
    """
    修改结果表的表头
    """
    # 往表格中增加一列"用例描述"，并且给"用例描述"增加排序
    cells.insert(0, html.th('用例描述', class_="sortable", col="name"))
    # 往表格中增加一列"执行时间"，并且给"执行时间"增加排序
    cells.insert(1, html.th('执行时间', class_="sortable time", col="time"))
    # 移除表格最后一列
    cells.pop()


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    """
    修改结果表的表头后给对应的行增加值
    """
    # 往列"用例描述"插入每行的值
    cells.insert(0, html.td(report.description))
    # 往列"执行时间"插入每行的值
    cells.insert(1, html.td(strftime("%Y-%m-%d %H:%M:%S"), class_="col-time"))
    # 移除表格最后一列
    cells.pop()


def pytest_html_results_table_html(report, data):
    """如果测试通过，则显示这条用例通过啦！"""
    if report.passed:
        del data[:]
        data.append(html.div("这条用例通过啦！", class_="empty log"))

# ------------------------------------- END: 报告处理 ---------------------------------------#
