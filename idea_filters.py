# Patrones para ADORATION_PATTERNS
ADORATION_PATTERNS = [
    r"amazing",
    r"beautiful",
    r"gorgeous",
    r"incredible",
    r"inspiring",
    r"love",
    r"lovely",
    r"marvelous",
    r"phenomenal",
    r"perfect",
    r"stunning",
    r"wonderful",
    r"excellent",
    r"fantastic",
    r"great",
    r"superb",
    r"brilliant",
    r"outstanding",
    r"amazingly",
    r"incredibly",
    r"absolutely",
    r"totally",
    r"so good",
    r"so beautiful",
    r"so amazing",
    r"so wonderful",
    r"so perfect",
    r"so great",
    r"so incredible",
    r"so brilliant",
    r"so outstanding",
    r"so fantastic",
    r"so excellent",
    r"so marvelous",
    r"so lovely",
    r"so stunning",
    r"so inspiring",
    r"so amazing",
    r"so perfect",
    r"so good",
    r"so beautiful",
    r"so wonderful",
    r"so great",
    r"so incredible",
    r"so brilliant",
    r"so outstanding",
    r"so fantastic",
    r"so excellent",
    r"so marvelous",
    r"so lovely",
    r"so stunning",
    r"so inspiring",
    r"so amazing",
    r"so perfect",
    r"so good",
    r"so beautiful",
    r"so wonderful",
    r"so great",
    r"so incredible",
    r"so brilliant",
    r"so outstanding",
    r"so fantastic",
    r"so excellent",
    r"so marvelous",
    r"so lovely",
    r"so stunning",
    r"so inspiring",
]

# Patrones para BOT_PATTERNS
BOT_PATTERNS = [
    r"follow me",
    r"follow back",
    r"follow for follow",
    r"follow for follows",
    r"follow for f",
    r"followers",
    r"following",
    r"like for like",
    r"like for likes",
    r"like for l",
    r"likes",
    r"love for love",
    r"love for loves",
    r"love for l",
    r"loves",
    r"comment for comment",
    r"comment for comments",
    r"comment for c",
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
    r"flash sale",
    r"deal of the day",
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
    r"love those so much",
    r"love it so much",
    r"love this so much",
    r"love that so much",
    r"love these so much",
    r"love those so much",
    r"love it so much",
    r"love this so much",
    r"love that so much",
    r"love these so much",
    r"love those so much",
    r"love it so much",
    r"love this so much",
    r"love that so much",
    r"love these so much",
    r"love those so much",
    r"love it so much",
    r"love this so much",
    r"love that so much",
    r"love these so much",
    r"love those so much",
    r"love it so much",
    r"love this so much",
    r"love that so much",
    r"love these so much",
    r"love those so much",
    r"love it so much",
    r"love this so much",
    r"love that so much",
    r"love these so much",
    r"love those so much",
]

import re

def is_substantive_comment(comment_text):
    """
    Determines if a comment is substantive (not a bot or adoration).
    """
    # Convert to lowercase for case-insensitive matching
    text = comment_text.lower()
    
    # Check for adoration patterns
    adoration_match = any(re.search(pattern, text) for pattern in ADORATION_PATTERNS)
    
    if adoration_match:
        return False  # It's adoration, not substantive
    
    # Check for bot patterns
    bot_match = any(re.search(pattern, text) for pattern in BOT_PATTERNS)
    
    if bot_match:
        return False  # It's a bot message, not substantive
    
    # If it doesn't match either category, consider it substantive
    return True

def is_substantive_dm(dm_text):
    """
    Determines if a direct message is substantive.
    """
    # Convert to lowercase for case-insensitive matching
    text = dm_text.lower()
    
    # Check for adoration patterns
    adoration_match = any(re.search(pattern, text) for pattern in ADORATION_PATTERNS)
    
    if adoration_match:
        return False  # It's adoration, not substantive
    
    # Check for bot patterns
    bot_match = any(re.search(pattern, text) for pattern in BOT_PATTERNS)
    
    if bot_match:
        return False  # It's a bot message, not substantive
    
    # If it doesn't match either category, consider it substantive
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