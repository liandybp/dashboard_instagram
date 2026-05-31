#!/usr/bin/env python3

import sqlite3
import os
import json
from datetime import datetime, timedelta

# Ensure data directory exists
data_dir = "data.nosync"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Database file path
DB_PATH = os.path.join(data_dir, "cache.db")

def init_db():
    """Initialize the database with all required tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create meta table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meta (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    
    # Create account_snapshot table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS account_snapshot (
            id TEXT,
            platform TEXT,
            username TEXT,
            follower_count INTEGER,
            profile_pic_url TEXT,
            updated_at TEXT,
            PRIMARY KEY (id, platform)
        )
    ''')
    
    # Create account_health table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS account_health (
            id TEXT,
            platform TEXT,
            status TEXT,
            checked_at TEXT,
            token_valid INTEGER,
            is_active INTEGER,
            is_verified INTEGER,
            is_restricted INTEGER,
            scopes_ok INTEGER,
            missing_scopes TEXT,
            issues TEXT,
            recommendations TEXT,
            PRIMARY KEY (id, platform)
        )
    ''')
    
    # Ensure all columns exist (migration for existing tables)
    migrate_column('account_health', 'token_valid', 'INTEGER')
    migrate_column('account_health', 'is_active', 'INTEGER')
    migrate_column('account_health', 'is_verified', 'INTEGER')
    migrate_column('account_health', 'is_restricted', 'INTEGER')
    migrate_column('account_health', 'scopes_ok', 'INTEGER')
    migrate_column('account_health', 'missing_scopes', 'TEXT')
    migrate_column('account_health', 'issues', 'TEXT')
    migrate_column('account_health', 'recommendations', 'TEXT')
    
    # Create daily_metrics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_metrics (
            date TEXT,
            platform TEXT,
            reach INTEGER,
            views INTEGER,
            engagements INTEGER,
            likes INTEGER,
            comments_count INTEGER,
            saves INTEGER,
            shares INTEGER,
            impressions INTEGER,
            profile_visits INTEGER,
            website_clicks INTEGER,
            video_views INTEGER,
            story_taps_forward INTEGER,
            story_taps_back INTEGER,
            story_exits INTEGER,
            story_replies INTEGER,
            PRIMARY KEY (date, platform)
        )
    ''')
    
    # Create posts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY,
            platform TEXT,
            caption TEXT,
            permalink TEXT,
            thumbnail_url TEXT,
            likes INTEGER,
            comments_count INTEGER,
            saves INTEGER,
            shares INTEGER,
            reach INTEGER,
            timestamp TEXT
        )
    ''')
    
    # Create comments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id TEXT PRIMARY KEY,
            post_id TEXT,
            platform TEXT,
            text TEXT,
            username TEXT,
            timestamp TEXT
        )
    ''')
    
    # Create conversations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            account_id TEXT,
            last_message_at TEXT
        )
    ''')
    
    # Create messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            conversation_id TEXT,
            text TEXT,
            from_user TEXT,
            timestamp TEXT
        )
    ''')
    
    # Create follower_history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS follower_history (
            date TEXT,
            platform TEXT,
            followers INTEGER,
            followers_gained INTEGER DEFAULT 0,
            followers_lost INTEGER DEFAULT 0,
            PRIMARY KEY (date, platform)
        )
    ''')
    
    # Create refresh_log table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS refresh_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            started_at TEXT,
            finished_at TEXT,
            status TEXT,
            error TEXT
        )
    ''')
    
    # Create ideas table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ideas (
            id TEXT PRIMARY KEY,
            platform TEXT,
            content TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    ''')
    
    # Create idea_discards table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS idea_discards (
            id TEXT PRIMARY KEY,
            platform TEXT,
            reason TEXT,
            discarded_at TEXT
        )
    ''')
    
    # Create idea_feedback table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS idea_feedback (
            id TEXT PRIMARY KEY,
            idea_id TEXT,
            feedback_type TEXT,
            feedback_text TEXT,
            created_at TEXT
        )
    ''')
    
    # Create idea_categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS idea_categories (
            id TEXT PRIMARY KEY,
            name TEXT,
            description TEXT,
            created_at TEXT
        )
    ''')
    
    # Create idea_category_mappings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS idea_category_mappings (
            idea_id TEXT,
            category_id TEXT,
            PRIMARY KEY (idea_id, category_id)
        )
    ''')
    
    # Create idea_tags table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS idea_tags (
            id TEXT PRIMARY KEY,
            name TEXT,
            created_at TEXT
        )
    ''')
    
    # Create idea_tag_mappings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS idea_tag_mappings (
            idea_id TEXT,
            tag_id TEXT,
            PRIMARY KEY (idea_id, tag_id)
        )
    ''')
    
    # Create idea_sources table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS idea_sources (
            id TEXT PRIMARY KEY,
            name TEXT,
            description TEXT,
            created_at TEXT
        )
    ''')
    
    # Create idea_source_mappings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS idea_source_mappings (
            idea_id TEXT,
            source_id TEXT,
            PRIMARY KEY (idea_id, source_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def migrate_column(table_name, column_name, column_type):
    """Migrate a column to a table if it doesn't exist."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if column exists
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        # Extract column names from the result
        existing_columns = [col[1] for col in columns]
        
        # Only add column if it doesn't exist
        if column_name not in existing_columns:
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
            
        conn.commit()
    except Exception as e:
        print(f"Error en migración de columna {column_name}: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def backup_data(table_name):
    """Backup data from a table before massive delete operations."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all data from the table
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    
    # Get column names
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]
    
    # Create backup file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(data_dir, f"backup_{timestamp}_{table_name}.json")
    
    # Convert data to JSON format
    backup_data = [dict(zip(columns, row)) for row in rows]
    
    with open(backup_file, 'w') as f:
        json.dump(backup_data, f, indent=2)
    
    conn.close()
    return backup_file

def get_connection():
    """Get a database connection."""
    return sqlite3.connect(DB_PATH)

# Writers and readers for each table
def write_meta(key, value):
    """Write metadata to the meta table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO meta (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def read_meta(key):
    """Read metadata from the meta table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM meta WHERE key = ?", (key,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def write_account_snapshot(account_data):
    """Write account snapshot data."""
    conn = get_connection()
    cursor = conn.cursor()
    if isinstance(account_data, list):
        # Handle list of account data
        for data in account_data:
            cursor.execute('''
                INSERT OR REPLACE INTO account_snapshot 
                (id, platform, username, follower_count, profile_pic_url, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                data['id'],
                data['platform'],
                data['username'],
                data['follower_count'],
                data['profile_pic_url'],
                data['updated_at']
            ))
    else:
        # Handle single account data
        cursor.execute('''
            INSERT OR REPLACE INTO account_snapshot 
            (id, platform, username, follower_count, profile_pic_url, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            account_data['id'],
            account_data['platform'],
            account_data['username'],
            account_data['follower_count'],
            account_data['profile_pic_url'],
            account_data['updated_at']
        ))
    conn.commit()
    conn.close()

def read_account_snapshot(account_id, platform):
    """Read account snapshot data."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM account_snapshot 
        WHERE id = ? AND platform = ?
    ''', (account_id, platform))
    result = cursor.fetchone()
    conn.close()
    return result

def write_account_health(account_data):
    """Write account health data."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO account_health 
        (id, platform, status, checked_at,
         token_valid, is_active, is_verified, is_restricted, scopes_ok,
         missing_scopes, issues, recommendations)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        account_data['id'],
        account_data['platform'],
        account_data['status'],
        account_data['checked_at'],
        int(account_data.get('tokenValid', False)),
        int(account_data.get('isActive', False)),
        int(account_data.get('isVerified', False)),
        int(account_data.get('isRestricted', False)),
        int(account_data.get('scopesOk', True)),
        json.dumps(account_data.get('missingScopes', [])),
        json.dumps(account_data.get('issues', [])),
        json.dumps(account_data.get('recommendations', [])),
    ))
    conn.commit()
    conn.close()

def read_account_health(account_id, platform):
    """Read account health data."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM account_health 
        WHERE id = ? AND platform = ?
        ORDER BY checked_at DESC
        LIMIT 1
    ''', (account_id, platform))
    result = cursor.fetchone()
    conn.close()
    return result

def read_account_health_dict(account_id, platform):
    """Read account health data as dictionary."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM account_health 
        WHERE id = ? AND platform = ?
        ORDER BY checked_at DESC
        LIMIT 1
    ''', (account_id, platform))
    row = cursor.fetchone()
    conn.close()
    if row:
        # Convert to dictionary with column names as keys
        columns = [description[0] for description in cursor.description]
        return dict(zip(columns, row))
    return None

def write_daily_metrics(metrics_data):
    """Write daily metrics data."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO daily_metrics 
        (date, platform, reach, views, engagements, likes, comments_count, saves, shares, impressions,
         profile_visits, website_clicks, video_views, story_taps_forward, story_taps_back,
         story_exits, story_replies)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        metrics_data['date'],
        metrics_data['platform'],
        metrics_data['reach'],
        metrics_data['views'],
        metrics_data['engagements'],
        metrics_data['likes'],
        metrics_data['comments_count'],
        metrics_data['saves'],
        metrics_data['shares'],
        metrics_data['impressions'],
        metrics_data['profile_visits'],
        metrics_data['website_clicks'],
        metrics_data['video_views'],
        metrics_data['story_taps_forward'],
        metrics_data['story_taps_back'],
        metrics_data['story_exits'],
        metrics_data['story_replies']
    ))
    conn.commit()
    conn.close()

