#!/usr/bin/env python3
"""
发送飞书通知
"""
import json
import os
import sys
from datetime import datetime

def format_message(games_data):
    """格式化飞书消息"""
    if not games_data:
        return None

    current = games_data.get("current_free_games", [])
    upcoming = games_data.get("upcoming_free_games", [])
    timestamp = games_data.get("timestamp", "")

    # 简单的文本消息
    lines = []

    if current:
        lines.append("🎮 **Epic Games 本周免费游戏**\n")
        for game in current:
            lines.append(f"**{game['title']}**")
            lines.append(f"原价: {game['original_price']}")
            lines.append(f"限时: {game['start']} - {game['end']}")
            if game.get('description'):
                lines.append(f"简介: {game['description']}")
            lines.append("")
    else:
        lines.append("🎮 **Epic Games 本周暂无免费游戏**\n")

    if upcoming:
        lines.append("📅 **即将免费**\n")
        for game in upcoming:
            lines.append(f"**{game['title']}**")
            lines.append(f"原价: {game['original_price']}")
            lines.append(f"免费时间: {game['start']} - {game['end']}")
            lines.append("")

    lines.append(f"更新时间: {timestamp}")
    lines.append("链接: https://store.epicgames.com/zh-CN/free-games")

    return "\n".join(lines)

def main():
    """主函数"""
    input_data = sys.stdin.read()
    try:
        games_data = json.loads(input_data)
    except json.JSONDecodeError:
        message = "❌ **Epic Games 每周免费游戏通知**\n\n**错误**: 无法解析游戏数据"
        print(message)
        sys.exit(0)

    message = format_message(games_data)
    if not message:
        message = "❌ **Epic Games 每周免费游戏通知**\n\n**本周暂无免费游戏信息**"

    print(message)

if __name__ == "__main__":
    main()
