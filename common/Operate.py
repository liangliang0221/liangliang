# -*- coding: utf-8 -*-
from selenium.webdriver import ActionChains

from .BaseOperate import Baseoperate
from .GetYaml import getyaml
from .logs import log


logger = log()


class Operate:
    """执行 YAML 文件描述的 Appium 操作步骤。"""

    def __init__(self, path, driver):
        self.path = path
        self.driver = driver
        self.yaml = getyaml(self.path)
        self.baseoperate = Baseoperate(driver)

    def _resolve_element(self, i):
        return self._resolve_by(self.yaml.get_findtype(i), self.yaml.get_elementinfo(i), self.yaml.get_index(i))

    def _resolve_by(self, find_type, element_info, index=None):
        if not find_type:
            raise ValueError("当前操作需要 find_type，但 YAML 中未填写")

        if find_type == "name":
            return self.baseoperate.get_xpath_name(element_info)
        if find_type == "contains_name":
            return self.baseoperate.get_xpath_contains(element_info)
        if find_type == "id":
            return self.baseoperate.get_id(element_info)
        if find_type == "xpath":
            return self.baseoperate.get_xpath(element_info)
        if find_type == "android_uiautomator":
            return self.baseoperate.get_android_uiautomator(element_info)
        if find_type == "ios_uiautomator":
            return self.baseoperate.get_ios_uiautomator(element_info)
        if find_type == "accessibility_id":
            return self.baseoperate.get_accessibility_id(element_info)
        if find_type == "ios_predicate":
            return self.baseoperate.get_ios_predicate(element_info)
        if find_type == "ios_class_chain":
            return self.baseoperate.get_ios_class_chain(element_info)
        if find_type == "ids":
            elements = self.baseoperate.get_ids(element_info)
            if index is None:
                raise ValueError("find_type=ids 时必须填写 index")
            return elements[index]
        if find_type == "class_name":
            elements = self.baseoperate.get_className(element_info)
            if index is None:
                raise ValueError("find_type=class_name 时必须填写 index")
            return elements[index]

        raise ValueError("未知的 find_type：%s" % find_type)

    def _check_element(self, i):
        find_type = self.yaml.get_findtype(i)
        element_info = self.yaml.get_elementinfo(i)

        if find_type == "id":
            return self.baseoperate.find_id(element_info)
        if find_type == "xpath":
            return self.baseoperate.find_xpath(element_info)
        if find_type == "name":
            return self.baseoperate.find_xpath_name(element_info)
        if find_type == "contains_name":
            return self.baseoperate.find_xpath_contains(element_info)
        if find_type == "accessibility_id":
            return self.baseoperate.find_accessibility_id(element_info)
        if find_type == "ios_predicate":
            return self.baseoperate.find_ios_predicate(element_info)
        if find_type == "ios_class_chain":
            return self.baseoperate.find_ios_class_chain(element_info)

        self._resolve_element(i)
        return True

    def _repeat(self, i, action):
        for _ in range(self.yaml.get_backtimes(i)):
            action()

    def _step_desc(self, i):
        return self.yaml.get_path(i)

    def _step_label(self, i):
        return "%s | %s" % (self.yaml.get_title(), self._step_desc(i))

    def check_operate_type(self):
        logger.info("开始执行 YAML 用例文件：%s，总步骤数：%s" % (self.path, self.yaml.caselen()))
        for i in range(self.yaml.caselen()):
            operate_type = self.yaml.get_operate_type(i)
            desc = self._step_desc(i)
            label = self._step_label(i)
            logger.info("开始执行步骤[%s]：%s，描述：%s" % (i + 1, operate_type, desc))

            try:
                self._execute_step(i, operate_type)
                logger.info("步骤[%s]执行成功，描述：%s" % (i + 1, desc))
            except Exception as exc:
                logger.error(
                    "步骤[%s]执行失败：操作=%s，定位方式=%s，定位值=%s，描述=%s，错误=%s"
                    % (i + 1, operate_type, self.yaml.get_findtype(i), self.yaml.get_elementinfo(i), label, exc)
                )
                raise RuntimeError(
                    "YAML 步骤执行失败：第 %s 步，操作=%s，描述=%s" % (i + 1, operate_type, label)
                ) from exc
        logger.info("YAML 用例文件执行完成：%s" % self.path)

    def _execute_step(self, i, operate_type):
        if operate_type == "click":
            self._resolve_element(i).click()
        elif operate_type == "long_press":
            element = self._resolve_element(i)
            ActionChains(self.driver).click_and_hold(element).pause(self.yaml.get_backtimes(i)).release().perform()
        elif operate_type == "send_keys":
            self._resolve_element(i).send_keys(self.yaml.get_send_content(i))
        elif operate_type == "clear":
            self._resolve_element(i).clear()
        elif operate_type == "back":
            self._repeat(i, self.baseoperate.back)
        elif operate_type == "swipe_up":
            self._repeat(i, self.baseoperate.swipe_up)
        elif operate_type == "swipe_down":
            self._repeat(i, self.baseoperate.swipe_down)
        elif operate_type == "swipe_right":
            self._repeat(i, self.baseoperate.swipe_right)
        elif operate_type == "swipe_left":
            self._repeat(i, self.baseoperate.swipe_left)
        elif operate_type == "keycode":
            self.driver.press_keycode(self.yaml.get_backtimes(i))
            logger.info("Android keycode 输入成功")
        elif operate_type == "sleep":
            self._repeat(i, self.baseoperate.sleep)
        elif operate_type == "check":
            if not self._check_element(i):
                logger.error("元素校验失败，已跳过当前 check 步骤并继续执行后续步骤")
        elif operate_type == "element_swipe":
            index = self.yaml.get_index(i)
            start_el = self._resolve_by(self.yaml.get_findtype(i), self.yaml.get_elementinfo(i), index)
            end_el = self._resolve_by(self.yaml.get_end_findtype(i), self.yaml.get_end_elementinfo(i), index)
            self.driver.scroll(start_el, end_el, duration=500)
            logger.info("元素之间滑动成功")
        elif operate_type == "swipe_px":
            self._repeat(
                i,
                lambda: self.baseoperate.swipe_px(
                    self.yaml.get_elementinfo(i),
                    self.yaml.get_findtype(i),
                    self.yaml.get_end_elementinfo(i),
                    self.yaml.get_end_findtype(i),
                ),
            )
        elif operate_type == "swipe_pt":
            self._repeat(
                i,
                lambda: self.baseoperate.swipe_pt(
                    self.yaml.get_elementinfo(i),
                    self.yaml.get_findtype(i),
                    self.yaml.get_end_elementinfo(i),
                    self.yaml.get_end_findtype(i),
                ),
            )
        else:
            raise ValueError("未知的 operate_type：%s" % operate_type)