def read_daily_metrics(date, platform):
    """Read daily metrics data."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM daily_metrics 
        WHERE date = ? AND platform = ?
    ''', (date, platform))
    result = cursor.fetchone()
    conn.close()
    return result

def write_posts(posts_data):
    """Write posts data."""
    conn = get_connection()
    cursor = conn.cursor()
    for post in posts_data:
        cursor.execute('''
            INSERT OR REPLACE INTO posts 
            (id, platform, caption, permalink, thumbnail_url, likes, comments_count,
             saves, shares, reach, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            post['id'],
            post['platform'],
            post['caption'],
            post['permalink'],
            post['image_url'],
            post['likes'],
            post['comments_count'],
            post['saves'],
            post['shares'],
            post['reach'],
            post['timestamp']
        ))
    conn.commit()
    conn.close()

def read_posts(post_id):
    """Read posts data."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts WHERE id = ?', (post_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def write_comments(comments_data):
    """Write comments data."""
    conn = get_connection()
    cursor = conn.cursor()
    for comment in comments_data:
        cursor.execute('''
            INSERT OR REPLACE INTO comments 
            (id, post_id, platform, text, username, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            comment['id'],
            comment['post_id'],
            comment['platform'],
            comment['text'],
            comment['username'],
            comment['timestamp']
        ))
    conn.commit()
    conn.close()

def read_comments(post_id):
    """Read comments data for a specific post."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comments WHERE post_id = ?', (post_id,))
    result = cursor.fetchall()
    conn.close()
    return result

def write_conversations(conversations_data):
    """Write conversations data."""
    conn = get_connection()
    cursor = conn.cursor()
    for conversation in conversations_data:
        cursor.execute('''
            INSERT OR REPLACE INTO conversations 
            (id, account_id, last_message_at)
            VALUES (?, ?, ?)
        ''', (
            conversation['id'],
            conversation['account_id'],
            conversation['last_message_at']
        ))
    conn.commit()
    conn.close()

def read_conversations(account_id):
    """Read conversations for a specific account."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM conversations WHERE account_id = ?', (account_id,))
    result = cursor.fetchall()
    conn.close()
    return result

def write_messages(messages_data):
    """Write messages data."""
    conn = get_connection()
    cursor = conn.cursor()
    for message in messages_data:
        cursor.execute('''
            INSERT OR REPLACE INTO messages 
            (id, conversation_id, text, from_user, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            message['id'],
            message['conversation_id'],
            message['text'],
            message['from_user'],
            message['timestamp']
        ))
    conn.commit()
    conn.close()

