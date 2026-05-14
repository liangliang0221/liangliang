# -*- coding: utf-8 -*-
import os
import sys

import allure
import pytest

from conftest.test_module import WowoTestModule
from testcase.fixtures import driver  # noqa: F401


CURRENT_FILE = os.path.abspath(__file__)
DEBUG_NODE = "%s::TestWowo::test_case_001" % CURRENT_FILE


@allure.feature("综合测试模块")
@allure.description("综合测试用例集合：用于调试 data/test.yaml 中配置的单文件用例流程")
class TestWowo:
    @allure.story("单文件调试用例")
    @allure.title("执行 data/test.yaml 调试流程")
    @allure.description("读取 data/test.yaml，并按 YAML 步骤顺序执行当前调试流程")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.flaky(reruns=2, reruns_delay=5)
    def test_case_001(self, driver):
        WowoTestModule(driver).run_test()

def debug_main():
    """Run only this file's debug testcase."""
    args = [
        DEBUG_NODE,
        "-s",
        "-vv",
        "--tb=short",
        "--disable-warnings",
        "--maxfail=1",
        "--reruns=0",
        "--alluredir=./ouput/debug_temp",
        "--clean-alluredir",
    ]
    return pytest.main(args)


if __name__ == "__main__":
    sys.exit(debug_main())
