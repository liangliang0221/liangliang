# -*-coding: utf-8 -*-
# @Time    : 2023/12/14 11:57
# @Author  : zhenhai
# @File    : party.py
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
当前模块为party模块，主要存放用例：
1.
2.
3.
4.
....
"""

class Party:
    """
    Party 模块封装：用于执行 party 相关 yaml 驱动用例步骤。

    当前文件中只保留了入口初始化逻辑，具体用例方法在代码中被注释掉。
    """
    def __init__(self,driver):
        """
        初始化 Party 模块。

        Args:
            driver: Appium WebDriver 实例
        """
        self.driver = driver

    # def mobile_login(self):
    #     # 手机号登录
    #     path = PATH("../data/login/mobile_login.yaml")
    #     Operate(path,self.driver).check_operate_type()
    #
    # def facebook_login(self):
    #     # Facebook登录
    #     path = PATH("../data/login/mobile_login.yaml")
    #     Operate(path,self.driver).check_operate_type()