#!/usr/bin/env python3

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Import the Zernio client
try:
    from src.api.client import ZernioClient, AddonRequiredError, AuthError
except ImportError as e:
    print(f"Error importing Zernio client: {e}")
    sys.exit(1)

def load_account_data_from_zernio_with_fallback():
    """Load account data from Zernio API using the official client with fallback to mock data."""
    
    try:
        # Initialize the Zernio client
        client = ZernioClient()
        
        # Get account information
        accounts_result = client.list_accounts()
        if not accounts_result or 'accounts' not in accounts_result:
            print("No accounts found")
            return None
            
        # Find Instagram account
        instagram_account = None
        for account in accounts_result['accounts']:
            if account['platform'] == 'instagram':
                instagram_account = account
                break
                
        if not instagram_account:
            print("No Instagram account found")
            return None
            
        account_id = instagram_account['_id']
        
        # Load account health (this is what we use for account snapshot)
        # Use the correct Instagram account insights endpoint
        try:
            health_result = client.get_instagram_account_insights(account_id)
        except AddonRequiredError as e:
            print(f"Addon required for health data: {e}")
            health_result = {}
        except Exception as e:
            print(f"Error getting account health: {e}")
            health_result = {}
            
        # Load daily analytics (this is what we use for daily metrics)
        try:
            daily_result = client.get_daily_metrics(account_id)
        except AddonRequiredError as e:
            print(f"Addon required for daily analytics: {e}")
            daily_result = {"metrics": []}
        except Exception as e:
            print(f"Error getting daily analytics: {e}")
            daily_result = {"metrics": []}
            
        # Load follower stats (this is what we use for follower history)
        try:
            follower_result = client.get_follower_stats(account_id)
        except AddonRequiredError as e:
            print(f"Addon required for follower stats: {e}")
            follower_result = {"history": []}
        except Exception as e:
            print(f"Error getting follower stats: {e}")
            follower_result = {"history": []}
            
        # Load best time to post
        try:
            best_time_result = client.get_best_time_to_post(account_id)
        except AddonRequiredError as e:
            print(f"Addon required for best time data: {e}")
            best_time_result = {"best_time": []}
        except Exception as e:
            print(f"Error getting best time data: {e}")
            best_time_result = {"best_time": []}
            
        # Load comments (this is what we use for comments)
        try:
            comments_result = client.list_inbox_comments(account_id)
        except AddonRequiredError as e:
            print(f"Addon required for comments: {e}")
            comments_result = {"comments": []}
        except Exception as e:
            print(f"Error getting comments: {e}")
            comments_result = {"comments": []}
            
        # Load posts (this is what we use for posts)
        try:
            posts_result = client.get_analytics(account_id)
        except AddonRequiredError as e:
            print(f"Addon required for posts: {e}")
            posts_result = {"posts": []}
        except Exception as e:
            print(f"Error getting posts: {e}")
            posts_result = {"posts": []}
            
        # Prepare the data structure to match what app.py expects
        # Handle case where account insights are not available due to missing add-ons
        if isinstance(health_result, dict) and 'error' in health_result:
            # If we got an error from the API (like addon required), create mock data
            account_health_data = {
                "id": account_id,
                "platform": instagram_account['platform'],
                "status": "unknown",
                "checked_at": datetime.now().isoformat(),
                "message": "Datos de salud no disponibles (requiere Analytics add-on)"
            }
        else:
            # Use actual data from API
            account_health_data = {
                "id": account_id,
                "platform": instagram_account['platform'],
                "status": health_result.get('health_status', 'unknown'),
                "checked_at": datetime.now().isoformat()
            }
            
        return {
            'account_snapshot': {
                "id": account_id,
                "platform": instagram_account['platform'],
                "username": instagram_account.get('username', ''),
                "follower_count": health_result.get('followers', 0),
                "profile_image": health_result.get('profile_pic_url', ''),
                "updated_at": datetime.now().isoformat()
            },
            'account_health': account_health_data,
            'daily_metrics': daily_result.get('metrics', []),
            'posts': posts_result.get('posts', []),
            'comments': comments_result.get('comments', []),
            'follower_history': follower_result.get('history', []),
            'best_time_to_post': best_time_result.get('best_time', [])
        }
        
    except AuthError as e:
        print(f"Authentication error: {e}")
        return None
    except Exception as e:
        print(f"Error loading data from Zernio: {e}")
        import traceback
        traceback.print_exc()
        return None

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