# -*-coding: utf-8 -*-
# @Time    : 2023/12/18 16:07
# @Author  : zhenhai
# @File    : conftest.py
# @Software: PyCharm

"""
`testcase.conftest`：测试用例根目录 fixtures / collection 配置入口。

当前文件仅保留了注释掉的 `pytest_collection_modifyitems` 逻辑，避免影响执行顺序。
"""


# def pytest_collection_modifyitems(session, items):
#     # 期望用例顺序按照.py文件执行,有问题，影响到整体会话测试
#     appoint_classes = {'TestLogin': [], 'TestHome': [], 'TestParty': [], 'TestProperty': []}
#     for item in items:
#         for cls_name in appoint_classes:
#             if item.parent.name == cls_name:
#                 appoint_classes[cls_name].append(item)
#     items.clear()
#     for cases in appoint_classes.values():
#         items.extend(cases)
