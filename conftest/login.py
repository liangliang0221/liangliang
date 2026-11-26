# -*-coding: utf-8 -*-
# @Time    : 2023/10/25 10:32
# @Author  : zhenhai
# @File    : 123.py
# @Software: PyCharm

# 单个功能模块测试用例集

import os
import sys

# 让脚本直接运行时也能找到 common 包（sys.path[0] 会变成 conftest/，需要补上项目根目录）
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from common.Operate import Operate

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

"""
当前模块为登录模块，主要存放用例：
1.手机号登录
2.Facebook登录
3.Google登录
4.UID登录
....
"""

class Login:
    """
    登录模块封装：用于执行不同登录方式的 yaml 驱动用例步骤。
    """

    def __init__(self,driver):
        """
        初始化 Login 模块。

        Args:
            driver: Appium WebDriver 实例
        """
        self.driver = driver

    def mobile_login(self):
        """
        手机号登录流程（读取 `mobile_login.yaml`）。
        """
        # 手机号登录
        path = PATH("../data/login/login.yaml")
        Operate(path,self.driver).check_operate_type()

    def rename(self):
        """
        重命名用户流程（读取 `rename.yaml`，保持与现有实现一致）。
        """
        # 重命名用户
        path = PATH("../data/login/rename.yaml")
        Operate(path,self.driver).check_operate_type()
