# -*-coding: utf-8 -*-
# @Time    : 2026/05/13
# @Author  : AutoTest
# @File    : test_wowo.py
# @Software: PyCharm

import allure
import pytest

from conftest.test_module import WowoTestModule
from common.GetDriver import yaml_profile_data


@allure.feature('综合测试模块')
@allure.description('综合测试用例集合：包含登录、首页、消息模块的端到端测试')
class TestWowo():

    def setup_method(self):
        print("开始测试")
        driver = yaml_profile_data("../config/activity.yaml")
        self.driver = driver

    def teardown_method(self):
        print("测试结束")
        self.driver.quit()

    @allure.story("综合功能测试")
    @allure.title("执行登录-首页-消息综合测试")
    @allure.description("执行完整的端到端测试流程：登录 -> 首页元素验证 -> 消息模块验证")
    @allure.step("当前用例为综合功能测试")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.flaky(reruns=2, reruns_delay=5)
    def test_case_001(self):
        WowoTestModule(self.driver).run_test()

if __name__ == '__main__':
    pytest.main(['-s', 'test_message.py'])