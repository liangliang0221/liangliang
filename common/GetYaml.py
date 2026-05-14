# -*-coding: utf-8 -*-
# @Time    : 2026/05/13
# @Author  : liangliang
# @File    : GetYaml.py
# @Software: PyCharm

import yaml
import codecs

class getyaml:

    def __init__(self,path):
        """
        初始化数据驱动读取器。

        Args:
            path: yaml 文件路径
        """
        self.path = path

    def getYaml(self):
        '''
        读取yaml文件
        :param path: 文件路径
        :return:
        '''
        try:
            f = codecs.open(self.path, 'r', encoding='utf-8')
            data = yaml.load(f, Loader=yaml.FullLoader)
            f.close()
            return data
        except Exception:
            print("未找到yaml文件")

    def alldata(self):
        """
        读取 yaml 并返回解析后的完整数据结构。

        Returns:
            dict: yaml 解析后的数据
        """
        data =self.getYaml()
        return data

    def caselen(self):
        """
        获取 yaml 中 `testcase` 列表的长度。

        Returns:
            int: testcase 条数
        """
        data = self.alldata()
        length = len(data['testcase'])
        return length

    def get_elementinfo(self,i):
        """
        获取第 i 条 testcase 的 `element_info` 字段。

        Args:
            i: testcase 下标

        Returns:
            any: element_info 对应的数据结构
        """
        data = self.alldata()
        return data['testcase'][i]['element_info']

    def get_end_elementinfo(self,i):
        """
        获取第 i 条 testcase 的 `end_element_info` 字段（用于元素滑动终点）。
        """

        data = self.alldata()
        return data['testcase'][i]['end_element_info']

    def get_findtype(self,i):
        """
        获取第 i 条 testcase 的 `find_type`（定位策略）。
        """
        data = self.alldata()
        return data['testcase'][i]['find_type']

    def get_end_findtype(self,i):
        """
        获取第 i 条 testcase 的 `end_find_type`（元素滑动终点定位策略）。
        """

        data = self.alldata()
        return data['testcase'][i]['end_find_type']

    def get_operate_type(self,i):
        """
        获取第 i 条 testcase 的 `operate_type`（动作类型，如 click/send_keys/swipe 等）。
        """
        data = self.alldata()
        return data['testcase'][i]['operate_type']

    def get_index(self,i):
        """
        当 `find_type` 为 `ids` 或 `class_name` 时，获取对应的 `index`（第几个元素）。
        """

        data = self.alldata()
        testcase = data['testcase'][i]
        # 兼容：当 yaml 里存在 index 字段时直接返回；避免仅依赖 find_type 导致 end_find_type 取不到 index
        return testcase.get('index')

    def get_send_content(self,i):
        """
        当 `operate_type` 为 `send_keys` 时，获取 `send_content`（要输入的文本）。
        """
        data = self.alldata()
        if self.get_operate_type(i) == 'send_keys':
            return data['testcase'][i]['send_content']
        else:
            pass

    def get_backtimes(self,i):
        """
        获取第 i 条 testcase 的 `times`（回退/滑动次数/睡眠次数等）。
        """
        data = self.alldata()
        # 若yaml里面的operate_type类型为send_keys，则该组新增一项times并返回其数据，用于返回、上下左右操作次数,以及睡眠次數（每次5S）
        if self.get_operate_type(i)=='back' or self.get_operate_type(i)=='swipe_up' \
                or self.get_operate_type(i)=='swipe_down' or self.get_operate_type(i)=='swipe_right' \
                or self.get_operate_type(i)=='swipe_left' or self.get_operate_type(i)=='sleep' \
                or self.get_operate_type(i)=='swipe_pt' or self.get_operate_type(i)=='swipe_px'\
                or self.get_operate_type(i)=='keycode':
                    return data['testcase'][i]['times']
        else:
            pass

    def get_title(self):
        """
        获取 yaml 顶层 `testinfo[0].title` 标题信息。
        """

        data = self.alldata()
        return data['testinfo'][0]['title']

    def get_path(self, i):
        """
        获取第 i 条 testcase 的 `path` 字段（用于渲染/定位用例步骤的定位配置）。
        """

        data = self.alldata()
        return data['testcase'][i]['path']

# 用于测试路径以及访问是否正常返回
# path ="../data/property/my_property.yaml"
# path ="../data/home/home_works.yaml"
# print(getyaml(path).alldata())
# print(Getyaml(path).get_title())
# for i in range(Getyaml(path).caselen()):
#   print(Getyaml(path).get_operate_type(i))
#   print(Getyaml(path).get_elementinfo(i))
#   print(Getyaml(path).get_findtype(i))
#   print(Getyaml(path).get_send_content(i))
#   print(Getyaml(path).get_backtimes(i))
#   index =Getyaml(path).get_index(i)
#   print(index)