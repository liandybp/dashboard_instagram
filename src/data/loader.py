#!/usr/bin/env python3

import os
import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from cache import write_account_health

# Load environment variables from project files
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / "env", override=True)
load_dotenv(PROJECT_ROOT / ".env", override=True)

# Import the Zernio client
try:
    from src.api.client import ZernioClient, AddonRequiredError, AuthError
except ImportError as e:
    print(f"Error importing Zernio client: {e}")
    sys.exit(1)


def _build_fallback_data(reason: str = ""):
    """Return a safe data payload compatible with all dashboard tabs."""
    now = datetime.now().isoformat()
    if reason:
        print(f"Using fallback data: {reason}")

    return {
        "account_snapshot": {
            "id": "fallback_instagram_account",
            "platform": "instagram",
            "username": "demo_instagram",
            # Keep both keys for backward compatibility across tabs.
            "follower_count": 0,
            "followers_count": 0,
            "posts_count": 0,
            "engagement_rate": 0.0,
            "reach": 0,
            "profile_image": "",
            "updated_at": now,
        },
        "account_health": {
            "id": "fallback_instagram_account",
            "platform": "instagram",
            "status": "unknown",
            "checked_at": now,
            "message": "Datos de fallback cargados",
        },
        "daily_metrics": [],
        "posts": [],
        "comments": [],
        "follower_history": [],
        "best_time_to_post": [],
        "posting_frequency": [],
        "content_decay": [],
        "demographics": {
            "instagram": {"age": [], "gender": [], "country": [], "city": []},
            "youtube": {"age": [], "gender": [], "country": []},
        },
    }


def _extract_list(payload: dict, keys: list):
    """Extract a list from a payload trying multiple common key names."""
    if isinstance(payload, list):
        return payload
    if not isinstance(payload, dict):
        return []

    for key in keys:
        value = payload.get(key)
        if isinstance(value, list):
            return value
        if isinstance(value, dict):
            nested = _extract_list(value, keys)
            if nested:
                return nested

    for value in payload.values():
        if isinstance(value, dict):
            nested = _extract_list(value, keys)
            if nested:
                return nested
    return []


def _to_float(value, default=0.0):
    try:
        if value is None or value == "":
            return float(default)
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def _pick_first(data: dict, keys: list, default=None):
    if not isinstance(data, dict):
        return default
    for key in keys:
        if key in data and data.get(key) is not None:
            return data.get(key)
    return default


def _extract_accounts(payload):
    """Return a flat list of account dicts from any common API shape."""
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return []
    for key in ["accounts", "data", "items", "results"]:
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
        if isinstance(value, dict):
            nested = _extract_accounts(value)
            if nested:
                return nested
    return []


def _normalize_daily_metrics(daily_items: list):
    """Map daily metrics to a stable shape used by MetricsTab."""
    normalized = []
    for item in daily_items:
        if not isinstance(item, dict):
            continue
        date = _pick_first(item, ["date", "day", "timestamp", "createdAt"]) 
        if not date:
            continue

        reach = _to_float(_pick_first(item, ["reach", "accounts_reached", "totalReach", "avgReach"], 0), 0)
        engagements = _to_float(_pick_first(item, ["engagements", "engagement", "totalEngagement", "interactions", "engaged"], 0), 0)
        engagement_rate = _to_float(_pick_first(item, ["engagement_rate", "engagementRate", "avgEngagementRate"], None), 0)
        if engagement_rate == 0 and reach > 0:
            engagement_rate = (engagements / reach) * 100

        normalized.append(
            {
                "date": str(date)[:10],
                "reach": int(reach),
                "engagements": int(engagements),
                "engagement_rate": float(round(engagement_rate, 2)),
            }
        )

    normalized.sort(key=lambda x: x["date"])
    return normalized


