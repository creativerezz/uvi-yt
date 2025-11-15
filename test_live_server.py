#!/usr/bin/env python3
"""
Test script for live production server transcript fetching.
"""
import urllib.request
import urllib.parse
import json
import sys
from typing import Dict, Any

BASE_URL = "https://fetch.youtubesummaries.cc"

def test_endpoint(endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Test an endpoint and return the result."""
    url = f"{BASE_URL}{endpoint}"
    if params:
        query_string = urllib.parse.urlencode(params)
        url = f"{url}?{query_string}"
    
    try:
        print(f"\n🔍 Testing: {url}")
        with urllib.request.urlopen(url, timeout=15) as response:
            content = response.read().decode('utf-8')
            status_code = response.getcode()
            
            # Try to parse as JSON
            try:
                data = json.loads(content)
                return {
                    "status_code": status_code,
                    "success": True,
                    "data": data,
                    "raw": content[:200] if len(content) > 200 else content
                }
            except json.JSONDecodeError:
                return {
                    "status_code": status_code,
                    "success": True,
                    "data": None,
                    "raw": content[:500] if len(content) > 500 else content
                }
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        try:
            error_data = json.loads(error_body)
        except:
            error_data = {"detail": error_body[:200]}
        return {
            "status_code": e.code,
            "success": False,
            "error": error_data,
            "raw": error_body[:200]
        }
    except Exception as e:
        return {
            "status_code": None,
            "success": False,
            "error": str(e),
            "raw": None
        }

def print_result(result: Dict[str, Any], show_data: bool = True):
    """Print test result in a readable format."""
    if result["success"]:
        print(f"✅ Status: {result['status_code']}")
        if show_data and result.get("data"):
            if isinstance(result["data"], dict):
                print(f"📦 Response keys: {list(result['data'].keys())}")
                if "detail" in result["data"]:
                    print(f"⚠️  Error: {result['data']['detail']}")
                elif len(str(result["data"])) < 500:
                    print(f"📄 Data: {json.dumps(result['data'], indent=2)}")
                else:
                    print(f"📄 Data length: {len(str(result['data']))} characters")
            elif isinstance(result["data"], list):
                print(f"📦 List length: {len(result['data'])}")
                if len(result["data"]) > 0:
                    print(f"📄 First item: {result['data'][0]}")
            else:
                print(f"📄 Response: {result['raw'][:200]}...")
        elif result.get("raw"):
            print(f"📄 Response: {result['raw'][:300]}...")
    else:
        print(f"❌ Failed: {result.get('status_code', 'No status')}")
        if result.get("error"):
            print(f"⚠️  Error: {result['error']}")

def main():
    print("=" * 60)
    print("Testing Live Production Server")
    print(f"Base URL: {BASE_URL}")
    print("=" * 60)
    
    # Test 1: Health check
    print("\n" + "=" * 60)
    print("TEST 1: Health Check")
    print("=" * 60)
    result = test_endpoint("/health")
    print_result(result)
    
    # Test 2: Metadata
    print("\n" + "=" * 60)
    print("TEST 2: Video Metadata")
    print("=" * 60)
    result = test_endpoint("/youtube/metadata", {"video": "dQw4w9WgXcQ"})
    print_result(result)
    
    # Test 3: Captions
    print("\n" + "=" * 60)
    print("TEST 3: Video Captions (Transcript)")
    print("=" * 60)
    result = test_endpoint("/youtube/captions", {"video": "dQw4w9WgXcQ"})
    if result["success"] and result.get("raw"):
        print(f"✅ Status: {result['status_code']}")
        print(f"📄 Caption length: {len(result['raw'])} characters")
        print(f"📄 First 200 chars: {result['raw'][:200]}...")
    else:
        print_result(result)
    
    # Test 4: Timestamps
    print("\n" + "=" * 60)
    print("TEST 4: Video Timestamps")
    print("=" * 60)
    result = test_endpoint("/youtube/timestamps", {"video": "dQw4w9WgXcQ"})
    print_result(result, show_data=False)
    if result["success"] and isinstance(result.get("data"), list):
        print(f"📦 Timestamp count: {len(result['data'])}")
        if len(result["data"]) > 0:
            print(f"📄 First 5 timestamps:")
            for ts in result["data"][:5]:
                print(f"   - {ts}")
    
    # Test 5: Different video
    print("\n" + "=" * 60)
    print("TEST 5: Different Video (jNQXAC9IVRw)")
    print("=" * 60)
    result = test_endpoint("/youtube/captions", {"video": "jNQXAC9IVRw"})
    if result["success"] and result.get("raw"):
        print(f"✅ Status: {result['status_code']}")
        print(f"📄 Caption length: {len(result['raw'])} characters")
        print(f"📄 Preview: {result['raw'][:150]}...")
    else:
        print_result(result)
    
    # Test 6: Error handling
    print("\n" + "=" * 60)
    print("TEST 6: Error Handling (Invalid Video ID)")
    print("=" * 60)
    result = test_endpoint("/youtube/captions", {"video": "INVALID_ID_12345"})
    print_result(result)
    
    # Test 7: Cache stats
    print("\n" + "=" * 60)
    print("TEST 7: Cache Statistics")
    print("=" * 60)
    result = test_endpoint("/youtube/cache/stats")
    print_result(result)
    
    # Test 8: Service status
    print("\n" + "=" * 60)
    print("TEST 8: Service Status")
    print("=" * 60)
    result = test_endpoint("/service/status")
    print_result(result, show_data=False)
    if result["success"] and isinstance(result.get("data"), dict):
        data = result["data"]
        print(f"📦 Service: {data.get('status', 'unknown')}")
        print(f"📦 Version: {data.get('version', 'unknown')}")
        if "features" in data:
            features = data["features"]
            print(f"📦 Cache enabled: {features.get('cache_enabled', False)}")
            print(f"📦 Cache size: {features.get('cache_size', 0)}")
            print(f"📦 Proxy enabled: {features.get('proxy_enabled', False)}")
    
    print("\n" + "=" * 60)
    print("Testing Complete!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

