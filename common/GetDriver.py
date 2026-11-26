# -*-coding: utf-8 -*-
# @Time    : 2023/11/16 17:04
# @Author  : zhenhai
# @File    : GetDriver.py
# @Software: PyCharm

from appium import webdriver
import os
import sys

# 让脚本直接运行时也能找到 common 包（sys.path[0] 会变成 common/，需要补上项目根目录）
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

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
        # 关闭压缩布局层级，否则自绘/Compose 页面在 page_source 中只剩极少节点，无法定位
        try:
            driver.update_settings({'compressedLayoutHierarchy': False, 'waitForIdleTimeout': 0})
        except Exception:
            log.warn('设置 compressedLayoutHierarchy 失败，继续使用默认设置')
        print(driver)
        log.info('获取driver并启动成功')
        return driver
    except WebDriverException as e:
        log.warn('获取driver失败：%s' % e)
        raise

# if __name__ == "__main__":
#     yaml_profile_data("../config/activity.yaml")