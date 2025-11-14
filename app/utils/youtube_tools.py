import json
from urllib.parse import urlparse, parse_qs, urlencode
from urllib.request import urlopen
from typing import Optional, List

from fastapi import HTTPException
from youtube_transcript_api import YouTubeTranscriptApi  # type: ignore
from youtube_transcript_api.proxies import GenericProxyConfig, WebshareProxyConfig
from app.core.config import settings
from app.utils.transcript_cache import get_cache, Transcript

class YouTubeTools:
    @staticmethod
    def _get_youtube_api() -> YouTubeTranscriptApi:
        """Create YouTubeTranscriptApi instance with proxy configuration if available."""
        proxy_config = None
        
        if settings.PROXY_TYPE == "generic" and settings.PROXY_URL:
            # Use the provided proxy URL for both HTTP and HTTPS
            proxy_config = GenericProxyConfig(
                http_url=settings.PROXY_URL,
                https_url=settings.PROXY_URL
            )
        elif settings.PROXY_TYPE == "generic" and (settings.PROXY_HTTP or settings.PROXY_HTTPS):
            # Use separate HTTP/HTTPS proxies if provided
            proxy_config = GenericProxyConfig(
                http_url=settings.PROXY_HTTP or settings.PROXY_HTTPS,
                https_url=settings.PROXY_HTTPS or settings.PROXY_HTTP
            )
        elif settings.PROXY_TYPE == "webshare" and settings.WEBSHARE_USERNAME and settings.WEBSHARE_PASSWORD:
            # Use Webshare rotating proxies
            proxy_config = WebshareProxyConfig(
                proxy_username=settings.WEBSHARE_USERNAME,
                proxy_password=settings.WEBSHARE_PASSWORD
            )
        
        return YouTubeTranscriptApi(proxy_config=proxy_config)

    @staticmethod
    def _fetch_transcript(video_id: str, languages: Optional[List[str]] = None) -> List[Transcript]:
        """
        Fetch transcript for a video, using cache if available.
        
        This is a shared method used by both get_video_captions and get_video_timestamps
        to avoid duplicate API calls and benefit from caching.
        
        Args:
            video_id: YouTube video ID
            languages: List of language codes (e.g., ["en", "es"])
            
        Returns:
            List of transcript snippets
            
        Raises:
            HTTPException: If transcript cannot be fetched
        """
        cache = get_cache()
        normalized_languages = languages or ["en"]
        
        # Try to get from cache first
        cached_transcript = cache.get(video_id, normalized_languages)
        if cached_transcript is not None:
            return cached_transcript
        
        # Cache miss - fetch from API
        try:
            api = YouTubeTools._get_youtube_api()
            transcript = api.fetch(video_id, languages=normalized_languages)
            
            # Store in cache
            cache.set(video_id, transcript, normalized_languages)
            
            return transcript
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting captions for video: {str(e)}")

    @staticmethod
    def get_youtube_video_id(url_or_id: str) -> Optional[str]:
        """Extract a YouTube video ID from either a full URL *or* a raw video ID.

        This helper now supports three input formats so that the API is more
        forgiving when used from the interactive docs:

        1. Full YouTube watch URLs – e.g. ``https://www.youtube.com/watch?v=dQw4w9WgXcQ``
        2. Shortened URLs – e.g. ``https://youtu.be/dQw4w9WgXcQ``
        3. A plain 11-character video ID – e.g. ``dQw4w9WgXcQ``
        """

        # First, handle the case where the user passed the plain 11-character ID.
        allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-"
        if len(url_or_id) == 11 and all(ch in allowed_chars for ch in url_or_id):
            return url_or_id

        # Otherwise, attempt to parse as a URL.
        parsed_url = urlparse(url_or_id)
        hostname = parsed_url.hostname

        if hostname == "youtu.be":
            return parsed_url.path.lstrip("/") or None

        if hostname in ("www.youtube.com", "youtube.com"):
            if parsed_url.path == "/watch":
                query_params = parse_qs(parsed_url.query)
                return query_params.get("v", [None])[0]
            if parsed_url.path.startswith("/embed/"):
                return parsed_url.path.split("/")[2]
            if parsed_url.path.startswith("/v/"):
                return parsed_url.path.split("/")[2]

        return None

    @staticmethod
    def get_video_data(url: str) -> dict:
        """Function to get video data from a YouTube URL."""
        if not url:
            raise HTTPException(status_code=400, detail="No URL provided")

        try:
            video_id = YouTubeTools.get_youtube_video_id(url)
            if not video_id:
                raise HTTPException(status_code=400, detail="Invalid YouTube URL")
        except Exception:
            raise HTTPException(status_code=400, detail="Error getting video ID from URL")

        try:
            params = {"format": "json", "url": f"https://www.youtube.com/watch?v={video_id}"}
            oembed_url = "https://www.youtube.com/oembed"
            query_string = urlencode(params)
            full_url = oembed_url + "?" + query_string

            with urlopen(full_url) as response:
                response_text = response.read()
                video_data = json.loads(response_text.decode())
                clean_data = {
                    "title": video_data.get("title"),
                    "author_name": video_data.get("author_name"),
                    "author_url": video_data.get("author_url"),
                    "type": video_data.get("type"),
                    "height": video_data.get("height"),
                    "width": video_data.get("width"),
                    "version": video_data.get("version"),
                    "provider_name": video_data.get("provider_name"),
                    "provider_url": video_data.get("provider_url"),
                    "thumbnail_url": video_data.get("thumbnail_url"),
                }
                return clean_data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting video data: {str(e)}")

    @staticmethod
    def get_video_captions(url_or_id: str, languages: Optional[List[str]] = None) -> str:
        """Return plain-text captions for the requested YouTube video.

        If *languages* is omitted, English (``["en"]``) will be used by default.
        """

        if not url_or_id:
            raise HTTPException(status_code=400, detail="No URL or ID provided")

        video_id = YouTubeTools.get_youtube_video_id(url_or_id)
        if not video_id:
            raise HTTPException(status_code=400, detail="Invalid YouTube URL/ID")

        transcript = YouTubeTools._fetch_transcript(video_id, languages)
        
        if transcript:
            return " ".join(snippet.text for snippet in transcript)
        return "No captions found for video"

    @staticmethod
    def get_video_timestamps(url_or_id: str, languages: Optional[List[str]] = None) -> List[str]:
        """Return caption lines prefixed with the *start* timestamp.

        The function now mirrors :py:meth:`get_video_captions` and accepts either
        a full URL **or** a raw 11-character video ID.  If *languages* is
        omitted we default to English (``["en"]``).
        """

        if not url_or_id:
            raise HTTPException(status_code=400, detail="No URL or ID provided")

        video_id = YouTubeTools.get_youtube_video_id(url_or_id)
        if not video_id:
            raise HTTPException(status_code=400, detail="Invalid YouTube URL/ID")

        transcript = YouTubeTools._fetch_transcript(video_id, languages)
        
        timestamps: List[str] = []
        for snippet in transcript:
            start = int(snippet.start)
            minutes, seconds = divmod(start, 60)
            timestamps.append(f"{minutes}:{seconds:02d} - {snippet.text}")
        return timestamps