# -*-coding: utf-8 -*-

import sys
sys.path.insert(0, 'common')

from ElementInspector import ElementInspector

if __name__ == '__main__':
    # 初始化元素识别器
    inspector = ElementInspector('../config/activity.yaml')
    
    # 获取当前页面元素
    print("\n=== 正在获取页面元素... ===")
    elements = inspector.get_current_page_elements()
    
    # 打印元素列表
    print("\n=== 当前页面元素列表 ===")
    for i, el in enumerate(elements):
        print(f"{i+1}. [{el['type']}] text='{el.get('text', 'N/A')}' id='{el.get('resource_id', 'N/A')}'")
    
    # 生成YAML内容
    yaml_content = inspector.generate_yaml_content(elements)
    
    # 打印YAML内容
    print("\n=== 生成的YAML测试用例 ===")
    print(yaml_content)
    
    # 保存到test.yaml
    with open('data/test.yaml', 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    print("\n已更新 data/test.yaml")
    
    # 关闭driver
    inspector.close()
    
    # 运行测试
    print("\n=== 开始执行测试 ===")
    import subprocess
    subprocess.run(['pytest', 'testcase/test_wowo.py', '-v', '--tb=short'])