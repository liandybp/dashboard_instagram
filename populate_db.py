#!/usr/bin/env python3

import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Add project root to path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import cache module to get DB_PATH
from cache import init_db, write_account_snapshot, write_account_health, write_daily_metrics, write_follower_history, write_posts, write_comments, DB_PATH

# Ensure the database file exists in the correct location
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def populate_test_data():
    """Populate database with test data."""
    
    # Initialize database
    init_db()
    
    print("Populating test data...")
    
    # 1. Account snapshot data
    account_snapshot = {
        "id": "test_account_123",
        "platform": "instagram",
        "username": "test_user",
        "follower_count": 12500,
        "profile_pic_url": "https://via.placeholder.com/100",
        "updated_at": datetime.now().isoformat()
    }
    write_account_snapshot(account_snapshot)
    
    # 2. Account health data
    account_health = {
        "id": "test_account_123",
        "platform": "instagram",
        "status": "healthy",
        "checked_at": datetime.now().isoformat()
    }
    write_account_health(account_health)
    
    # 3. Daily metrics data (last 5 days)
    for i in range(5):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        daily_metrics = {
            "date": date,
            "platform": "instagram",
            "reach": 1000 + i * 200,
            "views": 500 + i * 100,
            "engagements": 200 + i * 50,
            "likes": 50 + i * 10,
            "comments_count": 10 + i * 2,
            "saves": 5 + i,
            "shares": 3 + i,
            "impressions": 1500 + i * 300,
            "profile_visits": 100 + i * 20,
            "website_clicks": 20 + i * 5,
            "video_views": 100 + i * 20,
            "story_taps_forward": 50 + i * 10,
            "story_taps_back": 30 + i * 5,
            "story_exits": 20 + i * 3,
            "story_replies": 10 + i
        }
        write_daily_metrics(daily_metrics)
    
    # 4. Follower history data (last 5 days)
    for i in range(5):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        follower_history = {
            "date": date,
            "platform": "instagram",
            "followers": 12000 + i * 100
        }
        write_follower_history(follower_history)
    
    # 5. Posts data (6 posts)
    posts_data = []
    for i in range(6):
        post = {
            "id": f"post_{i+1}",
            "platform": "instagram",
            "caption": f"Post {i+1} - This is a sample caption for testing purposes",
            "permalink": f"https://instagram.com/p/post_{i+1}",
            "image_url": f"https://via.placeholder.com/300?text=Post+{i+1}",
            "likes": 100 + i * 20,
            "comments_count": 10 + i,
            "saves": 5 + i,
            "shares": 3 + i,
            "reach": 500 + i * 100,
            "timestamp": (datetime.now() - timedelta(days=i*2)).isoformat()
        }
        posts_data.append(post)
    
    write_posts(posts_data)
    
    # 6. Comments data (3 comments)
    comments_data = []
    for i in range(3):
        comment = {
            "id": f"comment_{i+1}",
            "post_id": f"post_{i+1}",
            "platform": "instagram",
            "text": f"This is a sample comment {i+1} from user {i+1}",
            "username": f"user_{i+1}",
            "timestamp": (datetime.now() - timedelta(days=i)).isoformat()
        }
        comments_data.append(comment)
    
    write_comments(comments_data)
    
    print("Test data populated successfully!")

if __name__ == "__main__":
    populate_test_data()