# -*-coding: utf-8 -*-
# @Time    : 2023/12/7 20:11
# @Author  : zhenhai
# @File    : sing.py
# @Software: PyCharm
import os
import sys

# 让脚本直接运行时也能找到 common 包（sys.path[0] 会变成 conftest/，需要补上项目根目录）
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from common.Operate import Operate

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

"""
当前模块为唱歌模块，主要存放用例：
1.
2.
3.
4.
....
"""

class Sing:
    """
    唱歌模块封装：用于执行唱歌相关的 yaml 驱动用例步骤。
    """
    def __init__(self,driver):
        """
        初始化 Sing 模块。

        Args:
            driver: Appium WebDriver 实例
        """
        self.driver = driver

    def search(self):
        """
        执行唱歌「search」相关用例（读取 `search.yaml`）。
        """
        path = PATH("../data/sing/search.yaml")
        Operate(path,self.driver).check_operate_type()