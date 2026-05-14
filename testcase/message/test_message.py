# -*-coding: utf-8 -*-
# @Time    : 2026/05/13
# @Author  : liangliang
# @File    : test_message.py
# @Software: PyCharm

import allure
import pytest
from conftest.message import Message
from common.GetDriver import yaml_profile_data


@allure.feature('消息测试模块')
@allure.description('消息模块用例集合：包含消息页面UI元素定位测试')
class TestMessage():

    def setup_method(self):
        print("这里是开始")
        driver = yaml_profile_data("../config/activity.yaml")
        self.driver = driver

    def teardown_method(self):
        print("这里是结束")
        self.driver.quit()

    @allure.story("消息页面UI元素定位测试")
    @allure.title("执行消息页面UI元素定位测试")
    @allure.description("验证消息页面的各项UI元素是否正确显示和可交互")
    @allure.step("当前用例为消息页面UI元素定位测试")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.flaky(reruns=2, reruns_delay=5)
    def test_case_001(self):
        Message(self.driver).message()


if __name__ == '__main__':
    pytest.main(['-s', 'test_message.py'])