def _normalize_best_time(items: list):
    normalized = []
    day_map = {
        0: "Lunes", 1: "Martes", 2: "Miercoles", 3: "Jueves",
        4: "Viernes", 5: "Sabado", 6: "Domingo",
    }
    for item in items:
        if not isinstance(item, dict):
            continue
        hour = _pick_first(item, ["hour", "hora"], None)
        if hour is None:
            continue
        day = _pick_first(item, ["day_of_week", "dayOfWeek", "day"], None)
        if isinstance(day, int):
            day_label = day_map.get(day, str(day))
        else:
            day_label = str(day) if day is not None else "N/A"
        value = _to_float(_pick_first(item, ["value", "score", "avg_engagement", "avgEngagement"], 0), 0)
        normalized.append({"day_of_week": day_label, "hour": int(_to_float(hour, 0)), "value": float(value)})
    return normalized


def _normalize_posting_frequency(items: list):
    normalized = []
    for item in items:
        if not isinstance(item, dict):
            continue
        ppw = _to_float(_pick_first(item, ["postsPerWeek", "posts_per_week", "x"], None), None)
        er = _to_float(_pick_first(item, ["avgEngagementRate", "engagement_rate", "y"], None), None)
        if ppw is None or er is None:
            continue
        normalized.append({
            "posts_per_week": float(ppw),
            "avg_engagement_rate": float(er),
            "weeks_count": int(_to_float(_pick_first(item, ["weeksCount", "weeks_count"], 1), 1)),
        })
    return normalized


def _normalize_content_decay(items: list):
    normalized = []
    for item in items:
        if not isinstance(item, dict):
            continue
        bucket = _pick_first(item, ["bucketLabel", "bucket", "label"], None)
        pct = _to_float(_pick_first(item, ["avgPctOfFinal", "value", "percentage"], None), None)
        if bucket is None or pct is None:
            continue
        normalized.append({"bucket": str(bucket), "avg_pct_of_final": float(pct)})
    return normalized


def _normalize_demographics(items: list):
    normalized = []
    for item in items:
        if not isinstance(item, dict):
            continue
        label = _pick_first(item, ["label", "name", "value", "key", "bucket"], None)
        count = _pick_first(item, ["count", "value", "followers", "audience"], None)
        if label is None or count is None:
            continue
        normalized.append({"label": str(label), "count": float(_to_float(count, 0))})
    total = sum(x["count"] for x in normalized)
    if total > 0:
        for row in normalized:
            row["pct"] = round((row["count"] / total) * 100, 2)
    else:
        for row in normalized:
            row["pct"] = 0.0
    return normalized


def _derive_snapshot_metrics(instagram_account: dict, health_result: dict, daily_metrics: list, posts: list, analytics_overview: dict = None):
    """Derive robust KPIs for snapshot using multiple API sources."""
    account = instagram_account if isinstance(instagram_account, dict) else {}
    health = health_result if isinstance(health_result, dict) else {}

    followers = _pick_first(
        health,
        ["followers", "followers_count", "follower_count", "followersCount"],
        None,
    )
    if followers is None:
        followers = _pick_first(
            account,
            ["followers", "followers_count", "follower_count", "followersCount"],
            0,
        )

    posts_from_feed = len(posts) if posts else 0
    posts_from_account = int(
        _to_float(
            _pick_first(account, ["posts_count", "postsCount", "media_count", "mediaCount"], 0),
            0,
        )
    )
    overview = analytics_overview if isinstance(analytics_overview, dict) else {}
    posts_from_overview = int(
        _to_float(
            _pick_first(overview, ["totalPosts", "publishedPosts", "posts", "postCount"], 0),
            0,
        )
    )
    posts_count = max(posts_from_feed, posts_from_account, posts_from_overview)

    latest_daily = daily_metrics[-1] if daily_metrics else {}
    reach_value = _pick_first(latest_daily, ["reach"], None)
    if reach_value is None:
        reach_value = _pick_first(health, ["reach", "totalReach"], None)
    reach = float(reach_value) if reach_value is not None else None

    engagement_value = _pick_first(latest_daily, ["engagement_rate"], None)
    if engagement_value is None:
        engagement_value = _pick_first(health, ["engagement_rate", "engagementRate", "avgEngagementRate"], None)
    engagement_rate = float(engagement_value) if engagement_value is not None else None

    if engagement_rate is None and posts:
        total_reach = 0.0
        total_eng = 0.0
        for post in posts:
            if not isinstance(post, dict):
                continue
            post_reach = _to_float(_pick_first(post, ["reach", "accounts_reached"], 0), 0)
            likes = _to_float(_pick_first(post, ["likes", "likes_count", "likesCount"], 0), 0)
            comments = _to_float(_pick_first(post, ["comments", "comments_count", "commentsCount"], 0), 0)
            saves = _to_float(_pick_first(post, ["saves", "saves_count", "savesCount"], 0), 0)
            shares = _to_float(_pick_first(post, ["shares", "shares_count", "sharesCount"], 0), 0)
            total_reach += post_reach
            total_eng += likes + comments + saves + shares
        if total_reach > 0:
            engagement_rate = (total_eng / total_reach) * 100

    return {
        "followers_count": int(_to_float(followers, 0)),
        "posts_count": int(posts_count),
        "reach": int(_to_float(reach, 0)) if reach is not None else None,
        "engagement_rate": float(round(engagement_rate, 2)) if engagement_rate is not None else None,
    }


