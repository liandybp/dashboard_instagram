#!/usr/bin/env python3

import requests
import time
import json
from dotenv import load_dotenv
load_dotenv(override=True)

# Custom exceptions
class AuthError(Exception):
    pass

class AddonRequiredError(Exception):
    pass

# Base URL for Zernio API
BASE_URL = "https://api.zernio.com/v1"

def _request(method, path, params=None):
    """
    Internal request function with retry logic and error handling.
    
    Args:
        method: HTTP method (GET, POST, etc.)
        path: API endpoint path
        params: Query parameters (optional)
        
    Returns:
        JSON response if successful
        
    Raises:
        AuthError: For 401 errors
        AddonRequiredError: For 402/403 errors
        requests.RequestException: For network issues
    """
    headers = {
        "Authorization": f"Bearer {ZERNIO_API_KEY}"
    }
    
    # Retry logic for 5xx and 429 errors
    retries = [2, 3, 5, 9]  # seconds to wait between retries
    last_exception = None
    
    for i, wait_time in enumerate(retries):
        try:
            url = f"{BASE_URL}{path}"
            
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, params=params)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            # Handle different status codes
            if response.status_code == 401:
                raise AuthError("API key expirada o inválida")
            elif response.status_code == 402:
                raise AddonRequiredError("Activa el add-on Analytics en zernio.com")
            elif response.status_code == 403:
                raise AddonRequiredError("Activa el add-on Inbox en zernio.com")
            elif response.status_code == 200:
                return response.json()
            elif response.status_code in [500, 501, 502, 503, 504, 429]:
                # Retry for server errors and rate limiting
                if i < len(retries) - 1:  # Don't sleep after the last retry
                    time.sleep(wait_time)
                    continue
                else:
                    response.raise_for_status()
            else:
                response.raise_for_status()
                
        except requests.RequestException as e:
            last_exception = e
            if i < len(retries) - 1:  # Don't sleep after the last retry
                time.sleep(wait_time)
                continue
            else:
                raise e
    
    if last_exception:
        raise last_exception

def fetch_account_id(api_key, platform):
    """
    Fetch account ID for a specific platform.
    
    Args:
        api_key: Zernio API key
        platform: 'instagram' or 'youtube'
        
    Returns:
        Account ID string
    """
    global ZERNIO_API_KEY
    ZERNIO_API_KEY = api_key
    
    # Get accounts list
    accounts_data = _request("GET", "/accounts")
    
    # Find account by platform
    for account in accounts_data.get("accounts", []):
        if account.get("platform") == platform:
            return account.get("id")
    
    return None

def get_daily_metrics(account_id, start_date=None, end_date=None):
    """Get daily metrics for an account."""
    params = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    return _request("GET", f"/analytics/daily-metrics/{account_id}", params)

def get_account_insights(account_id, platform):
    """Get account insights for Instagram or YouTube."""
    return _request("GET", f"/analytics/{platform}/account-insights/{account_id}")

def get_post_engagement_metrics(account_id, post_id=None, start_date=None, end_date=None):
    """Get engagement metrics for posts."""
    params = {}
    if post_id:
        params["post_id"] = post_id
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    return _request("GET", f"/analytics/instagram/post-engagement-metrics/{account_id}", params)

def get_post_insights(account_id, post_id):
    """Get insights for a specific Instagram post."""
    return _request("GET", f"/analytics/instagram/post-insights/{account_id}/{post_id}")

def get_story_insights(account_id, story_id):
    """Get insights for a specific Instagram story."""
    return _request("GET", f"/analytics/instagram/story-insights/{account_id}/{story_id}")

def get_video_insights(account_id, video_id):
    """Get insights for a specific YouTube video."""
    return _request("GET", f"/analytics/youtube/video-insights/{account_id}/{video_id}")

def get_comment_insights(account_id, post_id, comment_id=None):
    """Get comment insights for a post."""
    params = {}
    if comment_id:
        params["comment_id"] = comment_id
    return _request("GET", f"/analytics/instagram/comment-insights/{account_id}/{post_id}", params)

def get_reel_insights(account_id, reel_id):
    """Get insights for a specific Instagram reel."""
    return _request("GET", f"/analytics/instagram/reel-insights/{account_id}/{reel_id}")

def get_story_stories(account_id, start_date=None, end_date=None):
    """Get story stories for an account."""
    params = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    return _request("GET", f"/analytics/instagram/story-stories/{account_id}", params)

def get_user_insights(account_id, user_id):
    """Get insights for a specific user."""
    return _request("GET", f"/analytics/instagram/user-insights/{account_id}/{user_id}")