def read_messages(conversation_id):
    """Read messages for a specific conversation."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM messages WHERE conversation_id = ?', (conversation_id,))
    result = cursor.fetchall()
    conn.close()
    return result

def write_follower_history(follower_data):
    """Write follower history data."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO follower_history 
        (date, platform, followers, followers_gained, followers_lost)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        follower_data['date'],
        follower_data['platform'],
        follower_data['followers'],
        follower_data.get('followers_gained', 0),
        follower_data.get('followers_lost', 0)
    ))
    conn.commit()
    conn.close()

def read_follower_history(date, platform):
    """Read follower history data."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM follower_history 
        WHERE date = ? AND platform = ?
    ''', (date, platform))
    result = cursor.fetchone()
    conn.close()
    return result

def read_follower_history_list(platform, days=90):
    """
    Devuelve serie temporal de seguidores con dinámica diaria.
    Ordenado cronológicamente, últimos N días.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Calculate cutoff date
    from datetime import datetime, timedelta
    cutoff = (datetime.utcnow() - timedelta(days=days)).date().isoformat()
    
    cursor.execute('''
        SELECT date, followers, followers_gained, followers_lost
        FROM follower_history
        WHERE platform = ? AND date >= ?
        ORDER BY date ASC
    ''', (platform, cutoff))
    
    rows = cursor.fetchall()
    conn.close()
    
    # Convert to list of dictionaries
    return [dict(zip(['date', 'followers', 'followers_gained', 'followers_lost'], row)) for row in rows]

