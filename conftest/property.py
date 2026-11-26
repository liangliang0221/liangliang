# -*-coding: utf-8 -*-
# @Time    : 2023/12/6 18:57
# @Author  : zhenhai
# @File    : property.py
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
当前模块为我的模块，主要存放用例：
1.
2.
3.
4.
....
"""

class Property:
    """
    我的属性模块封装：用于执行 property 相关 yaml 驱动用例步骤。
    """
    def __init__(self,driver):
        """
        初始化 Property 模块。

        Args:
            driver: Appium WebDriver 实例
        """
        self.driver = driver

    def my_property(self):
        """
        执行我的属性用例（读取 `my_property.yaml`）。
        """
        path = PATH("../data/property/my_property.yaml")
        Operate(path,self.driver).check_operate_type()