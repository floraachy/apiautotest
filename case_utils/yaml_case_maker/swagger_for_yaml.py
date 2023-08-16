# -*- coding: utf-8 -*-
# @Time    : 2023/8/15 15:52
# @Author  : chenyinhua
# @File    : swagger_for_yaml.py
# @Software: PyCharm
# @Desc:

# 标准库导入
import os
import json
from typing import Dict
# 第三方库导入
from jsonpath import jsonpath
from ruamel import yaml

"""
相比较于pyyaml, Ruamel可以保持YAML文件的结构和顺序不变。
安装：pip install ruamel.yaml
"""


class SwaggerForYaml:
    """
    将swagger接口文档转为YAML格式用例
    """

    def __init__(self, case_dir, swagger_path):
        """
        :param case_dir: 用例需要保存的目录
        :param swagger_path: 需要读取的swagger文件的路径
        """
        self._data = self.get_swagger_json(swagger_path)
        self.case_dir = case_dir

    def get_swagger_json(self, path):
        """
        获取 swagger 中的 json 数据
        :param path: 需要读取的swagger文件的路径
        :return:
        """
        try:
            with open(path, "r", encoding='utf-8') as f:
                row_data = json.load(f)
                return row_data
        except FileNotFoundError:
            raise FileNotFoundError("文件路径不存在，请重新输入")

    def get_allure_epic(self):
        """
        获取 yaml 用例中的 allure_epic
        """
        _allure_epic = self._data['info']['title']
        return _allure_epic

    @classmethod
    def get_allure_feature(cls, value):
        """
        获取 yaml 用例中的 allure_feature
        取的是每一个接口的tags， tag可能是列表格式，例如："tags": ["组织下可选角色"]，这种就处理一下获取第一个元素值
        """
        _allure_feature = value['tags'][0] if isinstance(value['tags'], list) else value['tags']
        return str(_allure_feature)

    @classmethod
    def get_allure_story(cls, value):
        """
        获取 yaml 用例中的 allure_story
        取的是每一个接口的summary
        """
        _allure_story = value['summary']
        return _allure_story

    @classmethod
    def get_case_id(cls, value):
        """
        获取 case_id， 是根据接口路径生成的
        """
        _case_id = value.replace("/", "_")
        return "case" + _case_id + "_01"

    @classmethod
    def get_title(cls, value):
        """
        获取接口的标题
        """
        _get_detail = value['summary']
        return "测试 " + _get_detail

    @classmethod
    def get_headers(cls, value):
        """
        获取请求头
        """
        _headers = {}
        # 先检查是否存在consumes， 存在则consumes的值作为header的Content-Type
        consumes = jsonpath(obj=value, expr="$.consumes")
        if consumes and consumes != [[]]:
            _headers = {"Content-Type": consumes[0][0]}
        # 再检查parameters是否存在，存在则检查in是否等于header， 存在则header[parameters[name]]=None
        parameters = jsonpath(obj=value, expr="$.parameters")
        if parameters and parameters != [[]]:
            for i in value['parameters']:
                if i['in'] == 'header':
                    _headers[i['name']] = None
        # 如果_headers是{}就返回None
        return None if not _headers else _headers

    @classmethod
    def get_request_type(cls, value, headers):
        """
        处理 request_type：需要综合考虑参数的in和header请求类型
        """
        headers_values = list(headers.values()) if isinstance(headers, dict) else str(headers)
        parameters = jsonpath(obj=value, expr="$.parameters")
        if parameters and parameters != [[]]:
            _parameters = value['parameters']
            if _parameters[0]['in'] == 'query':
                return "params"
            else:
                if 'application/x-www-form-urlencoded' in headers_values or 'multipart/form-data' in headers_values:
                    return "data"
                elif 'application/json' in headers_values:
                    return "json"
                elif 'application/octet-stream' in headers_values:
                    return "file"
                else:
                    return "data"

    @classmethod
    def get_payload(cls, value):
        """
        处理 payload数据
        """
        _dict = {}
        if jsonpath(obj=value, expr="$.parameters"):
            _parameters = value['parameters']
            for i in _parameters:
                if i['in'] != 'header':
                    _dict[i['name']] = None
        else:
            return None
        return None if not _dict else _dict

    def yaml_cases(self, data: Dict, file_path: str) -> None:
        """
        写入 yaml 数据
        :param file_path:
        :param data: 测试用例数据
        :return:
        """
        # 检查目录不存在则创建， 存在则不创建
        os.makedirs(self.case_dir, exist_ok=True)
        _file_name = file_path[1:].replace("/", "_") + '.yaml'
        _file_path = os.path.join(self.case_dir, _file_name)
        if _file_name in os.listdir(self.case_dir):
            data.pop("case_common")
            data = data["case_info"]
        with open(_file_path, "a", encoding="utf-8") as file:
            yaml.dump(data, file, Dumper=yaml.RoundTripDumper, allow_unicode=True)
            file.write('\n')

    def write_yaml_handler(self):
        # 获取所有接口的相关数据，key=接口路径， value=接口各项参数
        _api_data = self._data['paths']
        for key, value in _api_data.items():
            for k, v in value.items():
                yaml_data = {
                    "case_common": {
                        "allure_epic": self.get_allure_epic(),
                        "allure_feature": self.get_allure_feature(v),
                        "allure_story": self.get_allure_story(v)
                    },
                    "case_info": [
                        {
                            "id": self.get_case_id(key + "_" + k),
                            "title": self.get_title(v),
                            "run": False,
                            "url": key,
                            "severity": None,
                            "method": k,
                            "headers": self.get_headers(v),
                            "cookies": None,
                            "request_type": self.get_request_type(v, self.get_headers(v)),
                            "payload": self.get_payload(v),
                            "files": None,
                            "extract": None,
                            "assert_response": {'eq': {'http_code': 200}},
                            "assert_sql": None

                        }
                    ]
                }
                self.yaml_cases(data=yaml_data, file_path=key)


if __name__ == '__main__':
    SwaggerForYaml(case_dir=r"", swagger_path=r"").write_yaml_handler()
