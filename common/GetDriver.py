# -*-coding: utf-8 -*-
# @Time    : 2026/05/13
# @Author  : liangliang
# @File    : GetDriver.py
# @Software: PyCharm

from appium import webdriver
from common.ReadFile import *
from selenium.common.exceptions import WebDriverException
from common.logs import log
from appium.options.common import AppiumOptions


log = log()


def yaml_profile_data(address):
    """
    根据 yaml 配置创建并启动 Appium `Remote` WebDriver。

    Args:
        address: yaml 配置文件路径（用于读取平台信息、设备信息以及 App 启动信息）

    Returns:
        Appium WebDriver: 驱动实例；如果创建失败则返回 `None`（同时会写入日志）。
    """
    try:
        data = ReadFile(address).data
        driver_caps = {
                'platformName': data['platformName'],
                'platformVersion': str(data['platformVersion']),
                'deviceName': data['deviceName'],
                'appPackage': data['appPackage'],
                'appActivity': data['appActivity'],
                'noReset': data['noReset'],
                'unicodeKeyboard': data['unicodeKeyboard'],
                'resetKeyboard': data['resetKeyboard'],
                'ensureWebviewsHavePages': data['ensureWebviewsHavePages'],
                'newCommandTimeout':data['newCommandTimeout']
            }
        options = AppiumOptions()
        options.load_capabilities(driver_caps)

        driver = webdriver.Remote('http://' + str(data['ip']) + ':' + str(data['port']) + '/wd/hub', options=options)
        print(driver)
        log.info('获取driver并启动成功')
        return driver
    except WebDriverException:
        log.warn('获取driver失败')

# if __name__ == "__main__":
#     yaml_profile_data("../config/activity.yaml")