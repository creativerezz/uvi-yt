#!/usr/bin/env python3
"""
Transcript Speed Test Script

Tests the performance of transcript fetching endpoints, comparing
cached vs uncached response times.
"""

import time
import asyncio
import statistics
from typing import List, Dict, Tuple
import httpx
from urllib.parse import urlencode


class TranscriptSpeedTest:
    """Test transcript endpoint performance."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def check_server_health(self) -> bool:
        """Check if server is healthy before running tests."""
        try:
            response = await self.client.get(f"{self.base_url}/health", timeout=5.0)
            if response.status_code == 200:
                return True
            print(f"⚠️  Health check returned status {response.status_code}")
            return False
        except Exception as e:
            print(f"❌ Cannot reach server: {str(e)}")
            print(f"   Make sure the server is running at {self.base_url}")
            return False
    
    async def fetch_transcript(self, video_id: str, languages: List[str] = None) -> Tuple[float, bool]:
        """
        Fetch transcript and measure time.
        
        Returns:
            Tuple of (response_time_seconds, success)
        """
        languages = languages or ["en"]
        params = {
            "video": video_id,
            "languages": ",".join(languages)
        }
        url = f"{self.base_url}/youtube/captions?{urlencode(params)}"
        
        start_time = time.perf_counter()
        try:
            response = await self.client.get(url, timeout=30.0)
            elapsed = time.perf_counter() - start_time
            
            if response.status_code == 200:
                return (elapsed, True)
            else:
                # Better error messages for common status codes
                if response.status_code == 502:
                    error_msg = "Bad Gateway - Server may be down or restarting"
                elif response.status_code == 503:
                    error_msg = "Service Unavailable - Server is overloaded"
                elif response.status_code == 504:
                    error_msg = "Gateway Timeout - Request took too long"
                elif response.status_code == 500:
                    error_msg = "Internal Server Error"
                else:
                    error_msg = f"HTTP {response.status_code}"
                
                # Try to parse error detail from JSON response
                try:
                    error_data = response.json()
                    if "detail" in error_data:
                        error_msg = f"{error_msg}: {error_data['detail']}"
                except:
                    # If not JSON, show first 100 chars of response
                    text_preview = response.text[:100].replace('\n', ' ')
                    if text_preview:
                        error_msg = f"{error_msg} - {text_preview}"
                
                print(f"  ⚠️  Error {response.status_code}: {error_msg}")
                return (elapsed, False)
        except httpx.TimeoutException:
            elapsed = time.perf_counter() - start_time
            print(f"  ⏱️  Timeout after {elapsed:.2f}s - Request took too long")
            return (elapsed, False)
        except httpx.ConnectError as e:
            elapsed = time.perf_counter() - start_time
            print(f"  🔌 Connection Error: Cannot connect to {self.base_url}")
            print(f"     Check if the server is running and accessible")
            return (elapsed, False)
        except Exception as e:
            elapsed = time.perf_counter() - start_time
            print(f"  ❌ Exception: {str(e)}")
            return (elapsed, False)
    
    async def test_single_video(self, video_id: str, num_runs: int = 5) -> Dict:
        """
        Test a single video with multiple runs.
        
        First run is cache miss, subsequent runs are cache hits.
        """
        print(f"\n📹 Testing video: {video_id}")
        print(f"   Running {num_runs} requests...")
        
        times: List[float] = []
        successes = 0
        
        for i in range(num_runs):
            elapsed, success = await self.fetch_transcript(video_id)
            if success:
                times.append(elapsed)
                successes += 1
                cache_status = "🔄 Cache MISS" if i == 0 else "✅ Cache HIT"
                print(f"   Run {i+1}: {elapsed*1000:.2f}ms {cache_status}")
            else:
                print(f"   Run {i+1}: Failed")
            
            # Small delay between requests
            await asyncio.sleep(0.1)
        
        if not times:
            return {
                "video_id": video_id,
                "success": False,
                "error": "All requests failed"
            }
        
        cache_miss_time = times[0] if len(times) > 0 else None
        cache_hit_times = times[1:] if len(times) > 1 else []
        
        result = {
            "video_id": video_id,
            "success": True,
            "total_runs": num_runs,
            "successful_runs": successes,
            "cache_miss_time": cache_miss_time,
            "cache_hit_times": cache_hit_times,
            "cache_hit_avg": statistics.mean(cache_hit_times) if cache_hit_times else None,
            "cache_hit_min": min(cache_hit_times) if cache_hit_times else None,
            "cache_hit_max": max(cache_hit_times) if cache_hit_times else None,
            "speedup": cache_miss_time / statistics.mean(cache_hit_times) if cache_hit_times and cache_miss_time else None,
        }
        
        return result
    
    async def test_multiple_videos(self, video_ids: List[str], runs_per_video: int = 3) -> List[Dict]:
        """Test multiple videos."""
        results = []
        for video_id in video_ids:
            result = await self.test_single_video(video_id, runs_per_video)
            results.append(result)
            await asyncio.sleep(0.5)  # Delay between videos
        return results
    
    async def get_cache_stats(self) -> Dict:
        """Get current cache statistics."""
        try:
            response = await self.client.get(f"{self.base_url}/youtube/cache/stats")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"⚠️  Could not fetch cache stats: {e}")
        return {}
    
    async def clear_cache(self) -> bool:
        """Clear the transcript cache."""
        try:
            response = await self.client.delete(f"{self.base_url}/youtube/cache/clear")
            return response.status_code == 200
        except Exception as e:
            print(f"⚠️  Could not clear cache: {e}")
            return False
    
    def print_results(self, results: List[Dict]):
        """Print formatted test results."""
        print("\n" + "="*70)
        print("📊 PERFORMANCE TEST RESULTS")
        print("="*70)
        
        successful_tests = [r for r in results if r.get("success")]
        
        if not successful_tests:
            print("\n❌ No successful tests to report.")
            return
        
        print(f"\n✅ Successful tests: {len(successful_tests)}/{len(results)}")
        
        # Summary statistics
        cache_miss_times = [r["cache_miss_time"] for r in successful_tests if r.get("cache_miss_time")]
        cache_hit_avgs = [r["cache_hit_avg"] for r in successful_tests if r.get("cache_hit_avg")]
        speedups = [r["speedup"] for r in successful_tests if r.get("speedup")]
        
        if cache_miss_times:
            print(f"\n📈 Cache MISS (First Request):")
            print(f"   Average: {statistics.mean(cache_miss_times)*1000:.2f}ms")
            print(f"   Min:     {min(cache_miss_times)*1000:.2f}ms")
            print(f"   Max:     {max(cache_miss_times)*1000:.2f}ms")
        
        if cache_hit_avgs:
            print(f"\n⚡ Cache HIT (Subsequent Requests):")
            print(f"   Average: {statistics.mean(cache_hit_avgs)*1000:.2f}ms")
            print(f"   Min:     {min(cache_hit_avgs)*1000:.2f}ms")
            print(f"   Max:     {max(cache_hit_avgs)*1000:.2f}ms")
        
        if speedups:
            avg_speedup = statistics.mean(speedups)
            print(f"\n🚀 Average Speedup: {avg_speedup:.2f}x faster")
            print(f"   Best speedup: {max(speedups):.2f}x")
            print(f"   Worst speedup: {min(speedups):.2f}x")
        
        # Per-video breakdown
        print(f"\n📋 Per-Video Breakdown:")
        print("-" * 70)
        print(f"{'Video ID':<15} {'Miss (ms)':<12} {'Hit Avg (ms)':<15} {'Speedup':<10}")
        print("-" * 70)
        
        for result in successful_tests:
            video_id = result["video_id"][:14]
            miss = result.get("cache_miss_time", 0) * 1000
            hit_avg = result.get("cache_hit_avg", 0) * 1000 if result.get("cache_hit_avg") else None
            speedup = result.get("speedup")
            
            hit_str = f"{hit_avg:.2f}" if hit_avg else "N/A"
            speedup_str = f"{speedup:.2f}x" if speedup else "N/A"
            
            print(f"{video_id:<15} {miss:<12.2f} {hit_str:<15} {speedup_str:<10}")
        
        print("="*70)


async def main():
    """Main test function."""
    import sys
    
    # Default test videos (well-known videos that should have captions)
    default_videos = [
        "dQw4w9WgXcQ",  # Rick Astley - Never Gonna Give You Up
        "jNQXAC9IVRw",  # Me at the zoo (first YouTube video)
    ]
    
    # Parse command line arguments
    base_url = "http://localhost:8000"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    video_ids = default_videos
    if len(sys.argv) > 2:
        video_ids = sys.argv[2].split(",")
    
    runs_per_video = 5
    if len(sys.argv) > 3:
        runs_per_video = int(sys.argv[3])
    
    print("🧪 Transcript Speed Test")
    print("="*70)
    print(f"Base URL: {base_url}")
    print(f"Videos to test: {len(video_ids)}")
    print(f"Runs per video: {runs_per_video}")
    
    async with TranscriptSpeedTest(base_url) as tester:
        # Check server health first
        print("\n🏥 Checking server health...")
        if not await tester.check_server_health():
            print("\n❌ Server health check failed!")
            print("\n💡 Troubleshooting:")
            print("   1. Verify the server is running")
            print("   2. Check if the URL is correct")
            print("   3. For production, check Railway deployment status:")
            print("      railway status")
            print("   4. Check server logs:")
            print("      railway logs")
            print("\n   Try testing locally first:")
            print("   python test_transcript_speed.py http://localhost:8000")
            return
        
        print("✅ Server is healthy!")
        
        # Check cache stats before
        print("\n📊 Cache Status (Before):")
        cache_stats_before = await tester.get_cache_stats()
        if cache_stats_before:
            print(f"   Enabled: {cache_stats_before.get('enabled', 'Unknown')}")
            print(f"   Size: {cache_stats_before.get('size', 0)}/{cache_stats_before.get('max_size', 0)}")
            print(f"   TTL: {cache_stats_before.get('ttl_seconds', 0)}s")
        else:
            print("   ⚠️  Could not fetch cache stats")
        
        # Clear cache for clean test
        print("\n🧹 Clearing cache for clean test...")
        cleared = await tester.clear_cache()
        if cleared:
            print("   ✅ Cache cleared")
        else:
            print("   ⚠️  Could not clear cache (may not be critical)")
        await asyncio.sleep(0.5)
        
        # Run tests
        results = await tester.test_multiple_videos(video_ids, runs_per_video)
        
        # Check cache stats after
        print("\n📊 Cache Status (After):")
        cache_stats_after = await tester.get_cache_stats()
        if cache_stats_after:
            print(f"   Size: {cache_stats_after.get('size', 0)}/{cache_stats_after.get('max_size', 0)}")
        
        # Print results
        tester.print_results(results)
        
        print("\n💡 Tips:")
        print("   - First request is slower (cache miss)")
        print("   - Subsequent requests are faster (cache hit)")
        print("   - Cache TTL: 1 hour by default")
        print("   - Test with: python test_transcript_speed.py [base_url] [video_ids] [runs]")


if __name__ == "__main__":
    asyncio.run(main())

