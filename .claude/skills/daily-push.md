# 每日消息推送 Skill

手动触发每日消息推送。

## 触发方式

用户可以通过 `/daily-push` 来调用这个 skill。

## 参数

- `--test`: 测试模式，只打印数据不发送邮件

## 描述

执行每日消息推送任务：
1. 获取广州和茂名各区域天气
2. 获取昨日热点新闻 Top 10
3. 发送到指定邮箱

## 执行指令

当用户调用此 skill 时，执行以下命令：

### 正常模式（发送邮件）

```bash
cd D:/agents/scripts && python main.py
```

需要设置的环境变量：
- SMTP_HOST=smtp.qq.com
- SMTP_PORT=587
- SMTP_USER=714497100@qq.com
- SMTP_PASS=jlwpkzqfeqiqbdai
- EMAIL_RECIPIENTS=947433837@qq.com
- QWEATHER_API_KEY=(从 settings.local.json 获取)
- TIANAPI_KEY=(从 settings.local.json 获取)

### 测试模式（不发送邮件）

```bash
cd D:/agents/scripts && python main.py --test
```

## 执行步骤

1. 读取 settings.local.json 获取环境变量
2. 运行 Python 脚本获取数据
3. 组装并发送邮件（非测试模式）
4. 报告执行结果

## 示例用法

```bash
# 正常执行（发送邮件）
/daily-push

# 测试模式（不发送邮件）
/daily-push --test
```

## 前置条件

确保以下环境变量已在 settings.local.json 中配置：
- `QWEATHER_API_KEY`: 和风天气 API Key
- `TIANAPI_KEY`: 天行数据 API Key
- SMTP 相关配置
