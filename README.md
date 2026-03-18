# Daily Push - 每日消息推送 Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个基于 Claude Code 的自动化每日消息推送系统，可获取天气、新闻、IT资讯并发送到指定邮箱。

## 功能特性

- **天气推送**: 获取指定城市各区域实时天气（和风天气 API）
- **新闻推送**: 获取每日热点新闻（天行数据每日简报）
- **IT 资讯**: 获取科技行业最新动态
- **邮件发送**: 精美的 HTML 邮件格式
- **定时任务**: 支持每天定时自动推送

## 效果预览

邮件包含：
- 广州/茂名各区域天气卡片
- 今日热点新闻 Top 10
- IT 资讯 Top 10

## 快速开始

### 前置要求

- Python 3.8+
- Claude Code CLI
- 和风天气 API Key
- 天行数据 API Key
- SMTP 邮箱服务

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/wkr712/daily-push.git
   cd daily-push
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置环境变量**

   复制配置模板：
   ```bash
   cp .claude/settings.local.json.example .claude/settings.local.json
   ```

   编辑 `.claude/settings.local.json`：
   ```json
   {
     "env": {
       "SMTP_HOST": "smtp.qq.com",
       "SMTP_PORT": "587",
       "SMTP_USER": "your_email@qq.com",
       "SMTP_PASS": "your_auth_code",
       "EMAIL_RECIPIENTS": "recipient@example.com",
       "QWEATHER_API_KEY": "your_qweather_key",
       "QWEATHER_API_HOST": "xxxxxx.re.qweatherapi.com",
       "TIANAPI_KEY": "your_tianapi_key"
     }
   }
   ```

4. **修改 Skill 路径**

   编辑 `.claude/skills/daily-push.md`，将脚本路径改为你的实际路径。

5. **测试运行**
   ```
   /daily-push --test
   ```

## 获取 API Key

### 和风天气

1. 访问 https://dev.qweather.com/
2. 注册并创建项目
3. 选择「Web API」→「免费订阅」
4. 复制 API Key 和自定义 API Host

### 天行数据

1. 访问 https://www.tianapi.com/
2. 注册并登录
3. 申请以下接口：
   - `bulletin` - 每日简报
   - `it` - IT 资讯
4. 复制 API Key

### SMTP 配置

**QQ邮箱**（推荐）：
1. QQ邮箱 → 设置 → 账户
2. 开启 POP3/SMTP 服务
3. 生成授权码

| 参数 | 值 |
|------|-----|
| SMTP_HOST | smtp.qq.com |
| SMTP_PORT | 587 |
| SMTP_USER | 你的QQ邮箱 |
| SMTP_PASS | 授权码 |

## 定时任务

### Claude Code 内置
```
/cron 0 8 * * * /daily-push
```

### Windows 任务计划程序
1. 打开「任务计划程序」
2. 创建基本任务 → 每天 8:00
3. 启动程序：`python D:\daily-push\scripts\main.py`

### Linux Crontab
```bash
0 8 * * * cd /path/to/daily-push/scripts && python main.py
```

## 自定义配置

### 修改天气城市

编辑 `scripts/weather.py`：

```python
# 添加你的城市
YOUR_CITY_LOCATIONS = {
    "城市名": "Location ID",
}
```

Location ID 查询：https://github.com/qwd/LocationList

### 修改邮件样式

编辑 `scripts/send_email.py` 中的 `create_email_html` 函数。

## 项目结构

```
daily-push/
├── .claude/
│   ├── agents/
│   │   └── daily-push.md      # Agent 定义
│   ├── skills/
│   │   └── daily-push.md      # Skill 定义
│   ├── settings.local.json    # 配置文件 (不上传)
│   └── settings.local.json.example  # 配置模板
├── scripts/
│   ├── main.py                # 主脚本
│   ├── weather.py             # 天气模块
│   ├── news.py                # 新闻模块
│   └── send_email.py          # 邮件模块
├── requirements.txt           # Python 依赖
└── README.md
```

## 环境变量说明

| 变量名 | 必需 | 说明 |
|--------|------|------|
| SMTP_HOST | ✅ | SMTP 服务器地址 |
| SMTP_PORT | ✅ | SMTP 端口 |
| SMTP_USER | ✅ | 发件邮箱 |
| SMTP_PASS | ✅ | SMTP 授权码 |
| EMAIL_RECIPIENTS | ✅ | 收件人（逗号分隔） |
| QWEATHER_API_KEY | ✅ | 和风天气 API Key |
| QWEATHER_API_HOST | ✅ | 和风天气自定义 Host |
| TIANAPI_KEY | ✅ | 天行数据 API Key |

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 天气 API 返回 403 | 检查 API Host 是否正确配置 |
| 邮件发送失败 | 检查 SMTP 配置和授权码 |
| 新闻数据为空 | 检查天行数据接口权限 |
| 中文乱码 | 确保设置 `PYTHONIOENCODING=utf-8` |

## 许可证

[MIT License](LICENSE)

## 贡献

欢迎提交 Issue 和 Pull Request！

## 致谢

- [和风天气](https://www.qweather.com/) - 天气数据
- [天行数据](https://www.tianapi.com/) - 新闻数据
- [Claude Code](https://claude.ai/) - AI 助手