def get_inbox_messages(account_id, start_date=None, end_date=None):
    """Get inbox messages for an account."""
    params = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    return _request("GET", f"/inbox/messages/{account_id}", params)

def get_inbox_conversations(account_id, start_date=None, end_date=None):
    """Get inbox conversations for an account."""
    params = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    return _request("GET", f"/inbox/conversations/{account_id}", params)

def get_inbox_users(account_id, start_date=None, end_date=None):
    """Get inbox users for an account."""
    params = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    return _request("GET", f"/inbox/users/{account_id}", params)

def get_inbox_message(account_id, message_id):
    """Get a specific inbox message."""
    return _request("GET", f"/inbox/messages/{account_id}/{message_id}")

def get_inbox_conversation(account_id, conversation_id):
    """Get a specific inbox conversation."""
    return _request("GET", f"/inbox/conversations/{account_id}/{conversation_id}")

def validate_all_endpoints(zernio_api_key, account_id_ig, account_id_yt=None):
    """
    Validate all endpoints and report which ones work and which fail.
    
    Args:
        zernio_api_key: API key for authentication
        account_id_ig: Instagram account ID
        account_id_yt: YouTube account ID (optional)
        
    Returns:
        Dictionary with endpoint validation results
    """
    print("Validating all Zernio endpoints...")
    print("=" * 50)
    
    # Set global API key for use in _request function
    global ZERNIO_API_KEY
    ZERNIO_API_KEY = zernio_api_key
    
    # Test endpoints
    test_cases = [
        ("Daily Metrics", lambda: get_daily_metrics(account_id_ig)),
        ("Account Insights (Instagram)", lambda: get_account_insights(account_id_ig, "instagram")),
        ("Post Engagement Metrics", lambda: get_post_engagement_metrics(account_id_ig)),
        ("Post Insights", lambda: get_post_insights(account_id_ig, "some-post-id")),
        ("Story Insights", lambda: get_story_insights(account_id_ig, "some-story-id")),
        ("Comment Insights", lambda: get_comment_insights(account_id_ig, "some-post-id")),
        ("Reel Insights", lambda: get_reel_insights(account_id_ig, "some-reel-id")),
        ("Story Stories", lambda: get_story_stories(account_id_ig)),
        ("User Insights", lambda: get_user_insights(account_id_ig, "some-user-id")),
        ("Inbox Messages", lambda: get_inbox_messages(account_id_ig)),
        ("Inbox Conversations", lambda: get_inbox_conversations(account_id_ig)),
        ("Inbox Users", lambda: get_inbox_users(account_id_ig)),
    ]
    
    # Add YouTube-specific endpoints if account_id_yt is provided
    if account_id_yt:
        test_cases.extend([
            ("Account Insights (YouTube)", lambda: get_account_insights(account_id_yt, "youtube")),
            ("Video Insights", lambda: get_video_insights(account_id_yt, "some-video-id")),
        ])
    
    results = {}
    
    for endpoint_name, endpoint_func in test_cases:
        try:
            result = endpoint_func()
            results[endpoint_name] = {"status": "SUCCESS", "result": result}
            print(f"✅ {endpoint_name}: SUCCESS")
        except AuthError as e:
            results[endpoint_name] = {"status": "AUTH_ERROR", "error": str(e)}
            print(f"❌ {endpoint_name}: AUTH ERROR - {e}")
        except AddonRequiredError as e:
            results[endpoint_name] = {"status": "ADDON_REQUIRED", "error": str(e)}
            print(f"⚠️  {endpoint_name}: ADDON REQUIRED - {e}")
        except Exception as e:
            results[endpoint_name] = {"status": "ERROR", "error": str(e)}
            print(f"❌ {endpoint_name}: ERROR - {e}")
    
    return results

# If this file is run directly, you can test with environment variables
if __name__ == "__main__":
    # Load environment variables (this will use .env file if it exists)
    from dotenv import load_dotenv
    load_dotenv(override=True)
    
    # Example usage:
    # You would normally get these from environment variables or other sources
    # api_key = os.getenv("ZERNIO_API_KEY")
    # account_id_ig = os.getenv("ZERNIO_ACCOUNT_ID") 
    # account_id_yt = os.getenv("ZERNIO_ACCOUNT_ID_YOUTUBE")
    
    # For debugging purposes, you can uncomment and set these directly:
    # api_key = "your_api_key_here"
    # account_id_ig = "your_instagram_account_id"
    # validate_all_endpoints(api_key, account_id_ig)
    pass