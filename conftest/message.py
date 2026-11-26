# -*-coding: utf-8 -*-
# @Time    : 2023/12/14 11:43
# @Author  : zhenhai
# @File    : message.py
# @Software: PyCharm

import os
import sys

# 让脚本直接运行时也能找到 common 包（sys.path[0] 会变成 conftest/，需要补上项目根目录）
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from common.Operate import Operate

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

"""
当前模块为讯息模块，主要存放用例：
1.讯息-主页面点击
2.讯息-我的好友
3.讯息-添加好友
4.讯息-家族群聊
5.讯息-热门活动、和声通知、官方公告、、、
......
"""

class Message:
    """
    讯息模块封装：用于执行 message 相关 yaml 驱动用例步骤。
    """
    def __init__(self,driver):
        """
        初始化 Message 模块。

        Args:
            driver: Appium WebDriver 实例
        """
        self.driver = driver

    def message_tab(self):
        """
        执行「讯息-主页面点击」用例（读取 `message_tab.yaml`）。
        """
        # 讯息-主页面点击
        path = PATH("../data/message/message_tab.yaml")
        Operate(path,self.driver).check_operate_type()

    def message_myFriends(self):
        """
        执行「讯息-我的好友」用例（读取 `message_myFriends.yaml`）。
        """
        # 讯息-我的好友
        path = PATH("../data/message/message_myFriends.yaml")
        Operate(path,self.driver).check_operate_type()

    def message_getFriends(self):
        """
        执行「讯息-添加好友」用例（读取 `message_getFriends.yaml`）。
        """
        # 讯息-添加好友
        path = PATH("../data/message/message_getFriends.yaml")
        Operate(path, self.driver).check_operate_type()

    def message_family(self):
        """
        执行「讯息-家族群聊」用例（读取 `message_family.yaml`）。
        """
        # 讯息-家族群聊
        path = PATH("../data/message/message_family.yaml")
        Operate(path, self.driver).check_operate_type()

    def message_inform(self):
        """
        执行「讯息-热门活动/和声通知/官方公告」用例（读取 `message_inform.yaml`）。
        """
        # 讯息-热门活动、和声通知、官方公告等
        path = PATH("../data/message/message_inform.yaml")
        Operate(path, self.driver).check_operate_type()
