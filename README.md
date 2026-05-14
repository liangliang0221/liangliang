# Trae 自动化测试项目

基于 Python + Appium 的移动端自动化测试框架，用于测试星野APP（wowo）的各项功能。

## 🌟 项目特性

- ✅ 支持 Android 移动端自动化测试
- ✅ 基于 Appium 实现元素定位和操作
- ✅ 使用 Allure 生成专业测试报告
- ✅ 支持 YAML 数据驱动测试
- ✅ 集成 pytest 测试框架

## 📁 项目结构

```
Trae/
├── common/          # 公共工具类
│   ├── BaseOperate.py    # 基础操作封装
│   ├── GetDriver.py      # Appium Driver 获取
│   ├── GetYaml.py        # YAML 配置读取
│   ├── Operate.py        # 操作执行器
│   └── logs.py           # 日志工具
├── config/          # 配置文件
│   └── activity.yaml     # Appium 配置
├── conftest/        # 测试模块
│   ├── homepage.py       # 首页测试模块
│   ├── message.py        # 消息页测试模块
│   ├── mine.py           # 我的页测试模块
│   └── test_module.py    # 综合测试模块
├── data/            # 测试数据
│   ├── HomePage/         # 首页测试数据
│   ├── Message/          # 消息页测试数据
│   └── Mine/             # 我的页测试数据
├── testcase/        # 测试用例
│   ├── home/             # 首页测试用例
│   ├── message/          # 消息页测试用例
│   ├── mine/             # 我的页测试用例
│   └── test_wowo.py      # 综合测试用例
├── output/          # 输出目录
│   └── report/           # 测试报告
├── requirements.txt      # 依赖列表
└── pytest.ini            # pytest 配置
```

## 🛠️ 环境要求

- Python 3.8+
- Appium Server 2.0+
- Android SDK
- JDK 1.8+

## 📦 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/liangliang0221/liangliang.git
cd Trae

# 2. 创建虚拟环境（可选但推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -r requirements.txt
```

## 🚀 运行测试

### 运行单个测试文件

```bash
# 运行首页测试
python -m pytest testcase/home/test_home.py -vs

# 运行消息页测试
python -m pytest testcase/message/test_message.py -vs

# 运行我的页测试
python -m pytest testcase/mine/test_mine.py -vs

# 运行综合测试
python -m pytest testcase/test_wowo.py -vs
```

### 运行所有测试

```bash
python -m pytest testcase/ -vs
```

### 生成 Allure 报告

```bash
# 运行测试并生成报告数据
python -m pytest testcase/ -vs --alluredir=output/report

# 生成 HTML 报告
allure generate output/report -o output/report/html --clean

# 启动报告服务器
allure serve output/report -p 8080
```

## 📊 测试报告

测试完成后，Allure 报告将包含：
- ✅ 测试用例执行结果
- ✅ 测试步骤详情
- ✅ 失败截图
- ✅ 执行时间统计
- ✅ 测试覆盖率

## 🧪 测试模块

| 模块 | 说明 | 文件 |
|------|------|------|
| 首页测试 | 首页推荐页和树洞功能测试 | `testcase/home/test_home.py` |
| 消息测试 | 消息页面UI元素定位测试 | `testcase/message/test_message.py` |
| 我的页测试 | 个人中心页面测试 | `testcase/mine/test_mine.py` |
| 综合测试 | 登录-首页-消息端到端测试 | `testcase/test_wowo.py` |

## 📝 测试数据格式

测试数据采用 YAML 格式，示例：

```yaml
testinfo:
  - id: test_case_id
    title: 测试用例标题
    execute: 1
testcase:
  - element_info: com.xinxin.wowo:id/btn_login
    find_type: id
    operate_type: click
    path: 点击登录按钮
```

## 🔧 配置说明

`config/activity.yaml` 配置项：
- `platformName`: 平台名称（Android/iOS）
- `deviceName`: 设备名称
- `appPackage`: 应用包名
- `appActivity`: 启动 Activity
- `automationName`: 自动化引擎（UiAutomator2）
- `noReset`: 是否重置应用状态

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**作者**: AutoTest / liangliang  
**版本**: v1.0  
**日期**: 2026年5月
