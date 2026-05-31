import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

try:
    from src.api.client import ZernioClient
except ImportError as e:
    print(f"Error importing Zernio client: {e}")
    sys.exit(1)

async def generate_all_ideas_ig():
    """Generate all Instagram ideas"""
    # This would be implemented with actual Claude API calls
    return []

def generate_all_ideas_yt():
    """Generate all YouTube ideas"""
    # This would be implemented with actual Claude API calls
    return []

def discard_idea(idea_id, reason_quick, reason_text):
    """Discard an idea"""
    # This would be implemented with actual logic to store discarded ideas
    print(f"Discarding idea {idea_id} with reason: {reason_quick} - {reason_text}")
    return True

# For compatibility with app.py imports
generate_ideas = generate_all_ideas_ig