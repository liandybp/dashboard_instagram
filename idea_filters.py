# Patrones para ADORATION_PATTERNS - more comprehensive list with word boundaries to avoid false positives
# Note: These patterns are intentionally kept broad but with word boundaries to catch clear adoration
ADORATION_PATTERNS = [
    r"\b(amazing|beautiful|gorgeous|incredible|inspiring|love|lovely|marvelous|phenomenal|perfect|stunning|wonderful|excellent|fantastic|great|superb|brilliant|outstanding)\b",
    r"\b(adoro|amo|me encanta|me gusta|genial|fantástico|maravilloso|perfecto|excelente)\b",
]

# Patrones para BOT_PATTERNS - more comprehensive list
BOT_PATTERNS = [
    r"follow me",
    r"follow back",
    r"follow for follow",
    r"follow for follows",
    r"followers",
    r"following",
    r"like for like",
    r"like for likes",
    r"likes",
    r"love for love",
    r"love for loves",
    r"loves",
    r"comment for comment",
    r"comment for comments",
    r"comments",
    r"tag a friend",
    r"tag someone",
    r"tagging",
    r"tagged",
    r"share this post",
    r"share it",
    r"share with friends",
    r"share with others",
    r"share this",
    r"share the love",
    r"tag your friend",
    r"tag your friends",
    r"comment below",
    r"comment here",
    r"leave a comment",
    r"leave a comment below",
    r"comment on this post",
    r"comment on this",
    r"click the link",
    r"link in bio",
    r"link in description",
    r"bio link",
    r"link to my profile",
    r"follow me on",
    r"check out my",
    r"check out our",
    r"check out their",
    r"check out this",
    r"click here",
    r"click now",
    r"get it now",
    r"limited time offer",
    r"deal of the day",
    r"flash sale",
    r"sale ends soon",
    r"offer expires soon",
    r"special discount",
    r"discount code",
    r"coupon code",
    r"use code",
    r"promo code",
    r"free shipping",
    r"freebie",
    r"free gift",
    r"limited time",
    r"exclusive offer",
    r"secret deal",
    r"special offer",
    r"hot deal",
    r"best deal",
    r"top deal",
    r"limited edition",
    r"exclusive access",
    r"early access",
    r"preview",
    r"preorder",
    r"new collection",
    r"new release",
    r"new product",
    r"new feature",
    r"new update",
    r"coming soon",
    r"launching soon",
    r"soon available",
    r"available now",
    r"now available",
    r"exclusive",
    r"limited",
    r"special",
    r"promo",
    r"offer",
    r"deal",
    r"discount",
    r"sale",
    r"free",
    r"gift",
    r"code",
    r"link",
    r"click",
    r"share",
    r"follow",
    r"like",
    r"comment",
    r"tag",
    r"bio",
    r"profile",
    r"post",
    r"story",
    r"reel",
    r"video",
    r"photo",
    r"picture",
    r"image",
    r"update",
    r"news",
    r"announcement",
    r"release",
    r"launch",
    r"event",
    r"contest",
    r"giveaway",
    r"winner",
    r"prize",
    r"award",
    r"recognition",
    r"celebration",
    r"thanks",
    r"thank you",
    r"appreciation",
    r"gratitude",
    r"support",
    r"community",
    r"followers",
    r"following",
    r"fans",
    r"lovers",
    r"enjoy",
    r"enjoying",
    r"love it",
    r"love this",
    r"love that",
    r"love these",
    r"love those",
    r"love this post",
    r"love that post",
    r"love these posts",
    r"love those posts",
    r"love it so much",
    r"love this so much",
    r"love that so much",
    r"love these so much",
    r"love those so much"
]

import re

