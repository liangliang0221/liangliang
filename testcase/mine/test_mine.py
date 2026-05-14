# -*-coding: utf-8 -*-
# @Time    : 2026/05/13
# @Author  : liangliang
# @File    : test_mine.py
# @Software: PyCharm

import allure
import pytest
from conftest.mine import Mine
from common.GetDriver import yaml_profile_data


@allure.feature('我的页测试模块')
@allure.description('我的页模块用例集合：包含我的页UI元素定位测试')
class TestMine():

    def setup_method(self):
        print("这里是开始")
        driver = yaml_profile_data("../config/activity.yaml")
        self.driver = driver

    def teardown_method(self):
        print("这里是结束")
        self.driver.quit()

    @allure.story("我的页UI元素定位测试")
    @allure.title("执行我的页UI元素定位测试")
    @allure.description("验证我的页面的各项UI元素是否正确显示和可交互")
    @allure.step("当前用例为我的页UI元素定位测试")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.flaky(reruns=2, reruns_delay=5)
    def test_case_001(self):
        Mine(self.driver).mine()


if __name__ == '__main__':
    pytest.main(['-s', 'test_mine.py'])
