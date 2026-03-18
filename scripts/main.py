#!/usr/bin/env python3
"""
每日消息推送主脚本
整合天气和新闻数据，发送邮件
"""

import sys
import os
from datetime import datetime

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from weather import get_all_weather_html, get_weather_text
from news import get_news_html, get_news_text, get_it_news_html, get_it_news_text
from send_email import send_daily_push


def main():
    """
    主函数：获取数据并发送邮件
    """
    print(f"开始执行每日推送 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 获取天气数据
    print("正在获取天气数据...")
    weather_html = get_all_weather_html()
    print("天气数据获取完成")

    # 获取新闻数据
    print("正在获取新闻数据...")
    news_html = get_news_html()
    print("新闻数据获取完成")

    # 获取 IT 资讯
    print("正在获取 IT 资讯...")
    it_news_html = get_it_news_html()
    print("IT 资讯获取完成")

    # 发送邮件
    print("正在发送邮件...")
    success = send_daily_push(weather_html, news_html, it_news_html)

    if success:
        print("[OK] 每日推送发送成功！")
        return 0
    else:
        print("[FAIL] 每日推送发送失败！")
        return 1


def test_mode():
    """
    测试模式：只打印数据，不发送邮件
    """
    print("=" * 60)
    print(f"测试模式 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    print("\n" + get_weather_text())
    print("\n" + get_news_text())
    print("\n" + get_it_news_text())

    print("\n" + "=" * 60)
    print("测试完成（未发送邮件）")
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_mode()
    else:
        sys.exit(main())
