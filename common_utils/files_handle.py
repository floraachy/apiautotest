# -*- coding: utf-8 -*-
# @Time    : 2023/3/30 22:34
# @Author  : Flora.Chen
# @File    : files_handle.py
# @Software: PyCharm
# @Desc: 处理文件相关操作
import os
import zipfile
import shutil


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
            file_path = os.path.abspath(os.path.join(dirpath, filename))
            # 如果"start"和"end"都有值
            if start and end:
                # filename是以"start"且filename是以"end"结尾，则追加到files
                if filename.startswith(start) and filename.endswith(end):
                    files.append(file_path)
            # 或者如果"start"有值，filename是以"start"开头，则追加到files
            elif start and (not end):
                if filename.startswith(start):
                    files.append(file_path)
            # 或者如果"end"有值，且filename是以"end"结尾，则追加到files
            elif end and (not start):
                if filename.endswith(end):
                    files.append(file_path)
            else:
                files.append(file_path)
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


def zip_file(in_path: str, out_path: str):
    """
    压缩指定文件夹
    :param in_path: 目标文件夹路径
    :param out_path: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    # 如果传入的路径是一个目录才进行压缩操作
    if os.path.isdir(in_path):
        print("目标路径是一个目录，开始进行压缩......")
        # 写入
        zip = zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED)
        for path, dirnames, filenames in os.walk(in_path):
            # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
            fpath = path.replace(in_path, '')
            for filename in filenames:
                zip.write(
                    os.path.join(
                        path, filename), os.path.join(
                        fpath, filename))
        zip.close()
        print("压缩完成！")
    else:
        print("目标路径不是一个目录，请检查！")


def delete_dir_file(file_path):
    """
    删除指定目录下的所有文件
    :param file_path: 目标文件夹路径 (存在多级路径的暂不支持)
    """
    paths = os.listdir(file_path)
    if paths:
        print("目标目录存在文件或目录，进行删除操作")
        for item in paths:
            path = os.path.join(file_path, item)
            # 如果目标路径是一个文件，使用os.remove删除
            if os.path.isfile(path):
                os.remove(path)
            # 如果目标路径是一个目录，使用os.rmdir删除
            if os.path.isdir(path):
                os.rmdir(path)
    else:
        print("目标目录不存在文件或目录，不需要删除")


def copy_file(src_file_path, dest_dir_path):
    """
    复制一个文件到另一个目录
    :param: src_file_path: 源文件路径
    :param: dest_dir_path: 目标文件夹路径

    """
    # 判断源文件路径是否存在
    if not os.path.isfile(src_file_path):
        return "源文件路径不存在"

    # 判断目标文件夹路径是否存在，不存在则创建
    if not os.path.isdir(dest_dir_path):
        os.makedirs(dest_dir_path)

    # 复制文件
    try:
        shutil.copy(src_file_path, dest_dir_path)
        return "复制成功"
    except Exception as e:
        return f"复制失败：{e}"


def get_file_field(file_path):
    """
    获取文件名称和二进制内容
    :param: file_path: 文件路径
    """
    # 处理文件绝对路径
    file_name = os.path.basename(file_path)
    # 获取文件二进制内容
    with open(file_path, 'rb') as f:
        file_content = f.read()
    return (file_name, file_content)
