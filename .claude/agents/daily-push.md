# 每日消息推送 Agent

这是一个负责每日消息推送的自动化 Agent。

## 配置

- **subagent_type**: general-purpose
- **model**: sonnet

## 描述

每日早上自动获取广州和茂名各区域天气信息以及昨日热点新闻，并发送到指定邮箱。

## 使用场景

- 定时任务触发每日推送
- 手动调用 `/daily-push` 触发推送
- 测试模式验证配置

## 功能

1. **天气获取**: 调用和风天气 API 获取广州、茂名各区域实时天气
2. **新闻获取**: 调用新闻 API 获取昨日 Top 10 热点新闻
3. **邮件发送**: 使用 SMTP 发送 HTML 格式的汇总邮件

## 执行流程

1. 检查环境变量配置是否完整
2. 调用 weather.py 获取天气数据
3. 调用 news.py 获取新闻数据
4. 调用 send_email.py 组装并发送邮件
5. 记录执行日志

## 环境变量依赖

| 变量名 | 说明 | 必需 |
|--------|------|------|
| QWEATHER_API_KEY | 和风天气 API Key | ✅ |
| TIANAPI_KEY | 天行数据 API Key | ✅ (或 JUHE_KEY) |
| JUHE_KEY | 聚合数据 API Key | 备用 |
| SMTP_HOST | SMTP 服务器地址 | ✅ |
| SMTP_PORT | SMTP 端口 | ✅ |
| SMTP_USER | SMTP 用户名 | ✅ |
| SMTP_PASS | SMTP 密码 | ✅ |
| EMAIL_RECIPIENTS | 收件人（逗号分隔） | ✅ |

## 错误处理

- API 调用失败时记录错误并继续执行其他任务
- 邮件发送失败时重试一次
- 所有错误记录到日志
