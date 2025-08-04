# 🎮 Cheat Status Dashboard(README By AI)

一个用于监控多个游戏外挂论坛最新更新状态的工具，帮助用户快速了解各大外挂在CS2更新后的可用性。

## 📋 项目概述

本项目提供两个版本：
- **🐍 Python版本** - 命令行工具，适合开发者和高级用户
- **🌐 Web版本** - 基于PHP的Web界面，提供可视化的状态监控

## 🎯 支持的平台

- **Nixware** - https://nixware.cc/
- **Neverlose** - https://neverlose.cc/
- **Fatality** - https://fatality.win/
- **Memesense** - https://memesense.gg/
- **Plaguecheat** - https://plaguecheat.cc/
- **CS2 Steam** - Steam官方CS2更新

## ✨ 功能特性

### 核心功能
- 🔍 **实时监控** - 自动获取各平台最新更新信息
- 📊 **状态分析** - 智能判断外挂在CS2更新后的可用性
- 🎨 **可视化界面** - 直观的状态显示和颜色编码
- 🔄 **自动刷新** - 定期更新数据，保持信息最新
- 📱 **响应式设计** - 支持桌面和移动设备

### 状态判断逻辑
- ✅ **可用** - 外挂更新日期 >= CS2更新日期
- ❌ **不可用** - 外挂更新日期 < CS2更新日期
- ❓ **未知** - 无法获取更新信息,可能是API出错或token配置错误

## 🚀 快速开始

### Python版本

#### 安装依赖
```bash
pip install -r requirements.txt
```

#### 配置文件
复制并编辑配置文件：
```python
# config.py
FATALITY_COOKIES = "你的Fatality登录cookies"
```

#### 使用方法
```bash
# 获取所有平台状态
python cheatstatus.py

# 获取特定平台信息
python cheatstatus.py --nixware
python cheatstatus.py --fatality
python cheatstatus.py --neverlose
python cheatstatus.py --memesense
python cheatstatus.py --cs2
```

### Web版本

#### 环境要求
- PHP 7.4+
- cURL扩展
- Web服务器（Apache/Nginx）

#### 安装步骤
1. 将项目文件上传到Web服务器
2. 配置 `api/config.php`：
```php
<?php
// Steam API配置
define('STEAM_ACCESS_TOKEN', '你的Steam API Token');

// Fatality Cookies配置
define('FATALITY_COOKIES', '你的Fatality cookies');

// 请求超时设置
define('REQUEST_TIMEOUT', 60);

// User-Agent
define('USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');
?>
```
3. 访问 `index.html` 开始使用

## 🔧 配置说明

### Fatality Cookies获取
1. 使用浏览器登录 https://fatality.win/
2. 按F12打开开发者工具
3. 在Network标签中刷新页面
4. 找到请求头中的Cookie值
5. 复制完整的Cookie字符串到配置文件

### Steam API Token获取
1. 访问 https://steamcommunity.com/dev/apikey
2. 注册并获取API密钥
3. 将密钥添加到配置文件

### 如果您将此项目搭建到您的服务器上，请放心，您的cookies和API密钥不会被泄露。(Web版本)

## 📊 API接口

Web版本提供RESTful API接口：

```bash
# 获取状态总结
GET /api/index.php?action=summary

# 获取所有新闻
GET /api/index.php?action=all

# 获取特定平台新闻
GET /api/index.php?action=nixware
GET /api/index.php?action=neverlose
GET /api/index.php?action=fatality
GET /api/index.php?action=memesense
GET /api/index.php?action=cs2
```

## 🎨 界面预览

Web版本提供：
- 📈 **状态总结页** - 一目了然的外挂可用性概览
- 📰 **详细新闻页** - 各平台最新更新详情
- 🔍 **单平台视图** - 专注查看特定平台信息

## 🛠️ 技术栈

### Python版本
- Python 3.7+
- requests
- beautifulsoup4
- lxml
- python-dateutil

### Web版本
- PHP 7.4+
- HTML5/CSS3
- JavaScript (ES6+)
- cURL

## 📝 更新日志

### v2.0.0
- ✨ 新增Web版本
- 🎨 全新的可视化界面
- 📊 智能状态分析
- 🔄 实时数据更新
- 📱 响应式设计

### v1.0.0
- 🎯 支持多平台监控
- 🐍 Python命令行版本
- 📰 新闻获取功能

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## ⚠️ 免责声明

本工具仅用于学习和研究目的，请遵守相关网站的使用条款。使用本工具所产生的任何后果由使用者自行承担。

## 📞 联系方式

如有问题或建议，请通过GitHub Issues联系。

---

⭐ 如果这个项目对你有帮助，请给个Star支持一下！