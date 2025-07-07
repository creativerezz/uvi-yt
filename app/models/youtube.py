from typing import Optional, List
from pydantic import BaseModel, Field

class YouTubeRequest(BaseModel):
    """Request body for YouTube-related endpoints.

    * **video** – Either a full YouTube URL *or* the plain 11-character video ID.
    * **languages** – Optional list of language codes (e.g. ``["en"]``). Defaults to
      English when omitted.
    """

    video: str = Field(..., description="YouTube video URL or ID", examples=["https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"])
    languages: Optional[List[str]] = Field(None, description="Preferred caption languages (ISO 639-1 codes)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "video": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "languages": ["en"]
            }
        }
    }

class VideoData(BaseModel):
    """
    Model for YouTube video metadata.
    
    Attributes:
        title: Video title
        author_name: Channel name
        author_url: Channel URL
        type: Media type
        height: Video height
        width: Video width
        version: API version
        provider_name: Service provider name
        provider_url: Service provider URL
        thumbnail_url: Thumbnail URL
    """
    title: Optional[str] = None
    author_name: Optional[str] = None
    author_url: Optional[str] = None
    type: Optional[str] = None
    height: Optional[int] = None
    width: Optional[int] = None
    version: Optional[str] = None
    provider_name: Optional[str] = None
    provider_url: Optional[str] = None
    thumbnail_url: Optional[str] = None