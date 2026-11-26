# -*-coding: utf-8 -*-
# @Time    : 2026/04/30
# @Author  : AutoTest
# @File    : test_wowo.py
# @Software: PyCharm

import allure
import pytest
import os
import sys

# 让脚本直接运行时也能找到 common/conftest 包（sys.path[0] 会变成 testcase/，需要补上项目根目录）
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from conftest.shakedown import Shakedown
from conftest.login import Login

from common.GetDriver import yaml_profile_data


@allure.feature('综合测试模块')
class TestAll():
    """
    综合测试用例集合：包含登录、首页、消息模块。
    """

    def setup_method(self):
        """
        初始化 APP driver，每个用例执行前都会触发（pytest 4+ 标准命名）。
        """
        print("开始测试")
        driver = yaml_profile_data("../config/activity.yaml")
        assert driver is not None, "driver 创建失败，请检查 Appium 服务是否启动、设备是否在线、是否有遗留会话"
        self.driver = driver

    def teardown_method(self):
        """
        用例结束后关闭 driver（pytest 4+ 标准命名）。
        """
        print("测试结束")
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()

    @allure.story("综合功能测试")
    @allure.title("执行登录-首页-消息综合测试")
    @allure.step("当前用例为综合功能测试")
    def test_case_001(self):
        """
        执行综合测试流程。
        """
        # Shakedown(self.driver).shakedown()
        Login(self.driver).mobile_login()
        Login(self.driver).rename()


if __name__ == '__main__':
    # 切到项目根目录，保证 pytest.ini 中 --alluredir ./ouput/temp 输出到项目根/ouput/temp
    os.chdir(_PROJECT_ROOT)
    pytest.main(['-s', os.path.join('testcase', 'test_All.py')])
