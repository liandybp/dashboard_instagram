def filter_spam_comments(comment_text):
    """
    Filter out spam and non-substantive comments.
    This is a simple implementation - in practice this would be more sophisticated.
    """
    # Common spam patterns
    spam_indicators = [
        "like", "follow", "subscrib", "comment",  # Generic spam words
        "free", "win", "prize", "cash", "money",  # Scam indicators
        "click here", "buy now", "limited time",  # Sales tactics
    ]
    
    # Check if comment is too short or contains spam patterns
    if len(comment_text) < 5:
        return False
    
    comment_lower = comment_text.lower()
    for indicator in spam_indicators:
        if indicator in comment_lower:
            return False
            
    # If we get here, it's likely a substantive comment
    return True