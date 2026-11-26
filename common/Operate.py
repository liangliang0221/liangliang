# -*-coding: utf-8 -*-
# @Time    : 2023/10/31 16:26
# @Author  : zhenhai
# @File    : Operate.py
# @Software: PyCharm

'''
读取yaml信息并执行
element_info：定位元素信息：八大元素数据+组合定位
find_type：定位元素属性：id、xpath、name（常规匹配文本）、ids（id、classname的序列）
operate_type: 定位元素行为操作：click、click_if_exist（存在则点击，不存在则跳过）、back（返回）、swipe_up（上滑） 、swipe_down（下滑）、sleep(睡眠)、check（校验）等
以上三个为必填项

send_content：send_keys 时用到，用于输入内容
index：ids、classname时用到，用于输入第几序列
times:back、swipe_up等时用到，用于输入次数
'''

from .GetYaml import getyaml
from .BaseOperate import Baseoperate
from .logs import log
# from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver import ActionChains
from appium.webdriver.common.appiumby import AppiumBy


class Operate:
    """
    用于读取 yaml 数据驱动用例并执行对应的 Appium 操作。

    该类会遍历 yaml 中 `testcase` 列表，根据 `operate_type` 决定执行点击、输入、滑动、校验等动作，
    再依据 `find_type` 选择不同定位方式（id/xpath/name/组合定位等）。
    """
    def __init__(self, path, driver):
        """
        初始化执行器。

        Args:
            path: yaml 用例文件路径（相对 `common/` 或按项目约定传入）
            driver: Appium WebDriver 实例
        """
        self.path = path
        self.driver = driver
        self.yaml = getyaml(self.path)
        self.baseoperate = Baseoperate(driver)

    def _resolve_element(self, i):
        """
        根据 yaml 的 `find_type` / `element_info` /（必要时的）`index` 解析出目标元素。

        Args:
            i: testcase 下标

        Returns:
            WebElement: 一个可直接用于 click/send_keys/clear/TouchAction 的元素
        """
        info = self.yaml.get_elementinfo(i)
        find_type = self.yaml.get_findtype(i)

        if find_type == 'name':
            return self.baseoperate.get_xpath_name(info)
        elif find_type == 'contains_name':
            return self.baseoperate.get_xpath_contains(info)
        elif find_type == 'id':
            return self.baseoperate.get_id(info)
        elif find_type == 'xpath':
            return self.baseoperate.get_xpath(info)
        elif find_type == 'android_uiautomator':
            return self.baseoperate.get_android_uiautomator(info)
        elif find_type == 'ids':
            return self.baseoperate.get_ids(info)[self.yaml.get_index(i)]
        elif find_type == 'class_name':
            return self.baseoperate.get_className(info)[self.yaml.get_index(i)]

        raise ValueError("未知 find_type: %s" % find_type)

    def _resolve_scroll_element(self, find_type, element_info, index):
        """
        element_swipe 场景的元素解析器（同时支持起点/终点）。

        Args:
            find_type: yaml 的 find_type（name/contains_name/id/xpath/android_uiautomator/ids/class_name）
            element_info: yaml 对应的 element_info 或 end_element_info
            index: ids/class_name 的序号（从 yaml 的 index 字段获取）

        Returns:
            WebElement 或者在 index 缺失时返回元素列表（尽量保持兼容）
        """
        if find_type == 'name':
            return self.baseoperate.get_xpath_name(element_info)
        elif find_type == 'contains_name':
            return self.baseoperate.get_xpath_contains(element_info)
        elif find_type == 'id':
            return self.baseoperate.get_id(element_info)
        elif find_type == 'xpath':
            return self.baseoperate.get_xpath(element_info)
        elif find_type == 'android_uiautomator':
            return self.baseoperate.get_android_uiautomator(element_info)
        elif find_type == 'ids':
            elements = self.baseoperate.get_ids(element_info)
            return elements[index] if index is not None else elements
        elif find_type == 'class_name':
            elements = self.baseoperate.get_className(element_info)
            return elements[index] if index is not None else elements
        raise ValueError("未知 find_type: %s" % find_type)

    def _find_if_exist(self, find_type, element_info, index=None):
        """
        轻量判断元素是否存在（不走 blackbox、不截图、不做长等待）。

        Args:
            find_type: yaml 的 find_type
            element_info: yaml 的 element_info
            index: ids/class_name 时的序号

        Returns:
            WebElement: 存在则返回第一个元素
            None: 不存在
        """
        if find_type == 'name':
            by, value = AppiumBy.XPATH, "//*[@text='%s']" % element_info
        elif find_type == 'contains_name':
            by, value = AppiumBy.XPATH, "//*[contains(@text,'%s')]" % element_info
        elif find_type == 'id':
            by, value = AppiumBy.ID, element_info
        elif find_type == 'xpath':
            by, value = AppiumBy.XPATH, element_info
        elif find_type == 'android_uiautomator':
            by, value = AppiumBy.ANDROID_UIAUTOMATOR, element_info
        elif find_type in ('ids', 'class_name'):
            by = AppiumBy.ID if find_type == 'ids' else AppiumBy.CLASS_NAME
            elements = self.driver.find_elements(by, element_info)
            if not elements:
                return None
            return elements[index or 0]
        else:
            raise ValueError("未知 find_type: %s" % find_type)

        elements = self.driver.find_elements(by, value)
        return elements[0] if elements else None


    def check_operate_type(self):
        """
        按 yaml 配置执行全部步骤。

        流程：
        1. 遍历 `self.yaml.caselen()` 条 testcase
        2. 根据 `operate_type` 分发执行（click/click_if_exist/long_press/send_keys/clear/back/swipe_*/sleep/keycode/check/element_swipe 等）
        3. 根据 `find_type` 使用 `Baseoperate` 提供的定位封装

        Raises:
            Exception: 当元素无法识别或执行失败时抛出（例如点击/长按/输入/清除等分支）。
        """

        for i in range(self.yaml.caselen()):
            path = self.yaml.get_path(i)
            body = self.yaml.get_title()
            log_success = ('操作：' + str(path))
            log_lose = ('执行失败：文件位置：' + str(body) + ',' + '操作：' + str(path))

            # 元素点击操作逻辑
            if self.yaml.get_operate_type(i) == 'click':
                # 隐式等待3s
                self.driver.implicitly_wait(3)
                try:
                    log().info(log_success)
                    self._resolve_element(i).click()
                except Exception:
                    log().error(log_lose)
                    raise

            # 元素存在则点击，不存在则跳过该步骤（用于可选入口/引导页）
            elif self.yaml.get_operate_type(i) == 'click_if_exist':
                self.driver.implicitly_wait(3)
                try:
                    element = self._find_if_exist(
                        self.yaml.get_findtype(i), self.yaml.get_elementinfo(i), self.yaml.get_index(i)
                    )
                except Exception:
                    element = None
                if element is None:
                    log().warn('元素不存在，跳过该步骤：' + str(path))
                else:
                    try:
                        log().info(log_success)
                        element.click()
                    except Exception:
                        log().error(log_lose)
                        raise

            # 元素长按操作逻辑
            elif self.yaml.get_operate_type(i) == 'long_press':
                try:
                    log().info(log_success)
                    el = self._resolve_element(i)
                    ActionChains(self.driver).click_and_hold(el=el, duration=self.yaml.get_backtimes(i)).perform()
                except Exception:
                    log().error(log_lose)
                    raise

            # 元素输入文本内容逻辑
            elif self.yaml.get_operate_type(i) == 'send_keys':
                self.driver.implicitly_wait(3)
                try:
                    log().info(log_success)
                    self._resolve_element(i).send_keys(self.yaml.get_send_content(i))
                except Exception:
                    log().error(log_lose)
                    raise

            # 元素清除本文内容逻辑
            elif self.yaml.get_operate_type(i) == 'clear':
                self.driver.implicitly_wait(3)
                try:
                    log().info(log_success)
                    self._resolve_element(i).clear()
                except Exception:
                    log().error(log_lose)
                    raise

            # 返回逻辑
            elif self.yaml.get_operate_type(i) == 'back':
                for n in range(self.yaml.get_backtimes(i)):
                    self.baseoperate.back()

            # 上滑逻辑
            elif self.yaml.get_operate_type(i) == 'swipe_up':
                for n in range(self.yaml.get_backtimes(i)):
                    self.baseoperate.swipe_up()

            # 下滑逻辑
            elif self.yaml.get_operate_type(i) == 'swipe_down':
                for n in range(self.yaml.get_backtimes(i)):
                    self.baseoperate.swipe_down()

            # 右滑逻辑
            elif self.yaml.get_operate_type(i) == 'swipe_right':
                for n in range(self.yaml.get_backtimes(i)):
                    self.baseoperate.swipe_right()

            # 左滑逻辑
            elif self.yaml.get_operate_type(i) == 'swipe_left':
                for n in range(self.yaml.get_backtimes(i)):
                    self.baseoperate.swipe_left()

            # 键盘输入逻辑，可根据键盘键码keyCode表进行输入
            elif self.yaml.get_operate_type(i) == 'keycode':
                try:
                    log().info(log_success)
                    self.driver.press_keycode(self.yaml.get_backtimes(i))
                except:
                    log().error(log_lose)
                    raise Exception("此处为自定义错误(键盘输入)，表明无法识别页面元素，common.operate")

            # 强制睡眠逻辑
            elif self.yaml.get_operate_type(i) == 'sleep':
                for n in range(self.yaml.get_backtimes(i)):
                    self.baseoperate.sleep()

            # 页面校验逻辑
            elif self.yaml.get_operate_type(i) == 'check':
                # 校验
                self.driver.implicitly_wait(3)
                if self.yaml.get_findtype(i) == 'id':
                    self.baseoperate.find_id(self.yaml.get_elementinfo(i))
                elif self.yaml.get_findtype(i) == 'xpath':
                    self.baseoperate.find_xpath(self.yaml.get_elementinfo(i))
                elif self.yaml.get_findtype(i) == 'name':
                    self.baseoperate.find_xpath_name(self.yaml.get_elementinfo(i))
                elif self.yaml.get_findtype(i) == 'contains_name':
                    self.baseoperate.find_xpath_contains(self.yaml.get_elementinfo(i))

            # 元素元素之间滑动逻辑
            elif self.yaml.get_operate_type(i) == 'element_swipe':
                # 元素之间滑动逻辑
                # 隐式等待3s，待处理
                self.driver.implicitly_wait(3)
                try:
                    log().info(log_success)

                    start_find_type = self.yaml.get_findtype(i)
                    end_find_type = self.yaml.get_end_findtype(i)
                    index = self.yaml.get_index(i)

                    start_el = self._resolve_scroll_element(
                        start_find_type, self.yaml.get_elementinfo(i), index
                    )
                    end_el = self._resolve_scroll_element(
                        end_find_type, self.yaml.get_end_elementinfo(i), index
                    )
                    self.driver.scroll(start_el, end_el, duration=500)
                except:
                    log().error(log_lose)
                    raise Exception("此处为自定义错误（元素之间滑动），表明无法识别页面元素，common.operate")

            # 坐标与坐标之间滑动逻辑
            elif self.yaml.get_operate_type(i) == 'swipe_px':
                # 坐标之间滑动逻辑
                # 隐式等待3s，待处理
                self.driver.implicitly_wait(3)
                try:
                    for n in range(self.yaml.get_backtimes(i)):
                        log().info(log_success)
                        self.baseoperate.swipe_px(self.yaml.get_elementinfo(i),self.yaml.get_findtype(i),self.yaml.get_end_elementinfo(i),self.yaml.get_end_findtype(i))
                except:
                    log().error(log_lose)
                    raise Exception("此处为自定义错误（坐标之间滑动异常_px），common.operate")

            # 页面百分比之间滑动逻辑
            elif self.yaml.get_operate_type(i) == 'swipe_pt':
                # 百分比之间滑动逻辑
                # 隐式等待3s，待处理
                self.driver.implicitly_wait(3)
                try:
                    for n in range(self.yaml.get_backtimes(i)):
                        log().info(log_success)
                        self.baseoperate.swipe_pt(self.yaml.get_elementinfo(i),self.yaml.get_findtype(i),self.yaml.get_end_elementinfo(i),self.yaml.get_end_findtype(i))
                except:
                    log().error(log_lose)
                    raise Exception("此处为自定义错误（坐标之间滑动异常_pt），common.operate")


# if __name__ == "__main__":
#     import GetDriver
#     driver = GetDriver.mydriver()
#     path = "../testyaml/cm/cm-001addcm.yaml"
#
#     cm = Operate(path,driver)
#     cm.check_operate_type()
#     cm.back_home()