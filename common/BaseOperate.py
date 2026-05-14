# -*-coding: utf-8 -*-
# @Time    : 2026/05/13
# @Author  : liangliang
# @File    : BaseOperate.py
# @Software: PyCharm

from selenium.webdriver.support.ui import WebDriverWait
from common.logs import log
import time
import os
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

    def blackbox(self):
        """
        弹窗黑名单扫描并关闭。

        会遍历内置黑名单定位器，找到第一个匹配元素即点击关闭并中断。
        若未找到弹窗元素，则调用 `page()` 尝试回到首页并抛出异常。
        """
        # 弹窗黑名单处理逻辑，调用时遍历弹窗并进行关闭操作，如当前弹窗都没有则返回报错
        black_list = [
                      (AppiumBy.XPATH, '//*[@text="登入"]'),
                      (AppiumBy.XPATH, '//*[@text="確定"]'),
                      (AppiumBy.XPATH, '//*[@text="取消"]'),
                      (AppiumBy.XPATH, '//*[@text="允許"]'),
                    #   (AppiumBy.ID, 'com.cwj.hsing:id/lyContent'),
                    #   (AppiumBy.ID, 'com.cwj.hsing:id/sign_tv'),
                    #   (AppiumBy.ID, 'com.android.permissioncontroller:id/permission_allow_foreground_only_button'),
                    #   (AppiumBy.XPATH, '//*[@resource-id="com.android.permissioncontroller:id/permission_allow_button"]'),
                    #   (AppiumBy.XPATH, '//androidx.compose.ui.platform.ComposeView/android.view.View[1]/android.view.View[1]/android.view.View[1]'),
                    #   (AppiumBy.XPATH, '//*[@resource-id="com.cwj.hsing:id/close"]'),
                    #   (AppiumBy.XPATH, '//*[@resource-id="showSignInPop"]/android.view.View[1]/android.widget.TextView[6]'),
                    #   (AppiumBy.XPATH, '//androidx.compose.ui.platform.ComposeView/android.view.View[1]/android.view.View[1]'),
                    #   (AppiumBy.XPATH,'//*[@resource-id="com.android.permissioncontroller:id/permission_allow_button"]')
                      ]
        log.info("没有定位到页面元素，将进行弹窗识别并关闭操作")
        try:
            i = 0
            for black in black_list:
                log.info("扫描弹窗ing,请等待...")
                eles = self.driver.find_elements(*black)
                if len(eles) > 0:
                    eles[0].click()
                    log.info("成功关闭一个弹窗,继续进行下一步操作")
                    i += 1
                    break
            if(i!=1):
                log.error("扫描结束，未定位到元素，将返回至首页并结束！！！")
                self.page()
                raise Exception('非弹窗问题')
        except:
            # # 截图+日志+报错
            self.screenshot()
            log.error('发生错误，可能是弹窗元素遍历问题，也可能为非弹窗问题')
            raise Exception('终止下一步操作')

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

        该方法会使用显式等待确保元素“可见”，定位失败时会触发 `blackbox()` 处理可能的弹窗干扰，
        并递归重试直到成功或异常被上层处理。

        Args:
            id: 元素的 resource-id 字符串

        Returns:
            AppiumBy 对应定位到的 WebElement
        """
        try:
            # 显性等待20s，每1s进行检查是否存在，用在判断,来查找页面是否存在id元素并检查元素对用户是否可见
            # WebDriverWait(self.driver, 20, 1).until(EC.visibility_of_element_located((AppiumBy.ID,id)))
            WebDriverWait(self.driver,20,1).until(EC.visibility_of_element_located((AppiumBy.ID,id)))
            log.info('成功定位元素：' + '%s' % id)
            element = self.driver.find_element(AppiumBy.ID,id)
            return element
        except:
            self.blackbox()
            return self.get_id(id)


    def get_ids(self, id):
        """
        定位一组页面 `id` 元素并返回 WebElement 列表。

        该方法会使用显式等待确保“全部元素”可见；定位失败时会触发 `blackbox()` 处理弹窗干扰，
        然后递归重试。

        Args:
            id: 元素的 resource-id

        Returns:
            list: WebElement 列表
        """
        try:
            WebDriverWait(self.driver, 20, 1).until(EC.visibility_of_all_elements_located((AppiumBy.ID, id)))
            elements =self.driver.find_elements(AppiumBy.ID,id)
            log.info('成功定位到元素：' + '%s' % id)
            return elements
        except:
            self.blackbox()
            return self.get_ids(id)


    def get_xpath(self, xpath):
        """
        定位页面 xpath 元素并返回 WebElement。

        该方法会使用显式等待确保元素“可见”；定位失败时触发 `blackbox()` 关闭可能的弹窗干扰，
        并递归重试。

        Args:
            xpath: xpath 定位表达式

        Returns:
            AppiumBy 对应定位到的 WebElement
        """
        try:
            # element = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_xpath(xpath))
            # 显性等待20s，每1s进行检查是否存在，用在判断,来查找页面是否存在xpath元素并检查元素对用户是否可见
            WebDriverWait(self.driver, 20, 1).until(EC.visibility_of_element_located((AppiumBy.XPATH,xpath)))
            element = self.driver.find_element(AppiumBy.XPATH,xpath)
            log.info('成功定位到元素：' + '%s' % xpath)
            return element
        except:
            self.blackbox()
            return self.get_xpath(xpath)


    def get_xpath_name(self, name):
        """
        使用 xpath 文本精确匹配定位页面元素并返回 WebElement。

        Args:
            name: 页面元素的 text 精确值

        Returns:
            WebElement: 定位到的元素
        """
        # 使用xpath文本定位方法，准确定位页面name（text）文本内容元素
        findname = "//*[@text='%s']" % name
        try:
            # 显性等待20s，每1s进行检查是否存在，用在判断，来查找页面是否存在name（text）文本内容并检查元素对用户是否可见
            WebDriverWait(self.driver, 20, 1).until(EC.visibility_of_element_located((AppiumBy.XPATH,findname)))
            # element = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_xpath(findname))
            element = self.driver.find_element(AppiumBy.XPATH,findname)
            log.info('成功定位元素：' + '%s' % name)
            return element
        except:
            self.blackbox()
            return self.get_xpath_name(name)


    def get_xpath_contains(self, name):
        """
        使用 xpath 文本模糊匹配定位页面元素并返回 WebElement。

        Args:
            name: 需要包含的 text 片段

        Returns:
            WebElement: 定位到的元素
        """
        # 使用xpath文本定位方法，模糊定位页面name（text）文本内容元素
        findname = "//*[@contains(text(),'%s']" % (name)
        try:
            # 显性等待20s，每1s进行检查是否存在，用在判断，来查找页面是否存在name（text）文本内容并检查元素对用户是否可见
            WebDriverWait(self.driver, 20, 1).until(EC.visibility_of_element_located((AppiumBy.XPATH,findname)))
            # element = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_xpath(findname))
            element = self.driver.find_element(AppiumBy.XPATH,findname)
            log.info('成功定位元素：' + '%s' % name)
            return element
        except:
            self.blackbox()
            return self.get_xpath_contains(name)


    def get_className(self, classname):
        """
        定位页面 className 元素并返回 WebElement 列表。

        该方法使用显式等待确保元素可见；定位失败时会调用 `blackbox()` 处理弹窗干扰后递归重试。

        Args:
            classname: className 字符串

        Returns:
            list: WebElement 列表
        """
        try:
            WebDriverWait(self.driver, 20, 1).until(EC.visibility_of_element_located((AppiumBy.CLASS_NAME,classname)))
            element = self.driver.find_elements(AppiumBy.CLASS_NAME,classname)
            log.info('成功定位元素：' + '%s' % classname)
            return element
        except:
            self.blackbox()
            return self.get_className(classname)

    def get_android_uiautomator(self,uiautomator):
        """
        使用 Android `UIAutomator` 表达式进行组合定位并返回 WebElement。

        Args:
            uiautomator: UIAutomator 定位表达式

        Returns:
            WebElement: 定位到的元素

        注：
            该方法定位失败会触发 `blackbox()` 并递归重试。
        """
        try:
            WebDriverWait(self.driver,20,1).until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR,uiautomator)))
            # element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'index(2).resourceId("com.mymoney:id/add_trans_btn")')
            element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,uiautomator)
            log.info('成功定位元素：'+'%s' % uiautomator)
            return element
        except:
            self.blackbox()
            return self.get_android_uiautomator(uiautomator)

    def get_ios_uiautomator(self,uiautomator):
        """
        使用 iOS `UIAutomation` 表达式进行组合定位并返回 WebElement。

        Args:
            uiautomator: UIAutomation 定位表达式

        Returns:
            WebElement: 定位到的元素

        注：
            该方法定位失败会触发 `blackbox()` 并递归重试。
        """
        try:
            WebDriverWait(self.driver,20,1).until(EC.visibility_of_element_located((AppiumBy.IOS_UIAUTOMATION,uiautomator)))
            # element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'index(2).resourceId("com.mymoney:id/add_trans_btn")')
            element = self.driver.find_element(AppiumBy.IOS_UIAUTOMATION,uiautomator)
            log.info('成功定位元素：'+'%s' % uiautomator)
            return element
        except:
            self.blackbox()
            return self.get_ios_uiautomator(uiautomator)


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



