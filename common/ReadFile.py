# -*-coding: utf-8 -*-
# @Time    : 2023/11/16 16:56
# @Author  : zhenhai
# @File    : Readfile.py
# @Software: PyCharm

import os
import yaml
from yamlinclude import YamlIncludeConstructor

YamlIncludeConstructor.add_to_loader_class(loader_class=yaml.FullLoader)

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))


class ReadFile:
    """
    读取配置文件（主要为 yaml）并返回解析后的数据结构。
    """
    def __init__(self, file):
        """
        初始化读取器。

        Args:
            file: 配置文件的相对路径（相对 `common/` 目录）
        """
        if os.path.isfile(PATH(file)):
            self.file = PATH(file)
        else:
            raise FileNotFoundError("文件不存在")

    @property  # 设置属性，调用data方法时可通过调用属性，不需要带括号
    def data(self):
        """
        以 `yaml.FullLoader` 方式读取 yaml 配置并返回内容。
        """
        with open(file=self.file, mode="rb") as f:
            infos = yaml.load(f, Loader=yaml.FullLoader)
            # infos = yaml.load(f)
        return infos

    def date(self):
        """
        以默认 yaml loader 方式读取配置文件（用于兼容旧逻辑）。
        """
        with open(file=self.file, mode="rb") as f:
            # infos = yaml.load(f, Loader=yaml.FullLoader)
            infos = yaml.load(f)
        return infos

"""
调用方法：
infos = ReadFile("../config/start_activity.py").data
"""