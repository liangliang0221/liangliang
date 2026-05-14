# -*-coding: utf-8 -*-
# @Time    : 2026/05/13
# @Author  : liangliang
# @File    : test_home.py
# @Software: PyCharm

import allure
import pytest
from conftest.homepage import HomePage
from common.GetDriver import yaml_profile_data


@allure.feature('首页测试模块')
@allure.description('首页模块用例集合：包含首页推荐页和首页树洞的UI元素定位测试')
class TestHomePage():

    def setup_method(self):
        print("这里是开始")
        driver = yaml_profile_data("../config/activity.yaml")
        self.driver = driver

    def teardown_method(self):
        print("这里是结束")
        self.driver.quit()

    @allure.story("首页推荐页UI元素定位测试")
    @allure.title("执行首页推荐页UI元素定位测试")
    @allure.description("验证首页推荐页的各项UI元素是否正确显示和可交互")
    @allure.step("当前用例为首页推荐页UI元素定位测试")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.flaky(reruns=2, reruns_delay=5)
    def test_case_001(self):
        HomePage(self.driver).home_page()

    @allure.story("首页树洞UI元素定位测试")
    @allure.title("执行首页树洞UI元素定位测试")
    @allure.description("验证首页树洞模块的各项UI元素是否正确显示和可交互")
    @allure.step("当前用例为首页树洞UI元素定位测试")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.flaky(reruns=2, reruns_delay=5)
    def test_case_002(self):
        HomePage(self.driver).home_tree()


if __name__ == '__main__':
    pytest.main(['-s', 'test_message.py'])