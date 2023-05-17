# -*- coding: utf-8 -*-
# @Time    : 2023/3/30 22:34
# @Author  : Flora.Chen
# @File    : files_handle.py
# @Software: PyCharm
# @Desc: 处理文件相关操作
import os


def get_files(target, start=None, end=None):
    """
    @param: target: 目标文件绝对路径
    @param: start: 以什么开头，默认为空
    @param: end: 以什么结尾，默认为空
    获取目录下所有的文件，以列表的形式返回
    """
    if os.path.isfile(target):
        return []
    # files返回j经过处理的文件列表
    files = []
    # dirpath：表示获取的目录的路径，以string形式返回值。
    # dirnames： 包含了当前dirpath路径下所有的子目录名字（不包含目录路径），以列表形式返回值。
    # filenames：包含了当前dirpath路径下所有的非目录子文件的名字（不包含目录路径）。
    for dirpath, dirnames, filenames in os.walk(target):
        for filename in filenames:
            # 如果"start"和"end"都有值
            if start and end:
                # filename是以"start"且filename是以"end"结尾，则追加到files
                if filename.startswith(start) and filename.endswith(end):
                    files.append(os.path.abspath(os.path.join(dirpath, filename)))
            # 或者如果"start"有值，filename是以"start"开头，则追加到files
            elif start and (not end):
                if filename.startswith(start):
                    files.append(os.path.abspath(os.path.join(dirpath, filename)))
            # 或者如果"end"有值，且filename是以"end"结尾，则追加到files
            elif end and (not start):
                if filename.endswith(end):
                    files.append(os.path.abspath(os.path.join(dirpath, filename)))
            else:
                files.append(os.path.abspath(os.path.join(dirpath, filename)))
    # 判断files列表是否为空，不为空则返回files，为空则返回all_files
    return files


def get_newest_file(dir_path):
    """
    获取目录下最新的文件
    """
    if os.path.isfile(dir_path):
        return None

    # 获取目录下所有文件
    files = os.listdir(dir_path)

    # 按文件修改时间排序
    sorted_files = sorted(
        [(os.path.join(dir_path, file), os.path.getmtime(os.path.join(dir_path, file))) for file in files],
        key=lambda x: x[1],
        reverse=True
    )

    # 返回最新文件路径
    return sorted_files[0][0]