def write_refresh_log(log_data):
    """Write refresh log data."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO refresh_log 
        (started_at, finished_at, status, error)
        VALUES (?, ?, ?, ?)
    ''', (
        log_data['started_at'],
        log_data['finished_at'],
        log_data['status'],
        log_data['error']
    ))
    conn.commit()
    conn.close()

def read_refresh_logs():
    """Read refresh logs."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM refresh_log ORDER BY started_at DESC')
    result = cursor.fetchall()
    conn.close()
    return result

def write_ideas(ideas_data):
    """Write ideas data (accumulative)."""
    conn = get_connection()
    cursor = conn.cursor()
    for idea in ideas_data:
        cursor.execute('''
            INSERT OR REPLACE INTO ideas 
            (id, platform, content, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            idea['id'],
            idea['platform'],
            idea['content'],
            idea['created_at'],
            idea['updated_at']
        ))
    conn.commit()
    conn.close()

def read_ideas():
    """Read all ideas."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ideas')
    result = cursor.fetchall()
    conn.close()
    return result

def write_idea_discards(discard_data):
    """Write idea discard data (accumulative)."""
    conn = get_connection()
    cursor = conn.cursor()
    for discard in discard_data:
        cursor.execute('''
            INSERT OR REPLACE INTO idea_discards 
            (id, platform, reason, discarded_at)
            VALUES (?, ?, ?, ?)
        ''', (
            discard['id'],
            discard['platform'],
            discard['reason'],
            discard['discarded_at']
        ))
    conn.commit()
    conn.close()

def read_idea_discards():
    """Read all idea discards."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM idea_discards')
    result = cursor.fetchall()
    conn.close()
    return result

# Execute init_db twice to test idempotency
if __name__ == "__main__":
    print("Initializing database for the first time...")
    init_db()
    print("First initialization complete.")
    
    print("Initializing database for the second time (testing idempotency)...")
    init_db()
    print("Second initialization complete. No errors occurred.")