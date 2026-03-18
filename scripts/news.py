#!/usr/bin/env python3
"""
新闻获取脚本 - 调用新闻 API
获取昨日热点新闻 Top 10
"""

import os
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# 天行数据 API 配置
TIANAPI_KEY = os.environ.get("TIANAPI_KEY", "")
TIANAPI_NEWS_URL = "https://apis.tianapi.com/bulletin/index"
TIANAPI_IT_URL = "https://apis.tianapi.com/it/index"

# 备用：聚合数据 API
JUHE_KEY = os.environ.get("JUHE_KEY", "")
JUHE_NEWS_URL = "http://v.juhe.cn/toutiao/index"


def get_news_tianapi(num: int = 10) -> Optional[List[Dict]]:
    """
    使用天行数据 API 获取新闻

    Args:
        num: 获取新闻数量

    Returns:
        新闻列表，失败返回 None
    """
    if not TIANAPI_KEY:
        print("错误: 未配置 TIANAPI_KEY 环境变量")
        return None

    params = {
        "key": TIANAPI_KEY,
    }

    try:
        response = requests.get(TIANAPI_NEWS_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        if data.get("code") == 200:
            # bulletin 接口返回 result.list
            newslist = data.get("result", {}).get("list", [])
            return newslist[:num] if newslist else None
        else:
            print(f"天行 API 错误: {data.get('code')} - {data.get('msg', '未知错误')}")
            return None
    except requests.RequestException as e:
        print(f"天行 API 请求失败: {e}")
        return None


def get_it_news_tianapi(num: int = 10) -> Optional[List[Dict]]:
    """
    使用天行数据 API 获取 IT 资讯

    Args:
        num: 获取新闻数量

    Returns:
        新闻列表，失败返回 None
    """
    if not TIANAPI_KEY:
        print("错误: 未配置 TIANAPI_KEY 环境变量")
        return None

    params = {
        "key": TIANAPI_KEY,
        "num": num,
    }

    try:
        response = requests.get(TIANAPI_IT_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        if data.get("code") == 200:
            return data.get("result", {}).get("newslist", [])
        else:
            print(f"天行 IT API 错误: {data.get('code')} - {data.get('msg', '未知错误')}")
            return None
    except requests.RequestException as e:
        print(f"天行 IT API 请求失败: {e}")
        return None


def get_news_juhe(type_: str = "top", num: int = 10) -> Optional[List[Dict]]:
    """
    使用聚合数据 API 获取新闻（备用）

    Args:
        type_: 新闻类型 (top/headline/shehui/guonei/guoji等)
        num: 获取新闻数量

    Returns:
        新闻列表，失败返回 None
    """
    if not JUHE_KEY:
        return None

    params = {
        "type": type_,
        "key": JUHE_KEY,
        "page": 1,
        "page_size": num,
    }

    try:
        response = requests.get(JUHE_NEWS_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        if data.get("error_code") == 0:
            return data.get("result", {}).get("data", [])
        else:
            print(f"聚合 API 错误: {data.get('error_code')} - {data.get('reason', '未知错误')}")
            return None
    except requests.RequestException as e:
        print(f"聚合 API 请求失败: {e}")
        return None


def get_top_news(num: int = 10) -> List[Dict]:
    """
    获取热点新闻，优先使用天行数据，失败则尝试聚合数据

    Args:
        num: 获取新闻数量

    Returns:
        标准化的新闻列表
    """
    # 尝试天行数据
    news = get_news_tianapi(num)
    if news:
        return [
            {
                "title": item.get("title", ""),
                "description": item.get("digest", item.get("title", "")),
                "source": item.get("source", "天行数据"),
                "url": item.get("url", ""),
                "time": item.get("mtime", ""),
            }
            for item in news
        ]

    # 尝试聚合数据
    news = get_news_juhe("top", num)
    if news:
        return [
            {
                "title": item.get("title", ""),
                "description": item.get("title", ""),  # 聚合数据可能没有描述
                "source": item.get("author_name", "未知来源"),
                "url": item.get("url", ""),
                "time": item.get("date", ""),
            }
            for item in news
        ]

    return []


def format_news_html(news_list: List[Dict]) -> str:
    """
    格式化新闻列表为 HTML
    """
    if not news_list:
        return '<div class="section"><p style="color: #999;">新闻数据获取失败</p></div>'

    html_parts = []
    html_parts.append('<div class="section">')
    html_parts.append('<div class="section-title"><span class="icon">News</span><h2>今日热点</h2></div>')
    html_parts.append('<ul class="news-list">')

    for i, news in enumerate(news_list, 1):
        title = news.get("title", "无标题")
        source = news.get("source", "")
        url = news.get("url", "")
        time = news.get("time", "")

        html_parts.append(f'<li>')
        html_parts.append(f'<a href="{url}" target="_blank">')
        html_parts.append(f'<span class="num">{i}</span>{title}')
        html_parts.append(f'</a>')
        if source or time:
            html_parts.append(f'<div class="meta">{source} {time}</div>')
        html_parts.append('</li>')

    html_parts.append('</ul>')
    html_parts.append('</div>')
    return "".join(html_parts)


def format_news_text(news_list: List[Dict]) -> str:
    """
    格式化新闻列表为纯文本
    """
    if not news_list:
        return "新闻数据获取失败: 未配置 API Key 或 API 不可用"

    lines = []
    lines.append("=" * 50)
    lines.append("[昨日热点新闻 Top 10]")
    lines.append("=" * 50)

    for i, news in enumerate(news_list, 1):
        title = news.get("title", "无标题")
        source = news.get("source", "")
        url = news.get("url", "")

        lines.append(f"\n{i}. {title}")
        if source:
            lines.append(f"   来源: {source}")
        if url:
            lines.append(f"   链接: {url}")

    return "\n".join(lines)


def get_news_html() -> str:
    """
    获取新闻并返回 HTML 格式
    """
    news = get_top_news(10)
    return format_news_html(news)


def get_news_text() -> str:
    """
    获取新闻并返回纯文本格式
    """
    news = get_top_news(10)
    return format_news_text(news)


def get_it_news(num: int = 10) -> List[Dict]:
    """
    获取 IT 资讯

    Args:
        num: 获取新闻数量

    Returns:
        标准化的新闻列表
    """
    news = get_it_news_tianapi(num)
    if news:
        return [
            {
                "title": item.get("title", ""),
                "description": item.get("description", item.get("title", "")),
                "source": item.get("source", "未知来源"),
                "url": item.get("url", ""),
                "time": item.get("ctime", ""),
            }
            for item in news
        ]
    return []


def format_it_news_html(news_list: List[Dict]) -> str:
    """
    格式化 IT 资讯列表为 HTML
    """
    if not news_list:
        return '<div class="section"><p style="color: #999;">IT 资讯获取失败</p></div>'

    html_parts = []
    html_parts.append('<div class="section">')
    html_parts.append('<div class="section-title"><span class="icon">IT</span><h2>IT 资讯</h2></div>')
    html_parts.append('<ul class="news-list">')

    for i, news in enumerate(news_list, 1):
        title = news.get("title", "无标题")
        source = news.get("source", "")
        url = news.get("url", "")
        time = news.get("time", "")

        html_parts.append(f'<li>')
        html_parts.append(f'<a href="{url}" target="_blank">')
        html_parts.append(f'<span class="num">{i}</span>{title}')
        html_parts.append(f'</a>')
        if source or time:
            html_parts.append(f'<div class="meta">{source} {time}</div>')
        html_parts.append('</li>')

    html_parts.append('</ul>')
    html_parts.append('</div>')
    return "".join(html_parts)


def format_it_news_text(news_list: List[Dict]) -> str:
    """
    格式化 IT 资讯列表为纯文本
    """
    if not news_list:
        return "IT 资讯获取失败: 未配置 API Key 或 API 不可用"

    lines = []
    lines.append("=" * 50)
    lines.append("[IT 资讯 Top 10]")
    lines.append("=" * 50)

    for i, news in enumerate(news_list, 1):
        title = news.get("title", "无标题")
        source = news.get("source", "")
        url = news.get("url", "")

        lines.append(f"\n{i}. {title}")
        if source:
            lines.append(f"   来源: {source}")
        if url:
            lines.append(f"   链接: {url}")

    return "\n".join(lines)


def get_it_news_html() -> str:
    """
    获取 IT 资讯并返回 HTML 格式
    """
    news = get_it_news(10)
    return format_it_news_html(news)


def get_it_news_text() -> str:
    """
    获取 IT 资讯并返回纯文本格式
    """
    news = get_it_news(10)
    return format_it_news_text(news)


if __name__ == "__main__":
    # 测试运行
    print(get_news_text())
