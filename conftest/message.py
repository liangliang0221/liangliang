# -*-coding: utf-8 -*-
# @Time    : 2026/05/13
# @Author  : liangliang
# @File    : Message.py
# @Software: PyCharm
import os
from common.Operate import Operate

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

"""
当前模块为消息模块，主要存放用例：
1. message - 消息页面UI元素定位测试
"""


class Message:
    """
    消息模块封装：用于执行消息相关的 yaml 驱动用例步骤。
    """
    def __init__(self, driver):
        """
        初始化 Message 模块。

        Args:
            driver: Appium WebDriver 实例
        """
        self.driver = driver

    def message(self):
        """
        执行消息页面相关用例（读取 `message.yaml`）。
        """
        path = PATH("../data/Message/message.yaml")
        Operate(path, self.driver).check_operate_type()