# -*-coding: utf-8 -*-
# @Time    : 2026/05/13
# @Author  : liangliang
# @File    : Mine.py
# @Software: PyCharm
import os
from common.Operate import Operate

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

"""
当前模块为我的页模块，主要存放用例：
1. mine - 我的页UI元素定位测试
"""


class Mine:
    """
    我的页模块封装：用于执行我的页相关的 yaml 驱动用例步骤。
    """
    def __init__(self, driver):
        """
        初始化 Mine 模块。

        Args:
            driver: Appium WebDriver 实例
        """
        self.driver = driver

    def mine(self):
        """
        执行我的页相关用例（读取 `mine.yaml`）。
        """
        path = PATH("../data/Mine/mine.yaml")
        Operate(path, self.driver).check_operate_type()