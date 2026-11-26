# -*-coding: utf-8 -*-
# @Time    : 2023/12/14 10:47
# @Author  : zhenhai
# @File    : shakedown.py
# @Software: PyCharm
# 用于单个测试用例调试
import os
import sys

# 让脚本直接运行时也能找到 common 包（sys.path[0] 会变成 conftest/，需要补上项目根目录）
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from common.Operate import Operate
from common.GetDriver import yaml_profile_data

"""
当前模块为测试单个用例，yaml用例存放至data的yemltest文件后调用main方法即可
"""

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

yamlpath = PATH("../data/login/yaml_login_huange.yaml")
print(yamlpath)
# 注意：这里是「启动参数」配置（capability），不是用例文件；ReadFile 以 common/ 为基准解析相对路径
driver = yaml_profile_data("../config/activity.yaml")

class Shakedown:
    """
    单用例调试封装。

    通过启动一个 driver，然后调用 `Operate` 去执行 `yamltest.yaml` 中的对应步骤。
    """
    def __init__(self,driver):
        """
        初始化 Shakedown 调试器。

        Args:
            driver: Appium WebDriver 实例
        """
        self.path = yamlpath
        self.driver = driver
        self.operate = Operate(self.path, self.driver)

    def shakedown(self):
        """
        执行单用例调试逻辑。
        """
        # 单个用例脚本调试使用
        self.operate.check_operate_type()


if __name__ == '__main__':
    Shakedown(driver).shakedown()