def is_substantive_comment(comment_text):
    """
    Determines if a comment is substantive (not a bot or adoration).
    """
    # Convert to lowercase for case-insensitive matching
    text = comment_text.lower()
    
    # Check for very short or emoji-only comments that are likely spam/bots
    # Remove all non-alphabetic characters and check if it's mostly emojis
    emoji_only = re.sub(r'[^\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]', '', text)
    letter_only = re.sub(r'[^a-zA-Záéíóúñü]', '', text)
    
    # If more than 70% of the characters are emojis, filter it out
    if len(text) > 0 and len(emoji_only) / len(text) > 0.7:
        return False
    
    # Check for repeating character patterns (e.g., 'jjjj', 'aaaa')
    # Look for 4 or more consecutive identical characters
    if re.search(r'(.)\1{3,}', text):
        return False
    
    # Special case: check for alternating character patterns that are spam-like
    # Like jajajaja where there's a repeating pattern of 2 chars that repeats 4 times
    if len(text) >= 8:
        # Check if the pattern repeats (e.g., 'jajajaja' = 'ja' repeated 4 times)
        for pattern_len in range(1, min(len(text)//2 + 1, 5)):
            pattern = text[:pattern_len]
            if len(pattern) > 0 and len(text) >= pattern_len * 4:
                # Check if this pattern repeats throughout
                full_pattern = (pattern * (len(text) // len(pattern)) + 
                              pattern[:len(text) % len(pattern)])
                if full_pattern == text:
                    return False
    
    # Check for very short comments (3 characters or less)
    clean_text = re.sub(r'[^a-zA-Záéíóúñü]', ' ', text)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    
    if len(clean_text) < 3:
        return False
    
    # Also check for very short repeated patterns that might be spam (like jajajaja)
    # Check if the string is mostly made of repeating patterns
    clean_text = re.sub(r'[^a-zA-Z0-9áéíóúñü]', '', text)
    if len(clean_text) > 4:
        # Look for simple repeating patterns like "ababab"
        pattern_length = min(3, len(clean_text) // 2)
        for i in range(1, pattern_length + 1):
            pattern = clean_text[:i]
            if len(pattern) > 0 and len(clean_text) >= 4 * len(pattern):
                # Check if the pattern repeats throughout
                if pattern * (len(clean_text) // len(pattern)) == clean_text[:len(pattern) * (len(clean_text) // len(pattern))]:
                    # Only filter if it's clearly spam-like (more than 3 repetitions)
                    if len(clean_text) // len(pattern) >= 4:
                        return False
    
    # Check for adoration patterns with word boundaries to avoid false positives
    adoration_match = any(re.search(pattern, text) for pattern in ADORATION_PATTERNS)
    
    if adoration_match:
        return False  # It's adoration, not substantive
    
    # Check for bot patterns
    bot_match = any(re.search(pattern, text) for pattern in BOT_PATTERNS)
    
    if bot_match:
        return False  # It's a bot message, not substantive
    
    # If it doesn't match any filtering criteria, consider it substantive
    return True

def is_substantive_dm(dm_text):
    """
    Determines if a direct message is substantive.
    """
    # Convert to lowercase for case-insensitive matching
    text = dm_text.lower()
    
    # Check for very short or emoji-only comments that are likely spam/bots
    # Remove all non-alphabetic characters and check if it's mostly emojis
    emoji_only = re.sub(r'[^\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]', '', text)
    letter_only = re.sub(r'[^a-zA-Záéíóúñü]', '', text)
    
    # If more than 70% of the characters are emojis, filter it out
    if len(text) > 0 and len(emoji_only) / len(text) > 0.7:
        return False
    
    # Check for repeating characters like 'jajajaja'
    if re.search(r'(.)\1{3,}', text):
        return False
    
    # Check for adoration patterns with word boundaries to avoid false positives
    adoration_match = any(re.search(pattern, text) for pattern in ADORATION_PATTERNS)
    
    if adoration_match:
        return False  # It's adoration, not substantive
    
    # Check for bot patterns
    bot_match = any(re.search(pattern, text) for pattern in BOT_PATTERNS)
    
    if bot_match:
        return False  # It's a bot message, not substantive
    
    # Check for very short comments (3 characters or less)
    clean_text = re.sub(r'[^a-zA-Záéíóúñü]', ' ', text)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    
    if len(clean_text) < 3:
        return False
    
    # If it doesn't match any filtering criteria, consider it substantive
    return True

def is_likely_bot_message(message_text):
    """
    Determines if a message is likely from a bot based on patterns.
    """
    # Convert to lowercase for case-insensitive matching
    text = message_text.lower()
    
    # Check for bot patterns
    bot_match = any(re.search(pattern, text) for pattern in BOT_PATTERNS)
    
    return bot_match