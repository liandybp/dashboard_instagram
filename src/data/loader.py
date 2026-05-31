#!/usr/bin/env python3

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from cache import write_account_health

# Load environment variables
load_dotenv(override=True)

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
    }


def _extract_list(payload: dict, keys: list):
    """Extract a list from a payload trying multiple common key names."""
    if not isinstance(payload, dict):
        return []
    for key in keys:
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


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
        if not accounts_result or 'accounts' not in accounts_result:
            print("No accounts found")
            return _build_fallback_data("No accounts in API response")
            
        # Find Instagram account
        instagram_account = None
        for account in accounts_result['accounts']:
            if account['platform'] == 'instagram':
                instagram_account = account
                break
                
        if not instagram_account:
            print("No Instagram account found")
            return _build_fallback_data("No Instagram account available")
            
        account_id = instagram_account.get('_id') or instagram_account.get('id')
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

        daily_metrics = _extract_list(daily_result, ["metrics", "dailyMetrics", "data", "rows"])
        posts = _extract_list(posts_result, ["posts", "data", "items", "analytics"])
        comments = _extract_list(comments_result, ["comments", "data", "items"])
        follower_history = _extract_list(follower_result, ["history", "data", "rows"])
        best_time_to_post = _extract_list(best_time_result, ["best_time", "bestTime", "slots", "data"])

        followers = (
            (health_result or {}).get("followers")
            or (health_result or {}).get("followers_count")
            or (health_result or {}).get("follower_count")
            or instagram_account.get("followers_count")
            or instagram_account.get("follower_count")
            or 0
        )
            
        return {
            'account_snapshot': {
                "id": account_id,
                "platform": platform,
                "username": instagram_account.get('username', ''),
                "follower_count": followers,
                "followers_count": followers,
                "posts_count": len(posts),
                "engagement_rate": 0.0,
                "reach": 0,
                "profile_image": (health_result or {}).get('profile_pic_url', ''),
                "updated_at": datetime.now().isoformat()
            },
            'account_health': account_health_data,
            'daily_metrics': daily_metrics,
            'posts': posts,
            'comments': comments,
            'follower_history': follower_history,
            'best_time_to_post': best_time_to_post
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