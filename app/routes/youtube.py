from typing import List, Optional

from fastapi import APIRouter, Query

from app.utils.youtube_tools import YouTubeTools

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

    return YouTubeTools.get_video_data(video)

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

    return YouTubeTools.get_video_captions(video, languages)

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

    return YouTubeTools.get_video_timestamps(video, languages)