# -*- coding: utf-8 -*-
import os
import time

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from common.logs import log


logger = log()


class Baseoperate:
    """Appium/Selenium 基础操作封装，带有限重试和失败截图。"""

    DEFAULT_TIMEOUT = 20
    POLL_FREQUENCY = 1
    MAX_RETRY = 2

    def __init__(self, driver):
        self.driver = driver

    def back(self):
        try:
            time.sleep(1)
            self.driver.press_keycode(4)
            logger.info("返回操作成功")
        except Exception as exc:
            logger.error("返回操作失败：%s" % exc)
            raise

    def blackbox(self):
        black_list = [
            (AppiumBy.XPATH, '//*[@text="登入"]'),
            (AppiumBy.XPATH, '//*[@text="确定"]'),
            (AppiumBy.XPATH, '//*[@text="取消"]'),
            (AppiumBy.XPATH, '//*[@text="允许"]'),
            (AppiumBy.XPATH, '//*[@text="Allow"]'),
            (AppiumBy.XPATH, '//*[@text="OK"]'),
        ]

        logger.info("扫描弹窗")
        for locator in black_list:
            try:
                elements = self.driver.find_elements(*locator)
            except WebDriverException:
                continue
            if elements:
                elements[0].click()
                logger.info("已关闭弹窗")
                return True

        return False

    def get_window_size(self):
        size = self.driver.get_window_size()
        return size["width"], size["height"]

    def swipe_up(self):
        width, height = self.get_window_size()
        self.driver.swipe(int(width * 0.5), int(height * 0.9), int(width * 0.5), int(height * 0.2), duration=500)
        time.sleep(1)
        logger.info("上滑成功")

    def swipe_down(self):
        width, height = self.get_window_size()
        self.driver.swipe(int(width * 0.5), int(height * 0.2), int(width * 0.5), int(height * 0.9), duration=500)
        time.sleep(1)
        logger.info("下滑成功")

    def swipe_right(self):
        width, height = self.get_window_size()
        self.driver.swipe(int(width * 0.2), int(height * 0.5), int(width * 0.8), int(height * 0.5), duration=500)
        time.sleep(1)
        logger.info("右滑成功")

    def swipe_left(self):
        width, height = self.get_window_size()
        self.driver.swipe(int(width * 0.8), int(height * 0.5), int(width * 0.2), int(height * 0.5), duration=500)
        time.sleep(1)
        logger.info("左滑成功")

    def swipe_px(self, start_x, start_y, end_x, end_y):
        self.driver.swipe(start_x, start_y, end_x, end_y, duration=500)
        time.sleep(1)
        logger.info("像素坐标滑动成功")

    def swipe_pt(self, start_x, start_y, end_x, end_y):
        width, height = self.get_window_size()
        x1 = int(width * float(start_x))
        y1 = int(height * float(start_y))
        x2 = int(width * float(end_x))
        y2 = int(height * float(end_y))
        self.driver.swipe(x1, y1, x2, y2, duration=500)
        time.sleep(1)
        logger.info("百分比坐标滑动成功")

    def sleep(self, seconds=5):
        time.sleep(seconds)
        logger.info("等待 %s 秒" % seconds)

    def screenshot(self):
        now = time.strftime("%y%m%d-%H-%M-%S")
        screenshot_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../log/screenshoot"))
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_file = os.path.join(screenshot_dir, "failpic_%s.png" % now)
        self.driver.get_screenshot_as_file(screenshot_file)
        logger.info("截图已保存：%s" % screenshot_file)
        return screenshot_file

    def _xpath_text_equals(self, text):
        return "//*[@text=%s]" % self._xpath_literal(text)

    def _xpath_text_contains(self, text):
        literal = self._xpath_literal(text)
        return "//*[contains(@text, %s) or contains(text(), %s)]" % (literal, literal)

    @staticmethod
    def _xpath_literal(value):
        value = str(value)
        if "'" not in value:
            return "'%s'" % value
        if '"' not in value:
            return '"%s"' % value
        parts = value.split("'")
        return "concat(%s)" % ', "\'", '.join("'%s'" % part for part in parts)

    def _wait_one(self, by, value, timeout=None):
        timeout = timeout or self.DEFAULT_TIMEOUT
        return WebDriverWait(self.driver, timeout, self.POLL_FREQUENCY).until(
            EC.visibility_of_element_located((by, value))
        )

    def _wait_all(self, by, value, timeout=None):
        timeout = timeout or self.DEFAULT_TIMEOUT
        return WebDriverWait(self.driver, timeout, self.POLL_FREQUENCY).until(
            EC.visibility_of_all_elements_located((by, value))
        )

    def _capture_after_error(self, error_message):
        logger.error(error_message)
        self.screenshot()

    def _find_with_retry(self, by, value, many=False, retry=0):
        try:
            if many:
                return self._wait_all(by, value)
            return self._wait_one(by, value)
        except TimeoutException as exc:
            if retry < self.MAX_RETRY and self.blackbox():
                logger.info("弹窗处理完成，重新尝试定位元素，第 %s 次重试" % (retry + 1))
                return self._find_with_retry(by, value, many=many, retry=retry + 1)

            message = "元素定位失败：by=%s，value=%s，已达到最大重试次数" % (by, value)
            self._capture_after_error(message)
            raise TimeoutException(message) from exc

    def _exists(self, by, value):
        try:
            self._wait_one(by, value, timeout=3)
            logger.info("元素校验成功")
            return True
        except TimeoutException:
            self._capture_after_error("元素校验失败：by=%s，value=%s，页面未找到可见元素" % (by, value))
            return False

    def find_id(self, element_id):
        return self._exists(AppiumBy.ID, element_id)

    def find_xpath(self, xpath):
        return self._exists(AppiumBy.XPATH, xpath)

    def find_xpath_name(self, name):
        return self._exists(AppiumBy.XPATH, self._xpath_text_equals(name))

    def find_xpath_contains(self, name):
        return self._exists(AppiumBy.XPATH, self._xpath_text_contains(name))

    def find_accessibility_id(self, accessibility_id):
        return self._exists(AppiumBy.ACCESSIBILITY_ID, accessibility_id)

    def find_ios_predicate(self, predicate):
        return self._exists(AppiumBy.IOS_PREDICATE, predicate)

    def find_ios_class_chain(self, class_chain):
        return self._exists(AppiumBy.IOS_CLASS_CHAIN, class_chain)

    def get_id(self, element_id):
        return self._find_with_retry(AppiumBy.ID, element_id)

    def get_ids(self, element_id):
        return self._find_with_retry(AppiumBy.ID, element_id, many=True)

    def get_xpath(self, xpath):
        return self._find_with_retry(AppiumBy.XPATH, xpath)

    def get_xpath_name(self, name):
        return self._find_with_retry(AppiumBy.XPATH, self._xpath_text_equals(name))

    def get_xpath_contains(self, name):
        return self._find_with_retry(AppiumBy.XPATH, self._xpath_text_contains(name))

    def get_className(self, classname):
        return self._find_with_retry(AppiumBy.CLASS_NAME, classname, many=True)

    def get_android_uiautomator(self, uiautomator):
        return self._find_with_retry(AppiumBy.ANDROID_UIAUTOMATOR, uiautomator)

    def get_ios_uiautomator(self, uiautomator):
        return self._find_with_retry(AppiumBy.IOS_UIAUTOMATION, uiautomator)

    def get_accessibility_id(self, accessibility_id):
        return self._find_with_retry(AppiumBy.ACCESSIBILITY_ID, accessibility_id)

    def get_ios_predicate(self, predicate):
        return self._find_with_retry(AppiumBy.IOS_PREDICATE, predicate)

    def get_ios_class_chain(self, class_chain):
        return self._find_with_retry(AppiumBy.IOS_CLASS_CHAIN, class_chain)

    def page(self):
        for _ in range(5):
            if self.find_xpath_name("首页"):
                self.get_xpath_name("首页").click()
                logger.info("已返回首页")
                return True
            self.back()
            self.blackbox()
        logger.error("尝试 5 次后仍未能返回首页")
        return False
