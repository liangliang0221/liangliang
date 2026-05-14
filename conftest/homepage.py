# -*-coding: utf-8 -*-
# @Time    : 2026/05/13
# @Author  : liangliang
# @File    : HomePage.py
# @Software: PyCharm
import os
from common.Operate import Operate

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

"""
当前模块为首页模块，主要存放用例：
1. homepage - 首页推荐页UI元素定位测试
2. home_tree - 首页树洞相关UI元素定位测试
"""


class HomePage:
    """
    首页模块封装：用于执行首页相关的 yaml 驱动用例步骤。
    """
    def __init__(self, driver):
        """
        初始化 HomePage 模块。

        Args:
            driver: Appium WebDriver 实例
        """
        self.driver = driver

    def home_page(self):
        """
        执行首页推荐页相关用例（读取 `home_page.yaml`）。
        """
        path = PATH("../data/HomePage/home_page.yaml")
        Operate(path, self.driver).check_operate_type()

    def home_tree(self):
        """
        执行首页树洞相关用例（读取 `home_tree.yaml`）。
        """
        path = PATH("../data/HomePage/home_tree.yaml")
        Operate(path, self.driver).check_operate_type()