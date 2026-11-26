"""
项目入口脚本：用于在本地生成 allure 报告等任务。

当前文件是模板式 main，实际测试运行由 `pytest` 收集并执行。
"""

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import pytest


def print_hi(name):
    """
    模板函数：打印问候信息。

    Args:
        name: 需要打印的名称
    """
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pytest.main(['--count=2', '--repeat-scope=session'])
    os.system('allure generate ./ouput/temp -o ./ouput/report --clean')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

