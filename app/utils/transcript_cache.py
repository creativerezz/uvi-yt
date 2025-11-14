"""
Transcript cache module for storing YouTube transcript data.

Provides in-memory caching with TTL (time-to-live) support to reduce
API calls and improve response times.
"""
import time
from typing import Optional, List, Tuple
from collections import OrderedDict

from youtube_transcript_api._types import Transcript  # type: ignore
from app.core.config import settings


class TranscriptCache:
    """
    In-memory cache for YouTube transcripts with TTL support.
    
    Uses LRU (Least Recently Used) eviction when cache reaches max size.
    Cache keys are tuples of (video_id, language_tuple).
    """
    
    def __init__(self):
        self._cache: OrderedDict[Tuple[str, tuple], Tuple[List[Transcript], float]] = OrderedDict()
        self.enabled = settings.CACHE_ENABLED
        self.ttl_seconds = settings.CACHE_TTL_SECONDS
        self.max_size = settings.CACHE_MAX_SIZE
    
    def _make_key(self, video_id: str, languages: Optional[List[str]]) -> Tuple[str, tuple]:
        """Create a cache key from video_id and languages."""
        lang_tuple = tuple(sorted(languages)) if languages else ("en",)
        return (video_id, lang_tuple)
    
    def _is_expired(self, timestamp: float) -> bool:
        """Check if a cache entry has expired based on TTL."""
        return time.time() - timestamp > self.ttl_seconds
    
    def get(self, video_id: str, languages: Optional[List[str]] = None) -> Optional[List[Transcript]]:
        """
        Get cached transcript if available and not expired.
        
        Args:
            video_id: YouTube video ID
            languages: List of language codes (e.g., ["en", "es"])
            
        Returns:
            Cached transcript list if found and valid, None otherwise
        """
        if not self.enabled:
            return None
        
        key = self._make_key(video_id, languages)
        
        if key not in self._cache:
            return None
        
        transcript, timestamp = self._cache[key]
        
        # Check if expired
        if self._is_expired(timestamp):
            del self._cache[key]
            return None
        
        # Move to end (most recently used)
        self._cache.move_to_end(key)
        return transcript
    
    def set(self, video_id: str, transcript: List[Transcript], languages: Optional[List[str]] = None) -> None:
        """
        Cache a transcript.
        
        Args:
            video_id: YouTube video ID
            transcript: List of transcript snippets
            languages: List of language codes used to fetch the transcript
        """
        if not self.enabled:
            return
        
        key = self._make_key(video_id, languages)
        timestamp = time.time()
        
        # Remove if already exists
        if key in self._cache:
            del self._cache[key]
        
        # Evict oldest entries if cache is full
        while len(self._cache) >= self.max_size:
            self._cache.popitem(last=False)  # Remove oldest (first) item
        
        # Add new entry
        self._cache[key] = (transcript, timestamp)
    
    def clear(self) -> None:
        """Clear all cached transcripts."""
        self._cache.clear()
    
    def size(self) -> int:
        """Get current cache size."""
        return len(self._cache)
    
    def cleanup_expired(self) -> int:
        """
        Remove expired entries from cache.
        
        Returns:
            Number of entries removed
        """
        if not self.enabled:
            return 0
        
        expired_keys = [
            key for key, (_, timestamp) in self._cache.items()
            if self._is_expired(timestamp)
        ]
        
        for key in expired_keys:
            del self._cache[key]
        
        return len(expired_keys)


# Global cache instance
_transcript_cache = TranscriptCache()


def get_cache() -> TranscriptCache:
    """Get the global transcript cache instance."""
    return _transcript_cache

