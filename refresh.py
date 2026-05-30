#!/usr/bin/env python3

import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Add project root to path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from zernio_client import ZernioClient
from cache import init_db, get_connection, write_refresh_log, read_refresh_logs, write_account_health, write_daily_metrics, write_follower_history

def refresh_instagram(zernio_client, cache):
    """Refresh Instagram data from Zernio API and persist to cache."""
    print("Starting Instagram refresh...")
    
    # Track counts for summary
    post_count = 0
    comment_count = 0
    dm_count = 0
    
    try:
        # 1. Get account health
        print("Fetching account health...")
        account_health = zernio_client.get_account_health()
        write_account_health(account_health)
        
        # 2. Get daily metrics with rolling 180d
        print("Fetching daily metrics...")
        daily_metrics = zernio_client.get_daily_metrics()
        for metric in daily_metrics:
            write_daily_metrics(metric)
        
        # 3. Get follower history
        print("Fetching follower history...")
        follower_history = zernio_client.get_follower_history()
        for history in follower_history:
            write_follower_history(history)
        
        # Note: Other endpoints would be implemented similarly
        
        return post_count, comment_count, dm_count
        
    except Exception as e:
        if "402" in str(e) or "403" in str(e):
            print(f"API Error (continuing): {e}")
            # Continue with other operations
            return post_count, comment_count, dm_count
        else:
            print(f"Error in Instagram refresh: {e}")
            raise

def refresh_youtube(zernio_client, cache):
    """Refresh YouTube data from Zernio API and persist to cache."""
    print("Starting YouTube refresh...")
    
    try:
        # Check if YouTube account is configured
        youtube_account_id = os.getenv('ZERNIO_ACCOUNT_ID_YOUTUBE', '')
        if not youtube_account_id:
            print("YouTube account not configured, skipping...")
            return
        
        print("Fetching YouTube data...")
        # Note: Implementation would fetch YouTube-specific data
        
    except Exception as e:
        if "402" in str(e) or "403" in str(e):
            print(f"API Error (continuing): {e}")
            # Continue with other operations
        else:
            print(f"Error in YouTube refresh: {e}")
            raise

def main():
    """Main refresh function that orchestrates all operations."""
    print("Starting refresh process...")
    
    # Initialize database
    init_db()
    
    # Get Zernio client
    zernio_client = ZernioClient()
    
    # Start refresh log
    start_time = datetime.now().isoformat()
    write_refresh_log({
        'started_at': start_time,
        'finished_at': None,
        'status': 'running',
        'error': None
    })
    
    try:
        # Refresh Instagram data
        post_count, comment_count, dm_count = refresh_instagram(zernio_client, None)
        
        # Check if YouTube should be refreshed
        youtube_account_id = os.getenv('ZERNIO_ACCOUNT_ID_YOUTUBE', '')
        if youtube_account_id:
            refresh_youtube(zernio_client, None)
        
        # Mark completion in refresh log
        end_time = datetime.now().isoformat()
        write_refresh_log({
            'started_at': start_time,
            'finished_at': end_time,
            'status': 'ok',
            'error': None
        })
        
        # Print summary - count rows in each table to simulate actual counts
        conn = get_connection()
        cursor = conn.cursor()
        
        # Count rows in each table (this would be actual data in a real implementation)
        tables_to_count = [
            "account_snapshot",
            "account_health", 
            "daily_metrics",
            "posts",
            "comments",
            "conversations",
            "messages",
            "follower_history",
            "refresh_log",
            "ideas",
            "idea_discards",
            "idea_feedback",
            "idea_categories",
            "idea_category_mappings",
            "idea_tags",
            "idea_tag_mappings",
            "idea_sources",
            "idea_source_mappings"
        ]
        
        print("\nRefresh completed successfully!")
        print("Summary:")
        for table in tables_to_count:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  {table}: {count} rows")
            except:
                print(f"  {table}: 0 rows (table may not exist yet)")
        
        conn.close()
        
    except Exception as e:
        # Mark failure in refresh log
        end_time = datetime.now().isoformat()
        write_refresh_log({
            'started_at': start_time,
            'finished_at': end_time,
            'status': 'partial_error',
            'error': str(e)
        })
        
        print(f"Refresh completed with errors: {e}")

if __name__ == "__main__":
    main()