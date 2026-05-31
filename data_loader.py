#!/usr/bin/env python3

import sqlite3
import os
import pandas as pd
from datetime import datetime
from cache import get_connection

def load_account_data_from_db():
    """Load account data from SQLite database."""
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Load account snapshot data
    cursor.execute('''
        SELECT id, platform, username, follower_count, profile_pic_url, updated_at 
        FROM account_snapshot 
        ORDER BY updated_at DESC 
        LIMIT 1
    ''')
    account_snapshot_row = cursor.fetchone()
    
    if account_snapshot_row:
        account_snapshot = {
            "id": account_snapshot_row[0],
            "platform": account_snapshot_row[1],
            "username": account_snapshot_row[2],
            "follower_count": account_snapshot_row[3],
            "profile_image": account_snapshot_row[4],
            "updated_at": account_snapshot_row[5]
        }
    else:
        # Fallback to mock data if no real data
        account_snapshot = {
            "id": "mock_id",
            "platform": "instagram",
            "username": "test_user",
            "follower_count": 12500,
            "profile_image": "https://via.placeholder.com/100",
            "updated_at": datetime.now().isoformat()
        }
    
    # Load account health data
    cursor.execute('''
        SELECT id, platform, status, checked_at 
        FROM account_health 
        ORDER BY checked_at DESC 
        LIMIT 1
    ''')
    account_health_row = cursor.fetchone()
    
    if account_health_row:
        account_health = {
            "status": account_health_row[2]
        }
    else:
        account_health = {"status": "unknown"}
    
    # Load daily metrics data (last 5 days)
    cursor.execute('''
        SELECT date, platform, reach, views, engagements, likes, comments_count, saves, shares, 
               impressions, profile_visits, website_clicks, video_views, story_taps_forward, 
               story_taps_back, story_exits, story_replies
        FROM daily_metrics 
        WHERE platform = 'instagram'
        ORDER BY date DESC 
        LIMIT 5
    ''')
    daily_metrics_rows = cursor.fetchall()
    
    if daily_metrics_rows:
        daily_metrics = {
            "date": [row[0] for row in daily_metrics_rows],
            "reach": [row[2] for row in daily_metrics_rows],
            "views": [row[3] for row in daily_metrics_rows],
            "engaged": [row[4] for row in daily_metrics_rows],
            "interactions": [row[5] for row in daily_metrics_rows]
        }
    else:
        # Fallback to mock data
        daily_metrics = {
            "date": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05"],
            "reach": [1000, 1200, 950, 1100, 1300],
            "views": [500, 600, 480, 550, 700],
            "engaged": [200, 250, 180, 220, 300],
            "interactions": [50, 60, 45, 55, 70]
        }
    
    # Load follower history data (last 5 days)
    cursor.execute('''
        SELECT date, platform, followers
        FROM follower_history 
        WHERE platform = 'instagram'
        ORDER BY date DESC 
        LIMIT 5
    ''')
    follower_history_rows = cursor.fetchall()
    
    if follower_history_rows:
        follower_history = {
            "date": [row[0] for row in follower_history_rows],
            "followers": [row[2] for row in follower_history_rows]
        }
    else:
        # Fallback to mock data
        follower_history = {
            "date": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05"],
            "followers": [12000, 12100, 12050, 12200, 12300]
        }
    
    # Load posts data (last 6 posts)
    cursor.execute('''
        SELECT id, platform, caption, permalink, thumbnail_url, likes, comments_count, saves, shares, reach, timestamp
        FROM posts 
        WHERE platform = 'instagram'
        ORDER BY timestamp DESC 
        LIMIT 6
    ''')
    posts_rows = cursor.fetchall()
    
    if posts_rows:
        posts = []
        for row in posts_rows:
            post = {
                "id": row[0],
                "platform": row[1],
                "caption": row[2],
                "permalink": row[3],
                "image_url": row[4],
                "likes": row[5],
                "comments_count": row[6],
                "saves": row[7],
                "shares": row[8],
                "reach": row[9],
                "timestamp": row[10]
            }
            posts.append(post)
    else:
        # Fallback to mock data
        posts = [
            {"id": 1, "image_url": "https://via.placeholder.com/300", "caption": "Post 1"},
            {"id": 2, "image_url": "https://via.placeholder.com/300", "caption": "Post 2"},
            {"id": 3, "image_url": "https://via.placeholder.com/300", "caption": "Post 3"},
            {"id": 4, "image_url": "https://via.placeholder.com/300", "caption": "Post 4"},
            {"id": 5, "image_url": "https://via.placeholder.com/300", "caption": "Post 5"},
            {"id": 6, "image_url": "https://via.placeholder.com/300", "caption": "Post 6"}
        ]
    
    # Load comments data (last 3 comments)
    cursor.execute('''
        SELECT id, post_id, platform, text, username, timestamp
        FROM comments 
        WHERE platform = 'instagram'
        ORDER BY timestamp DESC 
        LIMIT 3
    ''')
    comments_rows = cursor.fetchall()
    
    if comments_rows:
        comments = []
        for row in comments_rows:
            comment = {
                "id": row[0],
                "post_id": row[1],
                "platform": row[2],
                "text": row[3],
                "author": row[4],
                "timestamp": row[5]
            }
            comments.append(comment)
    else:
        # Fallback to mock data
        comments = [
            {"id": 1, "text": "¡Excelente contenido!", "author": "user1", "timestamp": "2023-01-01"},
            {"id": 2, "text": "Me encanta este post", "author": "user2", "timestamp": "2023-01-01"},
            {"id": 3, "text": "te amo eres mi ídola", "author": "user3", "timestamp": "2023-01-01"}
        ]
    
    # Load audience data (mocked for now)
    audience_ig = {
        "age": [25, 35, 45, 55],
        "count": [3000, 4500, 2800, 1200]
    }
    
    audience_yt = {
        "age": [25, 35, 45, 55],
        "count": [3000, 4500, 2800, 1200]
    }
    
    # Load best time data (mocked for now)
    best_time = {
        "hour": [9, 10, 11, 12, 13, 14],
        "day_of_week": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        "value": [85, 75, 90, 65, 80, 95]
    }
    
    # Load content decay data (mocked for now)
    content_decay = {
        "days": [1, 7, 14, 21, 30],
        "engagement": [100, 75, 60, 45, 30]
    }
    
    # Load account insights (last 30 days)
    cursor.execute('''
        SELECT date, platform, reach, views, engagements, likes, comments_count, saves, shares, 
               impressions, profile_visits, website_clicks, video_views, story_taps_forward, 
               story_taps_back, story_exits, story_replies
        FROM daily_metrics 
        WHERE platform = 'instagram'
        ORDER BY date DESC 
        LIMIT 30
    ''')
    insights_rows = cursor.fetchall()
    
    if insights_rows:
        # Calculate aggregated metrics for last 30 days
        reach_sum = sum(row[2] for row in insights_rows)
        views_sum = sum(row[3] for row in insights_rows)
        engaged_sum = sum(row[4] for row in insights_rows)
        interactions_sum = sum(row[5] for row in insights_rows)
        likes_sum = sum(row[6] for row in insights_rows)
        comments_sum = sum(row[7] for row in insights_rows)
        saves_sum = sum(row[8] for row in insights_rows)
        shares_sum = sum(row[9] for row in insights_rows)
        
        account_insights_30d = {
            "reach": reach_sum,
            "views": views_sum,
            "engaged": engaged_sum,
            "interactions": interactions_sum,
            "likes": likes_sum,
            "comments": comments_sum,
            "saves": saves_sum,
            "shares": shares_sum
        }
    else:
        # Fallback to mock data
        account_insights_30d = {
            "reach": 45000,
            "views": 22000,
            "engaged": 3800,
            "interactions": 1200,
            "likes": 950,
            "comments": 180,
            "saves": 75,
            "shares": 45
        }
    
    conn.close()
    
    return {
        "account_snapshot": {
            "username": account_snapshot["username"],
            "profile_image": account_snapshot["profile_image"],
            "follower_count": account_snapshot["follower_count"],
            "account_health": account_health
        },
        "account_insights_30d": account_insights_30d,
        "daily_metrics": daily_metrics,
        "follower_history": follower_history,
        "audience_ig": audience_ig,
        "audience_yt": audience_yt,
        "posts": posts,
        "comments": comments,
        "best_time": best_time,
        "content_decay": content_decay
    }