#!/usr/bin/env python3
"""Test script to verify proxy configuration and server functionality"""

import sys
from app.core.config import settings
from app.utils.youtube_tools import YouTubeTools

def test_config():
    """Test configuration loading"""
    print("=" * 60)
    print("Configuration Test")
    print("=" * 60)
    print(f"✅ Proxy Type: {settings.PROXY_TYPE}")
    print(f"✅ Webshare Username: {settings.WEBSHARE_USERNAME}")
    print(f"✅ Webshare Password: {'*' * len(settings.WEBSHARE_PASSWORD)}")
    print()

def test_proxy():
    """Test proxy connection with YouTube API"""
    print("=" * 60)
    print("Proxy Connection Test")
    print("=" * 60)
    
    try:
        # Test with Fireship - How to make vibe coding not suck
        video_id = "PLKrSVuT-Dg"
        print(f"Testing with video ID: {video_id}")
        
        # Test captions
        captions = YouTubeTools.get_video_captions(video_id, languages=['en'])
        print("✅ Successfully fetched captions through proxy!")
        print(f"Caption preview: {captions[:150]}...")
        print()
        
        # Test timestamps
        timestamps = YouTubeTools.get_video_timestamps(video_id, languages=['en'])
        print("✅ Successfully fetched timestamps through proxy!")
        print(f"First 3 timestamps:")
        for ts in timestamps[:3]:
            print(f"  {ts}")
        print()
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_video_data():
    """Test video metadata fetching"""
    print("=" * 60)
    print("Video Metadata Test")
    print("=" * 60)
    
    try:
        video_url = "https://www.youtube.com/watch?v=PLKrSVuT-Dg"
        print(f"Testing with URL: {video_url}")
        
        data = YouTubeTools.get_video_data(video_url)
        print("✅ Successfully fetched video metadata!")
        print(f"Title: {data.get('title')}")
        print(f"Author: {data.get('author_name')}")
        print()
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("\n🚀 YouTube API Server - Proxy Test Suite\n")
    
    test_config()
    
    proxy_ok = test_proxy()
    metadata_ok = test_video_data()
    
    print("=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    print(f"Proxy Connection: {'✅ PASS' if proxy_ok else '❌ FAIL'}")
    print(f"Video Metadata:   {'✅ PASS' if metadata_ok else '❌ FAIL'}")
    print()
    
    if proxy_ok and metadata_ok:
        print("🎉 All tests passed! Server is ready to use with Webshare proxy.")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        sys.exit(1)
