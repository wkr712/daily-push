#!/usr/bin/env python3
"""
天气获取脚本 - 调用和风天气 API
获取广州和茂名各区域天气信息
"""

import os
import requests
from datetime import datetime
from typing import Dict, List, Optional

# 和风天气 API 配置
QWEATHER_API_KEY = os.environ.get("QWEATHER_API_KEY", "")
QWEATHER_API_HOST = os.environ.get("QWEATHER_API_HOST", "api.qweather.com")
QWEATHER_BASE_URL = f"https://{QWEATHER_API_HOST}/v7"

# 广州各区域 Location ID
GUANGZHOU_LOCATIONS = {
    "广州市": "101280101",
    "天河区": "101280102",
    "越秀区": "101280103",
    "海珠区": "101280104",
    "荔湾区": "101280105",
    "白云区": "101280106",
    "黄埔区": "101280107",
    "花都区": "101280108",
    "番禺区": "101280109",
    "南沙区": "101280110",
    "从化区": "101280111",
    "增城区": "101280112",
}

# 茂名各区域 Location ID
MAOMING_LOCATIONS = {
    "茂名市": "101282001",
    "茂南区": "101282002",
    "电白区": "101282003",
    "高州市": "101282004",
    "化州市": "101282005",
    "信宜市": "101282006",
}


def get_weather(location_id: str) -> Optional[Dict]:
    """
    获取指定位置的天气信息

    Args:
        location_id: 和风天气 Location ID

    Returns:
        天气数据字典，失败返回 None
    """
    if not QWEATHER_API_KEY:
        print("错误: 未配置 QWEATHER_API_KEY 环境变量")
        return None

    url = f"{QWEATHER_BASE_URL}/weather/now"
    params = {
        "location": location_id,
        "key": QWEATHER_API_KEY,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("code") == "200":
            return data.get("now", {})
        else:
            print(f"API 错误: {data.get('code')} - {data.get('message', '未知错误')}")
            return None
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return None


def get_weather_forecast(location_id: str, days: int = 3) -> Optional[List[Dict]]:
    """
    获取天气预报

    Args:
        location_id: 和风天气 Location ID
        days: 预报天数 (1-7)

    Returns:
        天气预报列表，失败返回 None
    """
    if not QWEATHER_API_KEY:
        return None

    url = f"{QWEATHER_BASE_URL}/weather/{days}d"
    params = {
        "location": location_id,
        "key": QWEATHER_API_KEY,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("code") == "200":
            return data.get("daily", [])
        return None
    except requests.RequestException:
        return None


def format_weather_text(name: str, weather: Dict) -> str:
    """
    格式化天气信息为文本
    """
    if not weather:
        return f"{name}: 暂无数据"

    temp = weather.get("temp", "--")
    feels_like = weather.get("feelsLike", "--")
    text = weather.get("text", "--")
    wind_dir = weather.get("windDir", "--")
    wind_scale = weather.get("windScale", "--")
    humidity = weather.get("humidity", "--")

    return f"{name}: {text}, {temp}°C (体感 {feels_like}°C), {wind_dir}{wind_scale}级, 湿度{humidity}%"


def get_all_weather_html() -> str:
    """
    获取所有区域的天气信息，返回 HTML 格式
    """
    if not QWEATHER_API_KEY:
        return '<div class="section"><div class="section-title"><span class="icon">Weather</span><h2>天气数据获取失败</h2></div><p style="color: #999;">未配置 API Key</p></div>'

    html_parts = []

    # 广州天气
    html_parts.append('<div class="section">')
    html_parts.append('<div class="section-title"><span class="icon">Guangzhou</span><h2>广州天气</h2></div>')
    html_parts.append('<div class="weather-grid">')

    for name, location_id in GUANGZHOU_LOCATIONS.items():
        weather = get_weather(location_id)
        if weather:
            temp = weather.get('temp', '--')
            text = weather.get('text', '--')
            feels_like = weather.get('feelsLike', '--')
            wind_dir = weather.get('windDir', '--')
            wind_scale = weather.get('windScale', '--')
            humidity = weather.get('humidity', '--')

            html_parts.append(f'''
            <div class="weather-card">
                <div class="location">{name}</div>
                <div class="condition">{text}</div>
                <div class="temp">{temp}°C</div>
                <div class="details">
                    体感 {feels_like}°C | {wind_dir}{wind_scale}级<br>
                    湿度 {humidity}%
                </div>
            </div>''')
        else:
            html_parts.append(f'''
            <div class="weather-card">
                <div class="location">{name}</div>
                <div class="details" style="color: #999;">获取失败</div>
            </div>''')

    html_parts.append('</div>')
    html_parts.append('</div>')

    # 茂名天气
    html_parts.append('<div class="section">')
    html_parts.append('<div class="section-title"><span class="icon">Maoming</span><h2>茂名天气</h2></div>')
    html_parts.append('<div class="weather-grid">')

    for name, location_id in MAOMING_LOCATIONS.items():
        weather = get_weather(location_id)
        if weather:
            temp = weather.get('temp', '--')
            text = weather.get('text', '--')
            feels_like = weather.get('feelsLike', '--')
            wind_dir = weather.get('windDir', '--')
            wind_scale = weather.get('windScale', '--')
            humidity = weather.get('humidity', '--')

            html_parts.append(f'''
            <div class="weather-card">
                <div class="location">{name}</div>
                <div class="condition">{text}</div>
                <div class="temp">{temp}°C</div>
                <div class="details">
                    体感 {feels_like}°C | {wind_dir}{wind_scale}级<br>
                    湿度 {humidity}%
                </div>
            </div>''')
        else:
            html_parts.append(f'''
            <div class="weather-card">
                <div class="location">{name}</div>
                <div class="details" style="color: #999;">获取失败</div>
            </div>''')

    html_parts.append('</div>')
    html_parts.append('</div>')

    return "".join(html_parts)


def get_weather_text() -> str:
    """
    获取所有区域的天气信息，返回纯文本格式
    """
    if not QWEATHER_API_KEY:
        return "天气数据获取失败: 未配置 API Key"

    lines = []
    lines.append("=" * 50)
    lines.append("[广州天气]")
    lines.append("=" * 50)

    for name, location_id in GUANGZHOU_LOCATIONS.items():
        weather = get_weather(location_id)
        lines.append(format_weather_text(name, weather))

    lines.append("")
    lines.append("=" * 50)
    lines.append("[茂名天气]")
    lines.append("=" * 50)

    for name, location_id in MAOMING_LOCATIONS.items():
        weather = get_weather(location_id)
        lines.append(format_weather_text(name, weather))

    return "\n".join(lines)


if __name__ == "__main__":
    # 测试运行
    print(get_weather_text())
