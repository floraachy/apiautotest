# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/2/2 16:05
# @Author  : chenyinhua
# @File    : conftest.py
# @Software: PyCharm
# @Desc: 这是文件的描述信息

# 标准库导入
import time
# 第三方库导入
from loguru import logger
# 本地应用/模块导入
from config.global_vars import CUSTOM_MARKERS


# ------------------------------------- START: pytest钩子函数处理---------------------------------------#
def pytest_configure(config):
    """
    注册自定义标记
    """
    # 注册自定义标记
    print(f"需要注册的标记：{CUSTOM_MARKERS}")
    logger.debug(f"需要注册的标记：{CUSTOM_MARKERS}")
    markers = list(set(CUSTOM_MARKERS))
    for custom_marker in markers:
        if isinstance(custom_marker, str):
            config.addinivalue_line('markers', f'{custom_marker}')
            print(f"注册了自定义标记：{custom_marker}")
            logger.debug(f"注册了自定义标记：{custom_marker}")
        elif isinstance(custom_marker, dict):
            for k, v in custom_marker.items():
                config.addinivalue_line('markers', f'{k}:{v}')
            print(f"注册了自定义标记：{custom_marker}")
            logger.debug(f"注册了自定义标记：{custom_marker}")


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
    _ACTUAL_RUN = _PASSED + _FAILED + _XPASSED + _XFAILED
    logger.success(f"\n======================================================\n"
                   "-------------测试结果--------------------\n"
                   f"用例总数: {_TOTAL}\n"
                   f"跳过用例数: {_SKIPPED}\n"
                   f"实际执行用例总数: {_ACTUAL_RUN}\n"
                   f"通过用例数: {_PASSED}\n"
                   f"异常用例数: {_ERROR}\n"
                   f"失败用例数: {_FAILED}\n"
                   f"重跑的用例数(--reruns的值): {_RERUN}({reruns_value})\n"
                   f"意外通过的用例数: {_XPASSED}\n"
                   f"预期失败的用例数: {_XFAILED}\n\n"
                   "用例执行时长: %.2f" % _TIMES + " s\n")
    try:
        _RATE = _PASSED / _ACTUAL_RUN * 100
        logger.success(
            f"\n用例成功率: %.2f" % _RATE + " %\n"
                                       "=====================================================")
    except ZeroDivisionError:
        logger.critical(
            f"用例成功率: 0.00 %\n"
            "=====================================================")

# ------------------------------------- END: pytest钩子函数处理---------------------------------------#
