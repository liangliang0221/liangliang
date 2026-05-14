# -*-coding: utf-8 -*-

import os
from common.Operate import Operate

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))


class WowoTestModule:
    """
    综合测试模块封装：包含登录、首页、消息等功能的测试流程。
    """

    def __init__(self, driver):
        """
        初始化测试模块。

        Args:
            driver: Appium WebDriver 实例
        """
        self.driver = driver

    def run_test(self):
        """
        执行综合测试流程（读取 test.yaml）。
        """
        path = PATH("../data/test.yaml")
        Operate(path, self.driver).check_operate_type()