def _normalize_health_data(raw_health: dict, account_id: str, platform: str):
    """Normalize health payload so UI and cache can read a stable shape."""
    now = datetime.now().isoformat()
    raw = raw_health if isinstance(raw_health, dict) else {}

    token_valid = bool(raw.get("token_valid", raw.get("tokenValid", True)))
    is_active = bool(raw.get("is_active", raw.get("isActive", True)))
    is_verified = bool(raw.get("is_verified", raw.get("isVerified", False)))
    is_restricted = bool(raw.get("is_restricted", raw.get("isRestricted", False)))
    scopes_ok = bool(raw.get("scopes_ok", raw.get("scopesOk", True)))

    missing_scopes = raw.get("missing_scopes", raw.get("missingScopes", [])) or []
    issues = raw.get("issues", []) or []
    recommendations = raw.get("recommendations", []) or []

    ui_health = {
        "id": account_id,
        "platform": platform,
        "status": raw.get("health_status", raw.get("status", "unknown")),
        "checked_at": raw.get("checked_at", now),
        "token_valid": token_valid,
        "is_active": is_active,
        "is_verified": is_verified,
        "is_restricted": is_restricted,
        "scopes_ok": scopes_ok,
        "missing_scopes": missing_scopes,
        "issues": issues,
        "recommendations": recommendations,
    }

    db_health = {
        "id": account_id,
        "platform": platform,
        "status": ui_health["status"],
        "checked_at": ui_health["checked_at"],
        "tokenValid": token_valid,
        "isActive": is_active,
        "isVerified": is_verified,
        "isRestricted": is_restricted,
        "scopesOk": scopes_ok,
        "missingScopes": missing_scopes,
        "issues": issues,
        "recommendations": recommendations,
    }

    return ui_health, db_health

