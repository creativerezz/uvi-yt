import logging
from typing import List, Optional

from fastapi import APIRouter, Query, HTTPException

from app.utils.youtube_tools import YouTubeTools
from app.utils.transcript_cache import get_cache

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/youtube",
    tags=["youtube"],
    responses={404: {"description": "Not found"}},
)

# NOTE: We switched to **query parameters** so users can simply paste a URL or
# video ID in the Swagger UI without having to wrap it in a JSON object.  The
# *languages* parameter defaults to ``["en"]`` so callers can ignore it when
# they only need English captions.

@router.get(
    "/metadata",
    summary="Get video metadata",
    response_description="Clean YouTube oEmbed metadata for the requested video.",
)
async def get_video_metadata(
    video: str = Query(
        ..., description="YouTube video URL or ID", examples=["https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"]
    ),
):
    """Return basic video information such as *title*, *author* and *thumbnail*."""
    try:
        return YouTubeTools.get_video_data(video)
    except HTTPException:
        # Re-raise HTTPExceptions as-is (they're already properly formatted)
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_video_metadata: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve video metadata: {str(e)}"
        )

@router.get(
    "/captions",
    summary="Get plain-text captions",
    response_description="Concatenated caption text (one large string) for the requested video.",
)
async def get_video_captions(
    video: str = Query(..., description="YouTube video URL or ID"),
    languages: Optional[List[str]] = Query(None, description="Preferred caption languages (ISO 639-1 codes). Default: ['en']"),
):
    """Return plain-text captions for the requested video (English by default)."""
    try:
        return YouTubeTools.get_video_captions(video, languages)
    except HTTPException:
        # Re-raise HTTPExceptions as-is (they're already properly formatted)
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_video_captions: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve video captions: {str(e)}"
        )

@router.get(
    "/timestamps",
    summary="Get caption timestamps",
    response_description="A list of caption lines with starting timestamps.",
)
async def get_video_timestamps(
    video: str = Query(..., description="YouTube video URL or ID"),
    languages: Optional[List[str]] = Query(None, description="Preferred caption languages (ISO 639-1 codes). Default: ['en']"),
):
    """Return caption text with starting timestamps (English by default)."""
    try:
        return YouTubeTools.get_video_timestamps(video, languages)
    except HTTPException:
        # Re-raise HTTPExceptions as-is (they're already properly formatted)
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_video_timestamps: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve video timestamps: {str(e)}"
        )

@router.get(
    "/cache/stats",
    summary="Get cache statistics",
    response_description="Current cache statistics including size and configuration.",
)
async def get_cache_stats():
    """Return cache statistics and configuration."""
    try:
        cache = get_cache()
        return {
            "enabled": cache.enabled,
            "size": cache.size(),
            "max_size": cache.max_size,
            "ttl_seconds": cache.ttl_seconds,
        }
    except Exception as e:
        logger.error(f"Unexpected error in get_cache_stats: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve cache statistics: {str(e)}"
        )

@router.delete(
    "/cache/clear",
    summary="Clear transcript cache",
    response_description="Clears all cached transcripts.",
)
async def clear_cache():
    """Clear all cached transcripts."""
    try:
        cache = get_cache()
        cache.clear()
        return {"message": "Cache cleared successfully", "size": cache.size()}
    except Exception as e:
        logger.error(f"Unexpected error in clear_cache: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear cache: {str(e)}"
        )

@router.get(
    "/performance/test",
    summary="Test transcript performance",
    response_description="Performance metrics for transcript fetching (cache miss vs cache hit).",
)
async def test_performance(
    video: str = Query(..., description="YouTube video URL or ID"),
    runs: int = Query(3, ge=2, le=10, description="Number of test runs (default: 3)"),
    languages: Optional[List[str]] = Query(None, description="Preferred caption languages. Default: ['en']"),
):
    """
    Test transcript fetching performance.
    
    Makes multiple requests to measure cache miss (first request) vs cache hit (subsequent requests) performance.
    Useful for benchmarking cache effectiveness.
    
    Returns:
        Performance metrics including response times and speedup factor
    """
    try:
        import time
        
        video_id = YouTubeTools.get_youtube_video_id(video)
        if not video_id:
            raise HTTPException(status_code=400, detail="Invalid YouTube URL/ID")
        
        normalized_languages = languages or ["en"]
        times = []
        errors = []
        
        for i in range(runs):
            start_time = time.perf_counter()
            try:
                # Fetch transcript (will use cache after first request)
                transcript = YouTubeTools._fetch_transcript(video_id, normalized_languages)
                elapsed = time.perf_counter() - start_time
                times.append(elapsed)
            except Exception as e:
                elapsed = time.perf_counter() - start_time
                errors.append(str(e))
                times.append(None)
        
        if not times or all(t is None for t in times):
            raise HTTPException(
                status_code=500,
                detail=f"All requests failed. Errors: {', '.join(errors) if errors else 'Unknown error'}"
            )
        
        # Filter out None values for calculations
        valid_times = [t for t in times if t is not None]
        
        cache_miss_time = valid_times[0] if valid_times else None
        cache_hit_times = valid_times[1:] if len(valid_times) > 1 else []
        
        result = {
            "video_id": video_id,
            "runs": runs,
            "successful_runs": len(valid_times),
            "cache_miss": {
                "time_seconds": cache_miss_time,
                "time_ms": cache_miss_time * 1000 if cache_miss_time else None,
            } if cache_miss_time else None,
            "cache_hits": {
                "count": len(cache_hit_times),
                "times_seconds": cache_hit_times,
                "times_ms": [t * 1000 for t in cache_hit_times],
                "avg_seconds": sum(cache_hit_times) / len(cache_hit_times) if cache_hit_times else None,
                "avg_ms": (sum(cache_hit_times) / len(cache_hit_times) * 1000) if cache_hit_times else None,
                "min_seconds": min(cache_hit_times) if cache_hit_times else None,
                "max_seconds": max(cache_hit_times) if cache_hit_times else None,
            } if cache_hit_times else None,
            "speedup": cache_miss_time / (sum(cache_hit_times) / len(cache_hit_times)) if cache_miss_time and cache_hit_times else None,
        }
        
        return result
    except HTTPException:
        # Re-raise HTTPExceptions as-is (they're already properly formatted)
        raise
    except Exception as e:
        logger.error(f"Unexpected error in test_performance: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to run performance test: {str(e)}"
        )