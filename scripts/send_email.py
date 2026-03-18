#!/usr/bin/env python3
"""
邮件发送脚本
使用 SMTP 发送每日推送邮件
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Optional, List

# SMTP 配置
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.qq.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")

# 发送配置
SENDER = os.environ.get("SMTP_USER", "")
RECIPIENTS = os.environ.get("EMAIL_RECIPIENTS", "947433837@qq.com").split(",")


def create_email_html(weather_html: str, news_html: str, it_news_html: str = "") -> str:
    """
    创建完整的 HTML 邮件内容
    """
    today = datetime.now().strftime("%Y年%m月%d日")
    weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][datetime.now().weekday()]

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'PingFang SC', 'Microsoft YaHei', sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px 10px;
        }}
        .wrapper {{
            max-width: 700px;
            margin: 0 auto;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 25px;
            text-align: center;
            border-radius: 16px 16px 0 0;
        }}
        .header h1 {{
            font-size: 28px;
            font-weight: 600;
            margin-bottom: 8px;
            letter-spacing: 1px;
        }}
        .header .date {{
            font-size: 16px;
            opacity: 0.9;
        }}
        .content {{
            background: #ffffff;
            padding: 25px;
            border-radius: 0 0 16px 16px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
        }}
        .section {{
            margin-bottom: 30px;
        }}
        .section:last-child {{
            margin-bottom: 0;
        }}
        .section-title {{
            display: flex;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #f0f0f0;
        }}
        .section-title .icon {{
            font-size: 24px;
            margin-right: 10px;
        }}
        .section-title h2 {{
            font-size: 20px;
            font-weight: 600;
            color: #2c3e50;
        }}
        .weather-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }}
        .weather-card {{
            background: linear-gradient(145deg, #f8f9fa, #ffffff);
            border: 1px solid #e8e8e8;
            border-radius: 12px;
            padding: 15px;
            transition: transform 0.2s;
        }}
        .weather-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }}
        .weather-card .location {{
            font-size: 14px;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 8px;
        }}
        .weather-card .temp {{
            font-size: 28px;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 5px;
        }}
        .weather-card .details {{
            font-size: 12px;
            color: #666;
            line-height: 1.5;
        }}
        .weather-card .condition {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 12px;
            margin-bottom: 8px;
        }}
        .news-list {{
            list-style: none;
            padding: 0;
        }}
        .news-list li {{
            padding: 12px 0;
            border-bottom: 1px solid #f0f0f0;
        }}
        .news-list li:last-child {{
            border-bottom: none;
        }}
        .news-list li a {{
            color: #333;
            text-decoration: none;
            font-size: 15px;
            line-height: 1.5;
            display: block;
        }}
        .news-list li a:hover {{
            color: #667eea;
        }}
        .news-list .num {{
            display: inline-block;
            width: 24px;
            height: 24px;
            line-height: 24px;
            text-align: center;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-radius: 50%;
            font-size: 12px;
            font-weight: 600;
            margin-right: 10px;
        }}
        .news-list .meta {{
            font-size: 12px;
            color: #999;
            margin-top: 5px;
            margin-left: 34px;
        }}
        .divider {{
            height: 1px;
            background: linear-gradient(to right, transparent, #e0e0e0, transparent);
            margin: 25px 0;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #999;
            font-size: 13px;
        }}
        .footer a {{
            color: #667eea;
            text-decoration: none;
        }}
        @media only screen and (max-width: 500px) {{
            .weather-grid {{
                grid-template-columns: 1fr;
            }}
            .header h1 {{
                font-size: 24px;
            }}
        }}
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="header">
            <h1>Daily Push</h1>
            <div class="date">{today} {weekday}</div>
        </div>
        <div class="content">
            {weather_html}

            <div class="divider"></div>

            {news_html}

            {it_news_html}

            <div class="divider"></div>

            <div class="footer">
                <p>由 Claude Code 自动生成</p>
                <p style="margin-top: 5px;">如有问题请联系 <a href="mailto:{SENDER}">{SENDER}</a></p>
            </div>
        </div>
    </div>
</body>
</html>
"""
    return html


def send_email(
    subject: str,
    html_content: str,
    text_content: Optional[str] = None,
    recipients: Optional[List[str]] = None,
) -> bool:
    """
    发送 HTML 邮件

    Args:
        subject: 邮件主题
        html_content: HTML 内容
        text_content: 纯文本内容（可选，作为备用）
        recipients: 收件人列表（可选，默认使用配置）

    Returns:
        发送成功返回 True，失败返回 False
    """
    if not SMTP_USER or not SMTP_PASS:
        print("错误: 未配置 SMTP 用户名或密码")
        return False

    recipients = recipients or RECIPIENTS

    # 创建邮件
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER
    msg["To"] = ", ".join(recipients)

    # 添加纯文本部分（备用）
    if text_content:
        msg.attach(MIMEText(text_content, "plain", "utf-8"))

    # 添加 HTML 部分
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    try:
        # 连接 SMTP 服务器
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SENDER, recipients, msg.as_string())

        print(f"邮件发送成功: {', '.join(recipients)}")
        return True

    except smtplib.SMTPException as e:
        print(f"SMTP 错误: {e}")
        return False
    except Exception as e:
        print(f"发送失败: {e}")
        return False


def send_daily_push(weather_html: str, news_html: str, it_news_html: str = "", recipients: Optional[List[str]] = None) -> bool:
    """
    发送每日推送邮件

    Args:
        weather_html: 天气 HTML 内容
        news_html: 新闻 HTML 内容
        it_news_html: IT 资讯 HTML 内容（可选）
        recipients: 收件人列表（可选）

    Returns:
        发送成功返回 True
    """
    today = datetime.now().strftime("%Y年%m月%d日")
    subject = f"Daily Push - {today}"

    html_content = create_email_html(weather_html, news_html, it_news_html)

    return send_email(subject, html_content, recipients=recipients)


if __name__ == "__main__":
    # 测试发送
    test_html = """
    <div class="section">
        <div class="section-title">
            <span class="icon">Test</span>
            <h2>测试邮件</h2>
        </div>
        <p>这是一封测试邮件，用于验证 SMTP 配置是否正确。</p>
        <p style="margin-top: 15px; color: #666;">发送时间: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
    </div>
    """

    success = send_email(
        subject="测试邮件 - Daily Push",
        html_content=test_html,
        text_content="这是一封测试邮件，用于验证 SMTP 配置是否正确。",
    )

    if success:
        print("[OK] 测试邮件发送成功！")
    else:
        print("[FAIL] 测试邮件发送失败！")
