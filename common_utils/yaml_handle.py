# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/1/31 15:22
# @Author  : chenyinhua
# @File    : yaml_handle.py
# @Software: PyCharm
# @Desc: 从日志文件中提取响应数据

import yaml


class HandleYaml:

    def __init__(self, filename):
        """
        初始化用例文件
        :param filename: 文件绝对路径，如：D:\test\test.yaml
        """
        self.filename = filename

    @property
    def read_yaml(self):
        with open(file=self.filename, mode="r", encoding="utf-8") as fp:
            return yaml.safe_load(fp.read())

    def write(self, data, mode="a"):
        """
        往yaml文件中写入数据，默认是追加写入
        :param data: 要写入的数据
        :param mode: 写入模式
        :return:
        """
        with open(self.filename, mode=mode, encoding="utf-8") as f:
            yaml.dump(data, f)
