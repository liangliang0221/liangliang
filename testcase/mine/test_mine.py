# -*- coding: utf-8 -*-
import allure
import pytest

from conftest.mine import Mine
from testcase.fixtures import driver  # noqa: F401


@allure.feature("我的页面测试模块")
@allure.description("我的页面模块用例集合：包含我的页面 UI 元素定位测试")
class TestMine:
    @allure.story("我的页面 UI 元素定位测试")
    @allure.title("执行我的页面 UI 元素定位测试")
    @allure.description("验证我的页面的各项 UI 元素是否正确显示和可交互")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.flaky(reruns=2, reruns_delay=5)
    def test_case_001(self, driver):
        Mine(driver).mine()
