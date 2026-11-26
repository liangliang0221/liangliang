import uiautomator2 as u2

d = u2.connect() # 连接设备
xml_layout = d.dump_hierarchy() # 获取当前页面所有元素的XML数据
print(xml_layout)