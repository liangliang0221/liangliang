# -*-coding: utf-8 -*-
# @Time    : 2023/10/31 16:25
# @Author  : zhenhai
# @File    : BaseOperate.py
# @Software: PyCharm

from selenium.webdriver.support.ui import WebDriverWait
import os
import sys

# 让脚本直接运行时也能找到 common 包（sys.path[0] 会变成 common/，需要补上项目根目录）
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from common.logs import log
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC

log = log()

class Baseoperate:
    """
    基础封装层：对 Appium/Selenium WebDriver 的常用能力进行二次封装。

    主要能力包括：
    - `back`：通过 adb 触发返回键
    - `blackbox`：弹窗黑名单扫描与关闭
    - `swipe_*` / `sleep`：滑动与等待
    - `screenshot`：截图保存
    - `find_*` / `get_*`：元素存在性校验与元素获取
    - `page`：尝试返回到首页
    """

    def __init__(self, driver):
        """
        初始化 Baseoperate。

        Args:
            driver: Appium WebDriver 实例。
        """
        self.driver = driver

    def back(self):
        """
        通过 adb 模拟 Android 返回键（keyevent 4）。
        """
        try:
            time.sleep(1)
            os.popen("adb shell input keyevent 4")
            log.info("返回操作正常")
        except:
            log.error("返回操作异常")

    # 弹窗黑名单 — 按你的 App 实际弹窗补充即可
    _BLACKLIST = [
        (AppiumBy.XPATH, '//*[@text="允许"]'),
        (AppiumBy.XPATH, '//*[@text="确定"]'),
        (AppiumBy.XPATH, '//*[@text="取消"]'),
        (AppiumBy.XPATH, '//*[@text="登录"]'),
        (AppiumBy.XPATH, '//*[@text="稍后"]'),
    ]

    def blackbox(self):
        """重复扫描并关闭弹窗，直到屏幕干净；关到过则 return，否则截图+raise。"""
        log.info("开始扫描弹窗...")
        closed_any = False
        rounds = 0
        # 每关完一个弹窗就从头重扫，直到整轮一个都没找到（屏幕干净）
        while rounds < 5:
            rounds += 1
            found_in_this_round = False
            for by, val in self._BLACKLIST:
                try:
                    eles = self.driver.find_elements(by, val)
                    if eles:
                        eles[0].click()
                        log.info(f"已关闭弹窗: {val}")
                        found_in_this_round = closed_any = True
                        break  # 关完这一个就跳出内层，从头再扫一轮
                except Exception:
                    continue
            if not found_in_this_round:
                break  # 这一轮啥都没找到 → 清干净了

        if closed_any:
            return

        self.screenshot()
        log.error("未检测到已知弹窗")
        raise Exception("blackbox 未发现弹窗")

    '''
    以下封装函数主要用于长按、长按滑动等操作
    '''

    def get_window_size(self):
        """
        获取当前设备窗口宽高。

        Returns:
            tuple(int, int): (width, height)
        """
        # 获取屏幕大小
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return x, y

    def swipe_up(self):
        """
        向上滑动：在屏幕中心附近从下方向上滑动。
        """
        try:
            l = self.get_window_size()
            x1 = int(l[0] * 0.5)
            y1 = int(l[1] * 0.9)
            y2 = int(l[1] * 0.2)
            self.driver.swipe(x1, y1, x1, y2, duration=500)
            time.sleep(1)
            log.info("向上滑动正常")
        except:
            log.error('向上滑动异常')

    def swipe_down(self):
        """
        向下滑动：在屏幕中心附近从上方向下滑动。
        """
        try:
            l = self.get_window_size()
            x1 = int(l[0] * 0.5)
            y1 = int(l[1] * 0.2)
            y2 = int(l[1] * 0.9)
            self.driver.swipe(x1, y1, x1, y2, duration=500)
            time.sleep(1)
            log.info("向下滑动正常")
        except:
            log.error("向下滑动异常")

    def swipe_right(self):
        """
        向右滑动：在屏幕中线附近从左向右滑动。
        """
        try:
            l = self.get_window_size()
            x1 = int(l[0] * 0.2)
            x2 = int(l[0] * 0.8)
            y1 = int(l[1] * 0.5)
            self.driver.swipe(x1, y1, x2, y1, duration=500)
            time.sleep(1)
            log.info('向右滑动正常')
        except:
            log.error('向右滑动异常')

    def swipe_left(self):
        """
        向左滑动：在屏幕中线附近从右向左滑动。
        """
        try:
            l = self.get_window_size()
            x1 = int(l[0] * 0.8)
            x2 = int(l[0] * 0.2)
            y1 = int(l[1] * 0.5)
            self.driver.swipe(x1, y1, x2, y1, duration=500)
            time.sleep(1)
            log.info("向左滑动正常")
        except:
            log.error("向左滑动异常")

    def swipe_px(self,star_x,star_y,end_x,end_y):
        """
        使用绝对坐标进行滑动（PX）。

        Args:
            star_x/star_y: 起点坐标
            end_x/end_y: 终点坐标
        """
        try:
            l=self.get_window_size()
            self.driver.swipe(star_x,star_y,end_x,end_y,duration =500)
            time.sleep(1)
            log.info('坐标（PX）滑动正常')
        except:
            log.error('请检查坐标输入是否正确')

    def swipe_pt(self,star_x,star_y,end_x,end_y):
        """
        使用百分比坐标进行滑动（PT）。

        Args:
            star_x/star_y/end_x/end_y: 百分比值（相对宽/高），例如 0.5 表示 50%。
        """
        try:
            l = self.get_window_size()
            x1 = int(l[0] * star_x)
            x2 = int(l[0] * star_y)
            y1 = int(l[1] * end_x)
            y2 = int(l[1] * end_y)
            self.driver.swipe(x1, y1, x2, y2, duration=500)
            time.sleep(1)
            log.info("百分比（PT）滑动正常")
        except:
            log.error('请检查坐标输入是否正确')

    def sleep(self):
        """
        强制等待 5 秒。
        """
        try:
            time.sleep(5)
            log.info("強制等待5S")
        except:
            log.error("強制等待錯誤")

    def screenshot(self):
        """
        截图当前页面并保存为 png 文件。

        保存路径：`common/../log/screenshoot/failpic_{时间戳}.png`
        """
        now = time.strftime("%y%m%d-%H-%M-%S")
        PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
        screenshoot_path = PATH('../log/screenshoot/failpic_')
        self.driver.get_screenshot_as_file(screenshoot_path + now + '.png')

    def find_id(self, id):
        """
        判断页面上是否存在并显示指定 `id` 对应的元素。

        Args:
            id: 元素的 resource-id 字符串

        Returns:
            bool: 存在且可见则 True，否则 False
        """
        try:
            self.driver.find_element(AppiumBy.ID,id).is_displayed()
            log.info('当前页面存在此元素：' + '%s' % id)
            return True
        except:
            self.screenshot()
            log.error('当前页面不存在此元素：' + '%s' % id)
            return False

    def find_xpath(self, xpath):
        """
        判断页面上是否存在并显示指定 xpath 对应的元素。

        Args:
            xpath: xpath 定位表达式

        Returns:
            bool: 存在且可见则 True，否则 False
        """
        try:
            self.driver.find_element(AppiumBy.XPATH,xpath).is_displayed()
            log.info('当前页面存在此元素：' + '%s' % xpath)
            return True
        except:
            self.screenshot()
            log.error('当前页面不存在此元素：' + '%s' % xpath)
            return False

    def find_xpath_name(self, name):
        """
        通过文本精确匹配（`//*[@text='...']`）判断元素是否存在并可见。

        Args:
            name: 需要匹配的文本内容

        Returns:
            bool: 存在且可见则 True，否则 False
        """

        findname = "//*[@text='%s']" % (name)
        try:
            self.driver.find_element(AppiumBy.XPATH,findname).is_displayed()
            log.info('当前页面存在此元素：' + '%s' % name)
            return True
        except:
            self.screenshot()
            log.error('当前页面不存在此元素：' + '%s' % name)
            return False

    def find_xpath_contains(self, name):
        """
        通过文本模糊匹配（xpath contains）判断元素是否存在并可见。

        Args:
            name: 需要包含匹配的文本片段

        Returns:
            bool: 存在且可见则 True，否则 False
        """

        findname = "//*[@contains(text(),'%s']" % (name)
        try:
            self.driver.find_element(AppiumBy.XPATH,findname).is_displayed()
            log.info('当前页面存在此元素：' + '%s' % name)
            return True
        except:
            self.screenshot()
            log.error('当前页面不存在此元素：' + '%s' % name)
            return False

    def get_id(self, id):
        """
        定位页面 `id` 元素并返回 WebElement。

        定位失败时：
        1. 先尝试 blackbox（扫弹窗关闭）
        2. blackbox 还失败则直接 raise（交给上层 Operate 处理）

        Args:
            id: 元素的 resource-id 字符串
        Returns:
            WebElement
        Raises:
            Exception: 定位+弹窗清理都失败
        """
        try:
            WebDriverWait(self.driver, 20, 1).until(EC.visibility_of_element_located((AppiumBy.ID, id)))
            log.info('成功定位元素：' + '%s' % id)
            return self.driver.find_element(AppiumBy.ID, id)
        except Exception:
            try:
                self.blackbox()
                # blackbox 关完弹窗，再重试一次（只试一次，不再递归）
                WebDriverWait(self.driver, 5, 1).until(EC.visibility_of_element_located((AppiumBy.ID, id)))
                return self.driver.find_element(AppiumBy.ID, id)
            except Exception:
                log.error('定位失败：' + '%s' % id)
                raise


    def get_ids(self, id):
        """定位一组页面 id 元素并返回列表（非递归：失败 raise）"""
        try:
            WebDriverWait(self.driver, 20, 1).until(EC.visibility_of_all_elements_located((AppiumBy.ID, id)))
            elements = self.driver.find_elements(AppiumBy.ID, id)
            log.info('成功定位到元素：' + '%s' % id)
            return elements
        except Exception:
            try:
                self.blackbox()
                WebDriverWait(self.driver, 5, 1).until(EC.visibility_of_all_elements_located((AppiumBy.ID, id)))
                return self.driver.find_elements(AppiumBy.ID, id)
            except Exception:
                log.error('定位失败：' + '%s' % id)
                raise


    def get_xpath(self, xpath):
        """定位页面 xpath 元素并返回 WebElement（非递归：失败 raise）"""
        try:
            WebDriverWait(self.driver, 20, 1).until(EC.visibility_of_element_located((AppiumBy.XPATH, xpath)))
            element = self.driver.find_element(AppiumBy.XPATH, xpath)
            log.info('成功定位到元素：' + '%s' % xpath)
            return element
        except Exception:
            try:
                self.blackbox()
                WebDriverWait(self.driver, 5, 1).until(EC.visibility_of_element_located((AppiumBy.XPATH, xpath)))
                return self.driver.find_element(AppiumBy.XPATH, xpath)
            except Exception:
                log.error('定位失败：' + '%s' % xpath)
                raise


    def get_xpath_name(self, name):
        """使用 xpath 文本精确匹配定位页面元素（非递归：失败 raise）"""
        findname = "//*[@text='%s']" % name
        try:
            WebDriverWait(self.driver, 20, 1).until(EC.visibility_of_element_located((AppiumBy.XPATH, findname)))
            element = self.driver.find_element(AppiumBy.XPATH, findname)
            log.info('成功定位元素：' + '%s' % name)
            return element
        except Exception:
            try:
                self.blackbox()
                WebDriverWait(self.driver, 5, 1).until(EC.visibility_of_element_located((AppiumBy.XPATH, findname)))
                return self.driver.find_element(AppiumBy.XPATH, findname)
            except Exception:
                log.error('定位失败：' + '%s' % name)
                raise


    def get_xpath_contains(self, name):
        """使用 xpath 文本模糊匹配定位页面元素（非递归：失败 raise）"""
        findname = "//*[@contains(text(),'%s']" % (name)
        try:
            WebDriverWait(self.driver, 20, 1).until(EC.visibility_of_element_located((AppiumBy.XPATH, findname)))
            element = self.driver.find_element(AppiumBy.XPATH, findname)
            log.info('成功定位元素：' + '%s' % name)
            return element
        except Exception:
            try:
                self.blackbox()
                WebDriverWait(self.driver, 5, 1).until(EC.visibility_of_element_located((AppiumBy.XPATH, findname)))
                return self.driver.find_element(AppiumBy.XPATH, findname)
            except Exception:
                log.error('定位失败：' + '%s' % name)
                raise

    def get_className(self, classname):
        """定位 className 元素并返回列表（非递归：失败 raise）"""
        try:
            WebDriverWait(self.driver, 20, 1).until(EC.visibility_of_element_located((AppiumBy.CLASS_NAME, classname)))
            element = self.driver.find_elements(AppiumBy.CLASS_NAME, classname)
            log.info('成功定位元素：' + '%s' % classname)
            return element
        except Exception:
            try:
                self.blackbox()
                WebDriverWait(self.driver, 5, 1).until(EC.visibility_of_element_located((AppiumBy.CLASS_NAME, classname)))
                return self.driver.find_elements(AppiumBy.CLASS_NAME, classname)
            except Exception:
                log.error('定位失败：' + '%s' % classname)
                raise

    def get_android_uiautomator(self, uiautomator):
        """使用 Android UIAutomator 表达式定位元素（非递归：失败 raise）"""
        try:
            WebDriverWait(self.driver, 20, 1).until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, uiautomator)))
            element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, uiautomator)
            log.info('成功定位元素：' + '%s' % uiautomator)
            return element
        except Exception:
            try:
                self.blackbox()
                WebDriverWait(self.driver, 5, 1).until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, uiautomator)))
                return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, uiautomator)
            except Exception:
                log.error('定位失败：' + '%s' % uiautomator)
                raise

    def get_ios_uiautomator(self, uiautomator):
        """使用 iOS UIAutomation 表达式定位元素（非递归：失败 raise）"""
        try:
            WebDriverWait(self.driver, 20, 1).until(EC.visibility_of_element_located((AppiumBy.IOS_UIAUTOMATION, uiautomator)))
            element = self.driver.find_element(AppiumBy.IOS_UIAUTOMATION, uiautomator)
            log.info('成功定位元素：' + '%s' % uiautomator)
            return element
        except Exception:
            try:
                self.blackbox()
                WebDriverWait(self.driver, 5, 1).until(EC.visibility_of_element_located((AppiumBy.IOS_UIAUTOMATION, uiautomator)))
                return self.driver.find_element(AppiumBy.IOS_UIAUTOMATION, uiautomator)
            except Exception:
                log.error('定位失败：' + '%s' % uiautomator)
                raise


    def page(self):
        """
        尝试返回到应用的一级页面（“首页”）。

        该方法会最多尝试 5 次：
        - 如果检测到首页关键元素可见，则点击进入首页并结束
        - 否则触发 adb 返回键，同时在返回过程中扫描并关闭可能的弹窗
        """
        blacklist=[
                      (AppiumBy.XPATH, '//*[@text="不等了"]')
                      ]
        i = 0
        while i < 5:
            i = i + 1
            findname = self.find_xpath_name('首頁')
            if findname:
                log.info("点击一级页面-首页")
                self.driver.find_element(AppiumBy.XPATH, '//*[@text="首頁"]').click()
                # self.driver.implicitly_wait(2)
                log.info('已返回至当前应用一级界面-首页')
                break
            else:
                log.info("进行返回上一级页面操作")
                os.popen("adb shell input keyevent 4")
                for black in blacklist:
                    log.info("扫描是否受彈窗影響")
                    eles = self.driver.find_elements(*black)
                    # 大于0，则进行点击操作，等于0，则继续遍历
                    if len(eles) > 0:
                        eles[0].click()
                        log.info("成功关闭一个弹窗,继续进行返回邏輯操作")
                continue


    # def get_path(self, path):
    #     """
    #     用于返回操作行为
    #     """
    #     self.path = path
    #     return path


    # def getids_text(self, id):
    #     """
    #     定位页面resouce-id元素组
    #     :param id:
    #     :return:列表
    #     """
    #     try:
    #         elements = WebDriverWait(self.driver, 20).until(lambda x: x.find_elements_by_id(id))
    #         self.driver.implicitly_wait(2)
    #         log.info('成功定位元素：' + '%s' % id)
    #         return elements
    #     except:
    #         self.screenshot()
    #         log.error('未定位到元素：' + '%s' % id)



    # def get_id_closebox(self, id):
    #     """
    #     专门关闭弹框的
    #     :param id:
    #     :return:
    #     """
    #     try:
    #         # elements = self.driver.find_elements_by_id(id)
    #         element = WebDriverWait(self.driver, 20).until(lambda x: x.find_element_by_id(id))
    #         self.driver.implicitly_wait(2)
    #         return element
    #     except:
    #         pass
    #
    # def get_text_closebox(self, name):
    #     """
    #     专门关闭弹框的
    #     :param :text
    #     :return:
    #     """
    #     findname = "//*[@text='%s']" % name
    #     try:
    #         # element = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_xpath(xpath))
    #         WebDriverWait(self.driver, 20).until(lambda driver: driver.find_element_by_id(findname).is_displayed())
    #         element = self.driver.find_element_by_id(findname)
    #         return element
    #     except:
    #         pass


    #
    # def get_classname(self, classname):
    #     """
    #     定位页面xpath元素
    #     :param id:
    #     :return:
    #     """
    #     try:
    #         elements = WebDriverWait(self.driver, 20).until(lambda x: x.find_elements_by_class_name(classname))
    #         self.driver.implicitly_wait(2)
    #         log.info('成功定位到元素：' + '%s' % classname)
    #         return elements
    #     except:
    #         # self.screenshot()
    #         log.error('未定位到元素：' + '%s' % classname)


    #
    # def get_webcss(self, css):
    #
    #     # 此处还需要进行改动操作
    #
    #     """
    #            定位约单的web页面
    #            :param id:
    #            :return:
    #     """
    #     try:
    #         self.driver.execute(MobileCommand.SWITCH_TO_CONTEXT, {"name": "WEBVIEW_com.yuedan"})
    #         WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element_by_css_selector(css).is_displayed())
    #         element = self.driver.find_element_by_css_selector(css)
    #         element.click()
    #         self.driver.execute(MobileCommand.SWITCH_TO_CONTEXT, {"name": "NATIVE_APP"})
    #     except:
    #         # self.screenshot()
    #         # self.driver.get_screenshot_as_file("D:/error.png")
    #         log.error('未定位到元素：' + '%s' % id)
    #
    # def get_webcss_list(self, css, random):
    #     """
    #            定位约单的web页面,
    #            :param id:
    #            :return:list
    #     """
    #     try:
    #         self.driver.execute(MobileCommand.SWITCH_TO_CONTEXT, {"name": "WEBVIEW_com.yuedan"})
    #         elements = WebDriverWait(self.driver, 20).until(lambda x: x.find_elements_by_css_selector(css))
    #         elements[random].click()
    #         self.driver.execute(MobileCommand.SWITCH_TO_CONTEXT, {"name": "NATIVE_APP"})
    #     except:
    #         # self.screenshot()
    #         # self.driver.get_screenshot_as_file("D:/error.png")
    #         log.error('未定位到元素：' + '%s' % id)



