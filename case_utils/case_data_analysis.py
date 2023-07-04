# -*- coding: utf-8 -*-
# @Time    : 2023/6/7 16:37
# @Author  : chenyinhua
# @File    : case_data_analysis.py
# @Software: PyCharm
# @Desc: 分析用例数据是否符合规范

# 标准库导入
from typing import Text
# 第三方库导入
from config.models import TestCase, TestCaseEnum, Method, RequestType, Severity


class CaseDataCheck:
    """
    用例数据解析, 判断数据填写是否符合规范
    """

    def __init__(self):
        self.case_data = None
        self.case_id = None

    @property
    def get_method(self) -> Text:

        return self.check_params_right(
            Method,
            self.case_data.get(TestCaseEnum.METHOD.value[0])
        )

    @property
    def get_severity(self) -> Text:
        # 如果Severity为空或者不传或者传错，视为NORMAL
        attr = self.case_data.get(TestCaseEnum.SEVERITY.value[0])
        if attr is None or attr.upper() not in Severity._member_names_:
            return "NORMAL"
        else:
            return attr.upper()

    @property
    def get_request_type(self):
        return self.check_params_right(
            RequestType,
            self.case_data.get(TestCaseEnum.REQUEST_TYPE.value[0])
        )

    def check_case_data_attr(self, attr: Text):
        assert attr in self.case_data.keys(), (
            f"用例ID为 {self.case_id} 的用例中缺少 {attr} 参数，请确认用例内容是否编写规范."
        )

    def check_params_exit(self):
        """
        遍历一个枚举类中所有成员，并检查与每个成员对应的实例属性是否存在。
        如果属性存在，则什么也不做，如果不存在，则抛出异常或执行其他操作
        """
        for enum in list(TestCaseEnum._value2member_map_.keys()):
            if enum[1]:
                self.check_case_data_attr(enum[0])

    def check_params_right(self, enum_name, attr):
        """
        检查参数值是否正确，符合要求规范
        """
        _member_names_ = enum_name._member_names_
        assert attr.upper() in _member_names_, (
            f"用例ID为 {self.case_id} 的用例中 {enum_name}: {attr} 填写不正确，"
            f"当前框架中只支持 {_member_names_} 类型."
            f"如有疑问，请联系管理员."
        )
        return attr.upper()

    @property
    def get_assert_response(self):
        _assert_data = self.case_data.get(TestCaseEnum.ASSERT_RESPONSE.value[0])
        assert _assert_data is not None, (
            f"用例ID 为 {self.case_id} 未添加断言"
        )
        return _assert_data

    def case_process(self, cases):
        case_list = []
        for key, values in cases.items():
            # 公共配置中的数据，与用例数据不同，需要单独处理
            if key != 'case_common':
                # 检查用例数据，去除用例数据中的空格
                for k, v in values.items():
                    values[k] = v.strip() if isinstance(v, str) else v
                self.case_data = values
                self.case_id = key
                self.check_params_exit()
                case_data = {
                    'feature': self.case_data.get(TestCaseEnum.FEATURE.value[0]),
                    'title': self.case_data.get(TestCaseEnum.TITLE.value[0]),
                    'severity': self.get_severity,
                    'url': self.case_data.get(TestCaseEnum.URL.value[0]),
                    'run': self.case_data.get(TestCaseEnum.RUN.value[0]),
                    'method': self.get_method,
                    'headers': self.case_data.get(TestCaseEnum.HEADERS.value[0]),
                    'cookies': self.case_data.get(TestCaseEnum.COOKIES.value[0]),
                    'request_type': self.get_request_type,
                    'payload': self.case_data.get(TestCaseEnum.PAYLOAD.value[0]),
                    'files': self.case_data.get(TestCaseEnum.FILES.value[0]),
                    'extract': self.case_data.get(TestCaseEnum.EXTRACT.value[0]),
                    "assert_response": self.get_assert_response,
                    "assert_sql": self.case_data.get(TestCaseEnum.ASSERT_SQL.value[0]),
                }
                case_list.append(TestCase(**case_data).dict())

        return case_list
