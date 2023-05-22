# -*- coding: utf-8 -*-
# @Time    : 2023/5/19 11:46
# @Author  : chenyinhua
# @File    : get_results_handle.py
# @Software: PyCharm
# @Desc: 从测试报告中获取测试结果

import os
from common_utils.bs4_handle import SoupAPI
import json
from common_utils.time_handle import timestamp_strftime
from loguru import logger


def get_test_results_from_pytest_html_report(html_report_path):
    """
    通过BeautifulSoup4解析pytest-html生成的html报告，获取测试结果及测试情况
    :param html_report_path: pytest-html测试报告的绝对路径
    """
    try:
        bs = SoupAPI(html_report_path)
        test_results = {}

        # -------------- 获取测试环境信息 --------------
        environment_info = bs.get_element_by_id("environment").get_text()
        new_environment_info = [element for element in environment_info.split("\n") if element != '']
        for key, value in enumerate(new_environment_info):
            if value == "Platform":
                test_results['platform'] = new_environment_info[key + 1]

            if value == "Python":
                test_results['python_version'] = f"Python {new_environment_info[key + 1]}"

            if value == "开始时间":
                test_results['start_time'] = new_environment_info[key + 1]

            if value == "项目名称":
                test_results['project_name'] = new_environment_info[key + 1]

            if value == "项目环境":
                test_results['project_env'] = new_environment_info[key + 1]

        # -------------- 获取测试人员，所属部门，测试用例总数，运行时长 --------------
        p_elements = bs.get_elements_by_tag("p")
        for p_element in p_elements:
            res = p_element.get_text()
            if "测试人员：" in res:
                test_results['tester'] = res.replace("测试人员：", "")
            if "所属部门: " in res:
                test_results['department'] = res.replace("所属部门: ", "")
            if "tests ran" in res:
                new_list = res.split(" ")
                test_results['run_time'] = f"{new_list[4]} 秒"

        # -------------- 获取具体结果 --------------
        # 通过的用例个数
        passed = bs.select_element('span.passed')[0]
        test_results["passed"] = int(passed.get_text().split(" ")[0])
        # 跳过的用例个数
        skipped = bs.select_element('span.skipped')[0]
        test_results["skipped"] = int(skipped.get_text().split(" ")[0])
        # 失败的用例个数
        failed = bs.select_element('span.failed')[0]
        test_results["failed"] = int(failed.get_text().split(" ")[0])
        # 错误的用例个数
        error = bs.select_element('span.error')[0]
        test_results["broken"] = int(error.get_text().split(" ")[0])
        # 预期失败的用例个数
        xfailed = bs.select_element('span.xfailed')[0]
        test_results["xfailed"] = int(xfailed.get_text().split(" ")[0])
        # 意外通过的用例个数
        xpassed = bs.select_element('span.xpassed')[0]
        test_results["xpassed"] = int(xpassed.get_text().split(" ")[0])
        # 重跑的用例个数
        rerun = bs.select_element('span.rerun')[0]
        test_results["rerun"] = int(rerun.get_text().split(" ")[0])
        # 用例总数
        test_results['total'] = test_results["passed"] + test_results["skipped"] + test_results["failed"] + \
                                test_results[
                                    "broken"] + test_results["xfailed"] + test_results["xpassed"]
        # 通过率
        # 判断运行用例总数大于0
        if test_results['total'] > 0:
            # 计算用例成功率
            test_results["pass_rate"] = round(
                (test_results["passed"] + test_results["skipped"]) / test_results["total"] * 100, 2
            )
        else:
            # 如果未运行用例，则成功率为 0.0
            test_results["pass_rate"] = 0.0

        logger.debug(f"获取到的测试结果：{test_results}")
        return test_results
    except FileNotFoundError as e:
        logger.error(f"程序中检查到您未生成pytest-html报告，通常可能导致的原因是pytest-html环境未配置正确，{e}")
        raise FileNotFoundError(
            "程序中检查到您未生成pytest-html报告，"
            "通常可能导致的原因是pytest-html环境未配置正确，"
        ) from e


def get_test_results_from_from_allure_report(allure_html_path):
    """
    从allure生成的html报告的summary.json中，获取测试结果及测试情况
    :param allure_html_path: allure生成的html报告的绝对路径
    """
    try:
        summary_json_path = os.path.join(allure_html_path, "widgets", "summary.json")
        with open(summary_json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        case_count = data['statistic']
        _time = data['time']
        logger.debug(f"获取到的data是：{data}")
        logger.debug(f"获取到的_time是：{data['time']}")
        logger.debug(f"获取到的start是：{_time['start']}")
        keep_keys = {"passed", "failed", "broken", "skipped", "total"}
        test_results = {k: v for k, v in data['statistic'].items() if k in keep_keys}
        # 判断运行用例总数大于0
        if case_count["total"] > 0:
            # 计算用例成功率
            test_results["pass_rate"] = round(
                (case_count["passed"] + case_count["skipped"]) / case_count["total"] * 100, 2
            )
        else:
            # 如果未运行用例，则成功率为 0.0
            test_results["pass_rate"] = 0.0

        # 收集用例运行时长
        test_results['run_time'] = _time if test_results['total'] == 0 else round(_time['duration'] / 1000, 2)
        test_results["start_time"] = timestamp_strftime(_time["start"])
        test_results["stop_time"] = timestamp_strftime(_time["stop"])

        # 收集重试次数
        retry_trend_json_path = os.path.join(allure_html_path, "widgets", "retry-trend.json")
        with open(retry_trend_json_path, 'r', encoding='utf-8') as file:
            retry_data = json.load(file)
        test_results["rerun"] = retry_data[0]["data"]["retry"]
        # 项目环境
        env_json_path = os.path.join(allure_html_path, "widgets", "environment.json")
        with open(env_json_path, 'r', encoding='utf-8') as file:
            env_data = json.load(file)
        for data in env_data:
            test_results[data['name']] = data["values"][0]
        logger.debug(f"获取到的测试结果：{test_results}")
        return test_results
    except FileNotFoundError as e:
        logger.error(f"程序中检查到您未生成allure报告，通常可能导致的原因是allure环境未配置正确，{e}")
        raise FileNotFoundError(
            "程序中检查到您未生成allure报告，"
            "通常可能导致的原因是allure环境未配置正确，"
        ) from e
