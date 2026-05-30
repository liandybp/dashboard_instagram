#!/usr/bin/env python3
"""
Test script to verify app.py implementation correctness
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, '/home/liandybp/PyCharmMiscProject/greter/dashboard_instagram')

def test_imports():
    """Test that all imports work correctly"""
    try:
        import streamlit as st
        import pandas as pd
        import plotly.graph_objects as go
        import plotly.express as px
        from dotenv import load_dotenv
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_id_stripping():
    """Test the ID stripping functionality"""
    try:
        from app import strip_ids
        
        # Test cases
        test_cases = [
            ("post id 123456789012", ""),
            ("comment 123456789012", ""),
            ("message 123456789012", ""),
            ("This is a normal text", "This is a normal text"),
            ("post id: 123456789012", ""),
            ("comment 123456789012 and more text", "and more text"),
        ]
        
        for input_text, expected in test_cases:
            result = strip_ids(input_text)
            if result == expected:
                print(f"✅ ID stripping works: '{input_text}' -> '{result}'")
            else:
                print(f"❌ ID stripping failed: '{input_text}' -> '{result}', expected '{expected}'")
                
        return True
    except Exception as e:
        print(f"❌ ID stripping test failed: {e}")
        return False

def test_comment_filtering():
    """Test comment filtering functionality"""
    try:
        from idea_filters import is_substantive_comment
        
        # Test cases based on requirements
        substantive_cases = [
            "¿cómo grabas el audio?",
            "me gustaría aprender a editar de cero",
            "amazing post!",
            "love this content"
        ]
        
        non_substantive_cases = [
            "te amo eres mi ídola",
            "😍😍❤️❤️", 
            "jajajaja"
        ]
        
        # Test substantive comments
        for text in substantive_cases:
            if is_substantive_comment(text):
                print(f"✅ Substantive comment correctly identified: '{text}'")
            else:
                print(f"❌ Substantive comment incorrectly filtered: '{text}'")
                
        # Test non-substantive comments  
        for text in non_substantive_cases:
            if not is_substantive_comment(text):
                print(f"✅ Non-substantive comment correctly filtered: '{text}'")
            else:
                print(f"❌ Non-substantive comment incorrectly kept: '{text}'")
                
        return True
    except Exception as e:
        print(f"❌ Comment filtering test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing app.py implementation...")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_id_stripping,
        test_comment_filtering
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"Test {test.__name__} failed with exception: {e}")
            results.append(False)
    
    print("=" * 50)
    if all(results):
        print("🎉 All tests passed! Implementation is correct.")
        return 0
    else:
        print("❌ Some tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())