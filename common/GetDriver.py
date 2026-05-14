# -*- coding: utf-8 -*-
from appium import webdriver
from appium.options.common import AppiumOptions
from selenium.common.exceptions import WebDriverException

from common.ReadFile import ReadFile
from common.logs import log


logger = log()


def yaml_profile_data(address):
    """根据 YAML 配置创建 Appium Remote WebDriver。"""
    data = ReadFile(address).data
    required_keys = [
        "platformName",
        "platformVersion",
        "deviceName",
        "appPackage",
        "appActivity",
        "noReset",
        "unicodeKeyboard",
        "resetKeyboard",
        "ensureWebviewsHavePages",
        "newCommandTimeout",
        "ip",
        "port",
    ]
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        raise KeyError("driver 配置缺少必填项：%s" % ", ".join(missing_keys))

    driver_caps = {
        "platformName": data["platformName"],
        "platformVersion": str(data["platformVersion"]),
        "deviceName": data["deviceName"],
        "appPackage": data["appPackage"],
        "appActivity": data["appActivity"],
        "noReset": data["noReset"],
        "unicodeKeyboard": data["unicodeKeyboard"],
        "resetKeyboard": data["resetKeyboard"],
        "ensureWebviewsHavePages": data["ensureWebviewsHavePages"],
        "newCommandTimeout": data["newCommandTimeout"],
    }
    options = AppiumOptions()
    options.load_capabilities(driver_caps)

    server_url = "http://%s:%s/wd/hub" % (data["ip"], data["port"])
    logger.info(
        "准备启动 Appium driver：server=%s，platform=%s，device=%s，appPackage=%s，appActivity=%s"
        % (server_url, data["platformName"], data["deviceName"], data["appPackage"], data["appActivity"])
    )
    try:
        driver = webdriver.Remote(server_url, options=options)
        logger.info("Appium driver 启动成功：%s" % server_url)
        return driver
    except WebDriverException as exc:
        logger.error("Appium driver 启动失败：server=%s，错误=%s" % (server_url, exc))
        raise
