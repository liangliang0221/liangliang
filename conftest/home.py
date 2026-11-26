# -*-coding: utf-8 -*-
# @Time    : 2023/11/22 15:30
# @Author  : zhenhai
# @File    : home.py
# @Software: PyCharm
import os
import sys

# 让脚本直接运行时也能找到 common 包（sys.path[0] 会变成 conftest/，需要补上项目根目录）
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from common.Operate import Operate

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

"""
当前模块为首页模块，主要存放用例：
1.
2.
3.
4.
....
"""

class Home:
    """
    首页模块封装：用于执行首页相关的 yaml 驱动用例步骤。
    """
    def __init__(self,driver):
        """
        初始化 Home 模块。

        Args:
            driver: Appium WebDriver 实例
        """
        self.driver = driver

    def home_works(self):
        """
        执行首页「works」相关用例（读取 `home_works.yaml`）。
        """
        path = PATH("../data/home/home_works.yaml")
        Operate(path,self.driver).check_operate_type()

    def home_family(self):
        """
        执行首页「family」相关用例（读取 `home_family.yaml`）。
        """
        path = PATH("../data/home/home_family.yaml")
        Operate(path,self.driver).check_operate_type()