#!/usr/bin/env python3

import requests
import time
import json
import os
from dotenv import load_dotenv
load_dotenv(override=True)

# Custom exceptions
class AuthError(Exception):
    pass

class AddonRequiredError(Exception):
    pass

# Base URL for Zernio API
BASE_URL = "https://api.zernio.com/v1"

class ZernioClient:
    def __init__(self, api_key=None):
        """
        Initialize the Zernio Client.
        
        Args:
            api_key: Zernio API key (optional, will be loaded from environment if not provided)
        """
        self.api_key = api_key or os.getenv("ZERNIO_API_KEY")
        if not self.api_key:
            raise ValueError("ZERNIO_API_KEY must be provided either in constructor or as environment variable")
        
        # Default account IDs
        self.account_id_instagram = os.getenv("ZERNIO_ACCOUNT_ID")
        self.account_id_youtube = os.getenv("ZERNIO_ACCOUNT_ID_YOUTUBE")

    def _request(self, method, path, params=None):
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
            "Authorization": f"Bearer {self.api_key}"
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

    def get_account_health(self):
        """Get account health information."""
        if not self.account_id_instagram:
            raise ValueError("Instagram account ID not configured")
        return self._request("GET", f"/analytics/instagram/account-health/{self.account_id_instagram}")

    def get_account_insights(self):
        """Get account insights for Instagram."""
        if not self.account_id_instagram:
            raise ValueError("Instagram account ID not configured")
        return self._request("GET", f"/analytics/instagram/account-insights/{self.account_id_instagram}")

    def get_daily_metrics(self, start_date=None, end_date=None):
        """Get daily metrics for an account."""
        if not self.account_id_instagram:
            raise ValueError("Instagram account ID not configured")
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        return self._request("GET", f"/analytics/daily-metrics/{self.account_id_instagram}", params)

    def get_demographics(self):
        """Get demographic information."""
        if not self.account_id_instagram:
            raise ValueError("Instagram account ID not configured")
        return self._request("GET", f"/analytics/instagram/demographics/{self.account_id_instagram}")

    def get_follower_history(self, start_date=None, end_date=None):
        """Get follower history for an account."""
        if not self.account_id_instagram:
            raise ValueError("Instagram account ID not configured")
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        return self._request("GET", f"/analytics/instagram/follower-history/{self.account_id_instagram}", params)

    def get_best_time_to_post(self):
        """Get best time to post information."""
        if not self.account_id_instagram:
            raise ValueError("Instagram account ID not configured")
        return self._request("GET", f"/analytics/instagram/best-time-to-post/{self.account_id_instagram}")

    def get_posting_frequency(self):
        """Get posting frequency information."""
        if not self.account_id_instagram:
            raise ValueError("Instagram account ID not configured")
        return self._request("GET", f"/analytics/instagram/posting-frequency/{self.account_id_instagram}")

    def get_content_decay(self):
        """Get content decay information."""
        if not self.account_id_instagram:
            raise ValueError("Instagram account ID not configured")
        return self._request("GET", f"/analytics/instagram/content-decay/{self.account_id_instagram}")

    def list_inbox_comments(self, start_date=None, end_date=None):
        """List inbox comments."""
        if not self.account_id_instagram:
            raise ValueError("Instagram account ID not configured")
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        return self._request("GET", f"/inbox/comments/{self.account_id_instagram}", params)

    def list_conversations(self, start_date=None, end_date=None):
        """List conversations."""
        if not self.account_id_instagram:
            raise ValueError("Instagram account ID not configured")
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        return self._request("GET", f"/inbox/conversations/{self.account_id_instagram}", params)

    def get_conversation_messages(self, conversation_id, start_date=None, end_date=None):
        """Get messages from a specific conversation."""
        if not self.account_id_instagram:
            raise ValueError("Instagram account ID not configured")
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        return self._request("GET", f"/inbox/conversations/{self.account_id_instagram}/{conversation_id}/messages", params)

    def get_posts(self, start_date=None, end_date=None):
        """Get posts for an account."""
        if not self.account_id_instagram:
            raise ValueError("Instagram account ID not configured")
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        return self._request("GET", f"/analytics/instagram/posts/{self.account_id_instagram}", params)

    def get_comments(self, post_id=None, start_date=None, end_date=None):
        """Get comments for a specific post or all posts."""
        if not self.account_id_instagram:
            raise ValueError("Instagram account ID not configured")
        params = {}
        if post_id:
            params["post_id"] = post_id
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        return self._request("GET", f"/analytics/instagram/comments/{self.account_id_instagram}", params)

    def get_ideas(self, start_date=None, end_date=None):
        """Get ideas for an account."""
        if not self.account_id_instagram:
            raise ValueError("Instagram account ID not configured")
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        return self._request("GET", f"/ideas/{self.account_id_instagram}", params)

    def fetch_account_id(self, platform):
        """
        Fetch account ID for a specific platform.
        
        Args:
            platform: 'instagram' or 'youtube'
            
        Returns:
            Account ID string
        """
        # Get accounts list
        accounts_data = self._request("GET", "/accounts")
        
        # Find account by platform
        for account in accounts_data.get("accounts", []):
            if account.get("platform") == platform:
                return account.get("id")
        
        return None

    def validate_all_endpoints(self):
        """
        Validate all endpoints and report which ones work and which fail.
        
        Returns:
            Dictionary with endpoint validation results
        """
        print("Validating all Zernio endpoints...")
        print("=" * 50)
        
        # Test endpoints
        test_cases = [
            ("Account Health", lambda: self.get_account_health()),
            ("Daily Metrics", lambda: self.get_daily_metrics()),
            ("Demographics", lambda: self.get_demographics()),
            ("Follower History", lambda: self.get_follower_history()),
            ("Best Time to Post", lambda: self.get_best_time_to_post()),
            ("Posting Frequency", lambda: self.get_posting_frequency()),
            ("Content Decay", lambda: self.get_content_decay()),
            ("Inbox Comments", lambda: self.list_inbox_comments()),
            ("Inbox Conversations", lambda: self.list_conversations()),
        ]
        
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