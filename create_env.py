#!/usr/bin/env python3

import os
import sys
from zernio_client import fetch_account_id

def main():
    # Get credentials from environment variables
    zernio_api_key = os.getenv('ZERNIO_API_KEY')
    anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
    timezone = os.getenv('DASHBOARD_TZ')
    has_youtube = os.getenv('HAS_YOUTUBE', 'no').lower() == 'yes'
    
    if not all([zernio_api_key, anthropic_api_key, timezone]):
        print("Error: Please set ZERNIO_API_KEY, ANTHROPIC_API_KEY, and DASHBOARD_TZ environment variables")
        sys.exit(1)
    
    try:
        # Fetch Instagram account ID
        instagram_account_id = fetch_account_id(zernio_api_key, 'instagram')
        
        # Fetch YouTube account ID if applicable
        youtube_account_id = ''
        if has_youtube:
            youtube_account_id = fetch_account_id(zernio_api_key, 'youtube')
        
        # Create .env file content
        env_content = f"""ZERNIO_API_KEY={zernio_api_key}
ZERNIO_ACCOUNT_ID={instagram_account_id}
ZERNIO_ACCOUNT_ID_YOUTUBE={youtube_account_id}
ANTHROPIC_API_KEY={anthropic_api_key}
DASHBOARD_TZ={timezone}
"""
        
        # Write to .env file
        with open('.env', 'w') as f:
            f.write(env_content)
            
        print("Successfully created .env file")
        print("Contents:")
        print(env_content)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()