def load_account_data_from_zernio_with_fallback():
    """Load account data from Zernio API using the official client with fallback to mock data."""
    
    try:
        # Initialize the Zernio client
        client = ZernioClient()
        
        # Get account information
        accounts_result = client.list_accounts()
        accounts = _extract_accounts(accounts_result)
        if not accounts:
            print("No accounts found")
            return _build_fallback_data("No accounts in API response")
            
        # Find Instagram account
        instagram_account = None
        for account in accounts:
            if str(account.get('platform', '')).lower() == 'instagram':
                instagram_account = account
                break
                
        if not instagram_account:
            print("No Instagram account found")
            return _build_fallback_data("No Instagram account available")
            
        account_id = (
            instagram_account.get('_id')
            or instagram_account.get('id')
            or instagram_account.get('accountId')
            or instagram_account.get('account_id')
        )
        if not account_id:
            return _build_fallback_data("Instagram account without id")
        
        # Load account health (this is what we use for account snapshot)
        # Use the correct Instagram account insights endpoint
        try:
            health_result = client.get_instagram_account_insights(account_id=account_id)
        except AddonRequiredError as e:
            print(f"Addon required for health data: {e}")
            health_result = {}
        except Exception as e:
            print(f"Error getting account health: {e}")
            health_result = {}
            
        # Load daily analytics (this is what we use for daily metrics)
        try:
            daily_result = client.get_daily_metrics(platform="instagram", account_id=account_id)
        except AddonRequiredError as e:
            print(f"Addon required for daily analytics: {e}")
            daily_result = {"metrics": []}
        except Exception as e:
            print(f"Error getting daily analytics: {e}")
            daily_result = {"metrics": []}
            
        # Load follower stats (this is what we use for follower history)
        try:
            follower_result = client.get_follower_stats(account_id=account_id, platform="instagram")
        except AddonRequiredError as e:
            print(f"Addon required for follower stats: {e}")
            follower_result = {"history": []}
        except Exception as e:
            print(f"Error getting follower stats: {e}")
            follower_result = {"history": []}
            
        # Load best time to post
        try:
            best_time_result = client.get_best_time_to_post(platform="instagram", account_id=account_id)
        except AddonRequiredError as e:
            print(f"Addon required for best time data: {e}")
            best_time_result = {"best_time": []}
        except Exception as e:
            print(f"Error getting best time data: {e}")
            best_time_result = {"best_time": []}
            
        # Load comments (this is what we use for comments)
        try:
            comments_result = client.list_inbox_comments(account_id=account_id, platform="instagram")
        except AddonRequiredError as e:
            print(f"Addon required for comments: {e}")
            comments_result = {"comments": []}
        except Exception as e:
            print(f"Error getting comments: {e}")
            comments_result = {"comments": []}

        # Load posting frequency
        try:
            posting_frequency_result = client.get_posting_frequency(platform="instagram", account_id=account_id)
        except AddonRequiredError as e:
            print(f"Addon required for posting frequency: {e}")
            posting_frequency_result = {"data": []}
        except Exception as e:
            print(f"Error getting posting frequency: {e}")
            posting_frequency_result = {"data": []}

        # Load content decay
        try:
            content_decay_result = client.get_content_decay(platform="instagram", account_id=account_id)
        except AddonRequiredError as e:
            print(f"Addon required for content decay: {e}")
            content_decay_result = {"data": []}
        except Exception as e:
            print(f"Error getting content decay: {e}")
            content_decay_result = {"data": []}

        # Load demographics IG (age, gender, country, city)
        def _safe_demographics(breakdown: str):
            try:
                return client.get_demographics(account_id=account_id, breakdown=breakdown)
            except AddonRequiredError as e:
                print(f"Addon required for demographics {breakdown}: {e}")
            except Exception as e:
                print(f"Error getting demographics {breakdown}: {e}")
            return {"data": []}

        demographics_age_ig = _safe_demographics("age")
        demographics_gender_ig = _safe_demographics("gender")
        demographics_country_ig = _safe_demographics("country")
        demographics_city_ig = _safe_demographics("city")

        # Load demographics YT (si hay cuenta conectada)
        demographics_age_yt = {"data": []}
        demographics_gender_yt = {"data": []}
        demographics_country_yt = {"data": []}
        yt_account_id = client.account_id_youtube
        if yt_account_id:
            try:
                demographics_age_yt = client.get_demographics(account_id=yt_account_id, breakdown="age")
                demographics_gender_yt = client.get_demographics(account_id=yt_account_id, breakdown="gender")
                demographics_country_yt = client.get_demographics(account_id=yt_account_id, breakdown="country")
            except Exception as e:
                print(f"Error getting youtube demographics: {e}")
            
        # Load posts (this is what we use for posts)
        try:
            posts_result = client.get_analytics(platform="instagram", account_id=account_id)
        except AddonRequiredError as e:
            print(f"Addon required for posts: {e}")
            posts_result = {"posts": []}
        except Exception as e:
            print(f"Error getting posts: {e}")
            posts_result = {"posts": []}
            
        platform = instagram_account.get('platform', 'instagram')
        account_health_data, db_health_data = _normalize_health_data(health_result, account_id, platform)
        try:
            write_account_health(db_health_data)
        except Exception as e:
            print(f"Warning: failed to persist account health in cache: {e}")

        daily_metrics = _normalize_daily_metrics(
            _extract_list(daily_result, ["metrics", "dailyMetrics", "dailyData", "data", "rows", "items"])
        )
        analytics_overview = posts_result.get("overview", {}) if isinstance(posts_result, dict) else {}
        posts = _extract_list(posts_result, ["posts", "data", "items", "analytics"])
        comments = _extract_list(comments_result, ["comments", "data", "items"])
        follower_history = _extract_list(follower_result, ["history", "data", "rows"])
        best_time_to_post = _normalize_best_time(
            _extract_list(best_time_result, ["best_time", "bestTime", "slots", "data", "items"])
        )
        posting_frequency = _normalize_posting_frequency(
            _extract_list(posting_frequency_result, ["data", "rows", "items", "postingFrequency"])
        )
        content_decay = _normalize_content_decay(
            _extract_list(content_decay_result, ["data", "rows", "items", "contentDecay", "buckets"])
        )

        demographics = {
            "instagram": {
                "age": _normalize_demographics(_extract_list(demographics_age_ig, ["data", "rows", "items", "demographics"])),
                "gender": _normalize_demographics(_extract_list(demographics_gender_ig, ["data", "rows", "items", "demographics"])),
                "country": _normalize_demographics(_extract_list(demographics_country_ig, ["data", "rows", "items", "demographics"])),
                "city": _normalize_demographics(_extract_list(demographics_city_ig, ["data", "rows", "items", "demographics"])),
            },
            "youtube": {
                "age": _normalize_demographics(_extract_list(demographics_age_yt, ["data", "rows", "items", "demographics"])),
                "gender": _normalize_demographics(_extract_list(demographics_gender_yt, ["data", "rows", "items", "demographics"])),
                "country": _normalize_demographics(_extract_list(demographics_country_yt, ["data", "rows", "items", "demographics"])),
            },
        }

        snapshot_metrics = _derive_snapshot_metrics(
            instagram_account=instagram_account,
            health_result=health_result,
            daily_metrics=daily_metrics,
            posts=posts,
            analytics_overview=analytics_overview,
        )
            
        return {
            'account_snapshot': {
                "id": account_id,
                "platform": platform,
                "username": instagram_account.get('username', ''),
                "follower_count": snapshot_metrics["followers_count"],
                "followers_count": snapshot_metrics["followers_count"],
                "posts_count": snapshot_metrics["posts_count"],
                "engagement_rate": snapshot_metrics["engagement_rate"],
                "reach": snapshot_metrics["reach"],
                "profile_image": (health_result or {}).get('profile_pic_url', ''),
                "updated_at": datetime.now().isoformat()
            },
            'account_health': account_health_data,
            'daily_metrics': daily_metrics,
            'posts': posts,
            'comments': comments,
            'follower_history': follower_history,
            'best_time_to_post': best_time_to_post,
            'posting_frequency': posting_frequency,
            'content_decay': content_decay,
            'demographics': demographics
        }
        
    except AuthError as e:
        print(f"Authentication error: {e}")
        return _build_fallback_data("Authentication error")
    except Exception as e:
        print(f"Error loading data from Zernio: {e}")
        import traceback
        traceback.print_exc()
        return _build_fallback_data("Unhandled exception while loading data")

if __name__ == "__main__":
    # Test the function
    data = load_account_data_from_zernio_with_fallback()
    if data:
        print("Data loaded successfully")
        print(f"Username: {data['account_snapshot']['username']}")
        print(f"Followers: {data['account_snapshot']['follower_count']}")
        print(f"Posts count: {len(data['posts'])}")
        print(f"Comments count: {len(data['comments'])}")
    else:
        print("Failed to load data from Zernio")