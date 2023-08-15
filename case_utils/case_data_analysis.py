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
        """
        处理method参数：校验method参数是否是指定枚举值中的一个
        """
        return self.check_params_right(
            Method,
            self.case_data.get(TestCaseEnum.METHOD.value[0])
        )

    @property
    def get_severity(self) -> Text:
        """
        处理severity参数：如果Severity为空或者不传或者传错，视为NORMAL
        """
        # 如果Severity为空或者不传或者传错，视为NORMAL
        attr = self.case_data.get(TestCaseEnum.SEVERITY.value[0])
        if attr is None or attr.upper() not in Severity._member_names_:
            return "NORMAL"
        else:
            return attr.upper()

    @property
    def get_request_type(self):
        """
        处理request_type参数：校验request_type参数是否是指定枚举值中的一个
        """
        return self.check_params_right(
            RequestType,
            self.case_data.get(TestCaseEnum.REQUEST_TYPE.value[0])
        )

    def check_case_data_attr(self, attr: Text):
        """
        检查用例中是否缺失某个参数
        """
        assert attr in self.case_data.keys(), (
            f"用例ID: {self.case_id} --> 缺少 {attr} 参数，请确认用例内容是否编写规范."
        )

    def check_params_exit(self):
        """
        遍历一个枚举类中所有成员，并检查与每个成员对应的实例属性是否存在。
        如果属性存在，则什么也不做，如果不存在，则抛出异常或执行其他操作
        """
        print(f"打印：{list(TestCaseEnum._value2member_map_)}")
        for enum in list(TestCaseEnum._value2member_map_):
            if enum[1]:
                self.check_case_data_attr(enum[0])

    def check_required_fields(self):
        for field in TestCaseEnum:
            if field.value[1]:  # 判断是否为必填参数
                field_name = field.value[0]
                value = self.case_data[field_name]
                if value is None or (isinstance(value, str) and len(value.strip()) == 0):
                    raise ValueError(f"用例ID: {self.case_id} --> {field_name}字段的值是：{value}， 该字段值是必填，请检查是否填写正确.")

    def check_params_right(self, enum_name, attr):
        """
        检查参数值是否正确，符合要求规范
        """
        _member_names_ = enum_name._member_names_
        assert attr.upper() in _member_names_, (
            f"用例ID: {self.case_id} --> {enum_name}: {attr} 填写不正确，"
            f"当前框架中只支持 {_member_names_} 类型."
            f"如有疑问，请联系管理员."
        )
        return attr.upper()

    def case_process(self, cases):
        case_list = []
        for key, values in cases.items():
            # 公共配置中的数据，与用例数据不同，需要单独处理
            if key == 'case_info':
                for value in values:
                    self.case_data = value
                    self.case_id = value.get("id")
                    # 检查用例参数，需要必填的是否有值
                    self.check_required_fields()
                    # 检查用例参数值，是否都填写正确
                    self.check_params_exit()
                    case_data = {
                        'id': self.case_data.get(TestCaseEnum.ID.value[0]),
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
                        "assert_response": self.case_data.get(TestCaseEnum.ASSERT_RESPONSE.value[0]),
                        "assert_sql": self.case_data.get(TestCaseEnum.ASSERT_SQL.value[0]),
                    }
                    case_list.append(case_data)

        return case_list
