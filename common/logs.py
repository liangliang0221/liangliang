# @Time    : 2023/9/18 15:19
# @Author  : zhenhai
# @File    : logs.py
# @Software: PyCharm
#!/user/bin/env python3
# -*- coding : utf-8 -*-
# 用途 : 打印log到日志文件logs中,位置在testlog中显示

import logging
import os
import time

# 使用相对路径+绝对路径
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
log_path = PATH("../log")


class log:
    """
    日志封装类：将日志同时输出到控制台和落盘文件中（位于 `log/` 目录）。

    使用方式：
        - `log().info("message")`
        - `log().error("message")`
    """

    def __init__(self):
        """
        初始化 logger，并根据当前日期生成日志文件名。
        """

        filename = 'Appium-' + ''.join(time.strftime('%Y%m%d')) + ''.join('.txt')  # 设置log名
        self.logname = os.path.join(log_path, filename)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        # 设置日志输出格式
        self.formatter = logging.Formatter('[%(asctime)s] - [%(levelname)s] - %(message)s')

    def output(self, level, message):
        """
        输出一条日志。

        Args:
            level: 日志等级，支持 `info`、`debug`、`warn`、`error`
            message: 要写入的日志内容
        """

        fh = logging.FileHandler(self.logname, 'a')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warn':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)

        self.logger.removeHandler(fh)
        self.logger.removeHandler(ch)

        fh.close()

    #自定义日志状态
    def info(self, message: object) -> object:
        """输出 info 级别日志。"""
        self.output('info', message)

    def debug(self, message):
        """输出 debug 级别日志。"""
        self.output('debug', message)

    def warn(self, message):
        """输出 warn 级别日志。"""
        self.output('warn', message)

    def error(self, message):
        """输出 error 级别日志。"""
        self.output('error', message)
