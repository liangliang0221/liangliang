# -*-coding: utf-8 -*-

from appium import webdriver
from ReadFile import ReadFile
from appium.options.common import AppiumOptions
import time

import os
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

class ElementInspector:
    """
    页面元素识别工具：帮助获取当前页面的元素信息
    """
    
    def __init__(self, config_path):
        """
        初始化元素识别器
        
        Args:
            config_path: Appium配置文件路径
        """
        data = ReadFile(config_path).data
        driver_caps = {
            'platformName': data['platformName'],
            'platformVersion': str(data['platformVersion']),
            'deviceName': data['deviceName'],
            'appPackage': data['appPackage'],
            'appActivity': data['appActivity'],
            'noReset': data['noReset'],
            'unicodeKeyboard': data['unicodeKeyboard'],
            'resetKeyboard': data['resetKeyboard'],
            'ensureWebviewsHavePages': data['ensureWebviewsHavePages'],
            'newCommandTimeout': data['newCommandTimeout']
        }
        options = AppiumOptions()
        options.load_capabilities(driver_caps)
        self.driver = webdriver.Remote('http://' + str(data['ip']) + ':' + str(data['port']) + '/wd/hub', options=options)
        print("Driver启动成功")
        
    def get_current_page_elements(self):
        """
        获取当前页面的所有可点击元素信息
        
        Returns:
            list: 元素信息列表，包含text、resource-id、class等
        """
        time.sleep(3)
        elements = []
        
        # 获取所有TextView元素（通常包含可点击的文本）
        text_elements = self.driver.find_elements('xpath', '//android.widget.TextView')
        for el in text_elements:
            try:
                text = el.get_attribute('text')
                resource_id = el.get_attribute('resource-id')
                if text and text.strip():
                    elements.append({
                        'type': 'TextView',
                        'text': text,
                        'resource_id': resource_id,
                        'find_type': 'name' if text else 'id',
                        'element_info': text if text else resource_id
                    })
            except:
                pass
        
        # 获取所有Button元素
        button_elements = self.driver.find_elements('xpath', '//android.widget.Button')
        for el in button_elements:
            try:
                text = el.get_attribute('text')
                resource_id = el.get_attribute('resource-id')
                elements.append({
                    'type': 'Button',
                    'text': text,
                    'resource_id': resource_id,
                    'find_type': 'name' if text else 'id',
                    'element_info': text if text else resource_id
                })
            except:
                pass
        
        # 获取所有EditText元素
        edit_elements = self.driver.find_elements('xpath', '//android.widget.EditText')
        for el in edit_elements:
            try:
                hint = el.get_attribute('hint')
                resource_id = el.get_attribute('resource-id')
                elements.append({
                    'type': 'EditText',
                    'hint': hint,
                    'resource_id': resource_id,
                    'find_type': 'id',
                    'element_info': resource_id
                })
            except:
                pass
        
        return elements
    
    def generate_yaml_content(self, elements):
        """
        根据元素信息生成YAML格式内容
        
        Args:
            elements: 元素信息列表
            
        Returns:
            str: YAML格式的测试用例
        """
        yaml_lines = []
        yaml_lines.append('testinfo:')
        yaml_lines.append('    - id: wowo_inspect_test')
        yaml_lines.append('      title: 自动生成的测试用例')
        yaml_lines.append('      execute: 1')
        yaml_lines.append('testcase:')
        yaml_lines.append('    # ========== 页面元素识别结果 ==========')
        
        for idx, el in enumerate(elements):
            yaml_lines.append('    -')
            yaml_lines.append(f'      element_info: {el["element_info"]}')
            yaml_lines.append(f'      find_type: {el["find_type"]}')
            yaml_lines.append(f'      operate_type: click')
            yaml_lines.append(f'      path: 点击{el["text"] if "text" in el else el["element_info"]}')
        
        return '\n'.join(yaml_lines)
    
    def close(self):
        """关闭driver"""
        self.driver.quit()

if __name__ == '__main__':
    inspector = ElementInspector('../config/activity.yaml')
    elements = inspector.get_current_page_elements()
    
    print("\n=== 当前页面元素列表 ===")
    for i, el in enumerate(elements):
        print(f"{i+1}. [{el['type']}] text='{el.get('text', '')}' id='{el.get('resource_id', '')}'")
    
    yaml_content = inspector.generate_yaml_content(elements)
    print("\n=== 生成的YAML内容 ===")
    print(yaml_content)
    
    # 写入文件
    with open('../data/inspected_elements.yaml', 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    print("\n已保存到 data/inspected_elements.yaml")
    
    inspector.close()