#!/usr/bin/env python3
"""
Epic Games 每周免费游戏通知脚本
获取当前免费游戏和即将免费的游戏信息
"""
import json
import ssl
import sys
from datetime import datetime
from urllib.request import urlopen
from urllib.error import URLError

def fetch_free_games():
    """获取Epic Games免费游戏信息"""
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        with urlopen(url, context=ctx) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data
    except URLError as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        return None

def is_currently_free(game):
    """检查游戏当前是否免费"""
    if not game.get("promotions"):
        return False

    promo = game["promotions"]
    if not promo.get("promotionalOffers"):
        return False

    # 检查当前促销时间
    now = datetime.now(datetime.now().astimezone().tzinfo)
    for offer in promo["promotionalOffers"][0]["promotionalOffers"]:
        start = datetime.fromisoformat(offer["startDate"].replace('Z', '+00:00'))
        end = datetime.fromisoformat(offer["endDate"].replace('Z', '+00:00'))
        if start <= now <= end:
            return True
    return False

def is_upcoming_free(game):
    """检查游戏即将免费"""
    if not game.get("promotions"):
        return False

    promo = game["promotions"]
    if not promo.get("upcomingPromotionalOffers"):
        return False

    now = datetime.now(datetime.now().astimezone().tzinfo)
    for upcoming in promo["upcomingPromotionalOffers"]:
        for offer in upcoming["promotionalOffers"]:
            start = datetime.fromisoformat(offer["startDate"].replace('Z', '+00:00'))
            if start > now:
                return True
    return False

def format_free_promotion(game):
    """格式化当前免费游戏信息"""
    promo = game["promotions"]["promotionalOffers"][0]["promotionalOffers"][0]
    start = datetime.fromisoformat(promo["startDate"].replace('Z', '+00:00'))
    end = datetime.fromisoformat(promo["endDate"].replace('Z', '+00:00'))

    return {
        "title": game.get("title", "Unknown"),
        "original_price": game["price"]["totalPrice"]["fmtPrice"]["originalPrice"],
        "url": game.get("urlSlug", ""),
        "start": start.strftime("%Y-%m-%d %H:%M UTC"),
        "end": end.strftime("%Y-%m-%d %H:%M UTC"),
        "description": game.get("description", "").strip()[:200]
    }

def format_upcoming_promotion(game):
    """格式化即将免费的游戏信息"""
    promo = game["promotions"]["upcomingPromotionalOffers"][0]["promotionalOffers"][0]
    start = datetime.fromisoformat(promo["startDate"].replace('Z', '+00:00'))
    end = datetime.fromisoformat(promo["endDate"].replace('Z', '+00:00'))

    return {
        "title": game.get("title", "Unknown"),
        "original_price": game["price"]["totalPrice"]["fmtPrice"]["originalPrice"],
        "url": game.get("urlSlug", ""),
        "start": start.strftime("%Y-%m-%d %H:%M UTC"),
        "end": end.strftime("%Y-%m-%d %H:%M UTC"),
        "description": game.get("description", "").strip()[:200]
    }

def main():
    """主函数"""
    data = fetch_free_games()
    if not data:
        print(json.dumps({"error": "Failed to fetch Epic Games data"}))
        sys.exit(1)

    games = data.get("data", {}).get("Catalog", {}).get("searchStore", {}).get("elements", [])

    current_free = []
    upcoming_free = []

    for game in games:
        if is_currently_free(game):
            current_free.append(format_free_promotion(game))
        elif is_upcoming_free(game):
            upcoming_free.append(format_upcoming_promotion(game))

    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        timestamp = datetime.utcnow().isoformat() + "Z"
    result = {
        "timestamp": timestamp,
        "current_free_games": current_free,
        "upcoming_free_games": upcoming_free
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 如果没有免费游戏，返回非0状态码
    if not current_free and not upcoming_free:
        sys.exit(1)

if __name__ == "__main__":
    main()
