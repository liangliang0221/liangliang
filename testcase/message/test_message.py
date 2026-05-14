# -*- coding: utf-8 -*-
import allure
import pytest

from conftest.message import Message
from testcase.fixtures import driver  # noqa: F401


@allure.feature("消息测试模块")
@allure.description("消息模块用例集合：包含消息页面 UI 元素定位测试")
class TestMessage:
    @allure.story("消息页面 UI 元素定位测试")
    @allure.title("执行消息页面 UI 元素定位测试")
    @allure.description("验证消息页面的各项 UI 元素是否正确显示和可交互")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.flaky(reruns=2, reruns_delay=5)
    def test_case_001(self, driver):
        Message(driver).message()
