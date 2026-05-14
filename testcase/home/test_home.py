# -*- coding: utf-8 -*-
import allure
import pytest

from conftest.homepage import HomePage
from testcase.fixtures import driver  # noqa: F401


@allure.feature("首页测试模块")
@allure.description("首页模块用例集合：包含首页推荐页和首页树洞的 UI 元素定位测试")
class TestHomePage:
    @allure.story("首页推荐页 UI 元素定位测试")
    @allure.title("执行首页推荐页 UI 元素定位测试")
    @allure.description("验证首页推荐页的各项 UI 元素是否正确显示和可交互")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.flaky(reruns=2, reruns_delay=5)
    def test_case_001(self, driver):
        HomePage(driver).home_page()

    @allure.story("首页树洞 UI 元素定位测试")
    @allure.title("执行首页树洞 UI 元素定位测试")
    @allure.description("验证首页树洞模块的各项 UI 元素是否正确显示和可交互")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.flaky(reruns=2, reruns_delay=5)
    def test_case_002(self, driver):
        HomePage(driver).home_tree()
