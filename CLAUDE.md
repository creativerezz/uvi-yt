# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Essential Commands

### Development Server
- `python -m app.main`: Start the FastAPI development server
- `python run.py`: Alternative way to start the server
- `uvicorn app.main:app --reload`: Start with auto-reload for development

### Testing
- `pytest`: Run the test suite (configure tests as needed)
- `pytest -v`: Run tests with verbose output
- `pytest tests/`: Run tests from specific directory

### Docker Operations
- `docker-compose up -d`: Start the application with Docker Compose
- `docker-compose down`: Stop Docker Compose services
- `docker build -t youtube-api-server .`: Build Docker image
- `docker run -p 8000:8000 youtube-api-server`: Run containerized app

### Package Management
- `pip install -r requirements.txt`: Install dependencies
- `pip install -e .`: Install package in development mode
- `youtube-api-server`: Run via console script after package installation

## Architecture Overview

This is a **FastAPI-based YouTube API server** that extracts video metadata, captions, and timestamps. The architecture follows a clean separation of concerns:

### Core Structure
- **`app/main.py`**: FastAPI application initialization, CORS setup, and router integration
- **`app/core/config.py`**: Centralized configuration using environment variables
- **`app/models/youtube.py`**: Pydantic models for request/response validation
- **`app/routes/youtube.py`**: API endpoint handlers for YouTube operations
- **`app/utils/youtube_tools.py`**: Business logic for YouTube data extraction

### Key Components
- **YouTubeTools class**: Static methods for video ID extraction, oEmbed API calls, and transcript processing
- **Configuration system**: Environment-based settings with `.env` file support
- **API Models**: Pydantic v2 models for type safety and validation
- **CORS middleware**: Currently configured for development (allows all origins)

## API Endpoints

The server runs on `localhost:8000` by default:

- **GET /youtube/metadata**: Extract video metadata using YouTube oEmbed API
- **GET /youtube/captions**: Get video transcripts/captions via youtube-transcript-api
- **GET /youtube/timestamps**: Generate timestamped captions
- **GET /health**: Health check endpoint
- **GET /docs**: Swagger/OpenAPI documentation

## Quick Testing Commands

### Local Development (localhost:8000)
```bash
# Health check
curl "http://localhost:8000/health"
# Returns: {"status":"healthy"}

# Video metadata
curl "http://localhost:8000/youtube/metadata?video=dQw4w9WgXcQ"
# Returns: {"title":"Rick Astley - Never Gonna Give You Up...","author_name":"Rick Astley",...}

# Plain text captions
curl "http://localhost:8000/youtube/captions?video=dQw4w9WgXcQ"
# Returns: "[♪♪♪] ♪ We're no strangers to love ♪ ♪ You know the rules and so do I ♪..."

# Timestamped captions
curl "http://localhost:8000/youtube/timestamps?video=dQw4w9WgXcQ"
# Returns: ["0:01 - [♪♪♪]","0:18 - ♪ We're no strangers to love ♪",...]

# With full YouTube URL
curl "http://localhost:8000/youtube/captions?video=https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Production (Railway Deployment)
```bash
# Health check
curl "https://fetch.youtubesummaries.cc/health"

# Video metadata
curl "https://fetch.youtubesummaries.cc/youtube/metadata?video=dQw4w9WgXcQ"

# Captions with language preference
curl "https://fetch.youtubesummaries.cc/youtube/captions?video=dQw4w9WgXcQ&languages=en"

# Test with problematic video (proxy bypass)
curl "https://fetch.youtubesummaries.cc/youtube/captions?video=4v4PJoxm8Bc"
```

### Expected Response Formats
**Metadata Response:**
```json
{
  "title": "Rick Astley - Never Gonna Give You Up (Official Video) (4K Remaster)",
  "author_name": "Rick Astley",
  "author_url": "https://www.youtube.com/@RickAstleyYT",
  "type": "video",
  "height": 113,
  "width": 200,
  "thumbnail_url": "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg"
}
```

**Captions Response:**
```
"[♪♪♪] ♪ We're no strangers to love ♪ ♪ You know the rules and so do I ♪ ♪ A full commitment's what I'm thinking of ♪..."
```

**Timestamps Response:**
```json
[
  "0:01 - [♪♪♪]",
  "0:18 - ♪ We're no strangers to love ♪",
  "0:22 - ♪ You know the rules\nand so do I ♪",
  "0:27 - ♪ A full commitment's\nwhat I'm thinking of ♪"
]
```

**Error Response:**
```json
{
  "detail": "Error getting captions for video: Could not retrieve a transcript..."
}
```

## Technology Stack

- **Framework**: FastAPI with Uvicorn ASGI server
- **Data Validation**: Pydantic v2 for request/response models
- **YouTube Integration**: youtube-transcript-api for transcript extraction
- **HTTP Clients**: httpx and requests for external API calls
- **Configuration**: python-dotenv for environment management
- **Testing**: pytest with asyncio support
- **Containerization**: Docker and Docker Compose
- **Deployment**: Railway (with Nixpacks builder)

## Development Workflow

### Environment Setup
1. Create virtual environment: `python -m venv venv`
2. Activate environment: `source venv/bin/activate` (Unix) or `venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Copy environment template: `cp .env.example .env`
5. Start development server: `python -m app.main`

### Configuration
Environment variables are defined in `.env` file for development or via deployment platform (Railway, etc.):

**Required Environment Variables:**
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000) - automatically set by Railway
- `LOG_LEVEL`: Logging level (default: INFO)
- `PROJECT_NAME`: API title shown in documentation (default: "YouTube Tools API")
- `BACKEND_CORS_ORIGINS`: Allowed CORS origins (use "*" for development, specific domains for production)

**Example for Railway Deployment:**
```
BACKEND_CORS_ORIGINS="*"
DEBUG="false"  
HOST="0.0.0.0"
LOG_LEVEL="INFO"
PORT="8000"
PROJECT_NAME="YouTube API Server"
```

**Proxy Configuration (for bypassing YouTube IP blocks):**
```
# Generic HTTP proxy
PROXY_TYPE=generic
PROXY_URL=http://username:password@proxy-server:port/

# OR Webshare rotating proxies (recommended)
PROXY_TYPE=webshare
WEBSHARE_USERNAME=your_username
WEBSHARE_PASSWORD=your_password
```

**Development .env file:**
```
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
PROJECT_NAME=YouTube Tools API
BACKEND_CORS_ORIGINS=*
```

### Railway Deployment
1. **Connect Repository**: Link your GitHub repository to Railway
2. **Set Environment Variables**: Add the required environment variables in Railway dashboard:
   - `BACKEND_CORS_ORIGINS="*"`
   - `DEBUG="false"`
   - `HOST="0.0.0.0"`
   - `LOG_LEVEL="INFO"`
   - `PROJECT_NAME="YouTube API Server"`
   - Railway automatically sets `PORT`
3. **Deploy**: Railway uses `railway.json` configuration with `python -m app.main` as start command
4. **Access**: Your API will be available at the Railway-provided domain

### Code Organization Patterns
- **Static methods**: YouTubeTools uses static methods for stateless operations
- **Pydantic models**: All API inputs/outputs use typed Pydantic models
- **Router organization**: API routes are organized by domain (youtube.py)
- **Utility separation**: Business logic is separated into utils/ directory
- **Configuration centralization**: All settings managed through core/config.py

## Important Implementation Details

### URL Pattern Handling
The `extract_video_id` method handles multiple YouTube URL formats:
- Standard: `https://www.youtube.com/watch?v=VIDEO_ID`
- Short: `https://youtu.be/VIDEO_ID`
- Embedded: `https://www.youtube.com/embed/VIDEO_ID`
- Mobile: `https://m.youtube.com/watch?v=VIDEO_ID`

### Error Handling
- HTTP exceptions are raised with appropriate status codes
- YouTube API errors are caught and re-raised as HTTP 400 errors
- Missing video data returns structured error responses

### Transcript Processing
- Supports multiple language preferences for captions
- Falls back to auto-generated captions if manual ones unavailable
- Generates formatted timestamps with duration and text content

## Troubleshooting

### Common Issues

**1. "Could not retrieve a transcript" Error**
- **Cause**: YouTube is blocking requests from your IP (common with cloud providers)
- **Solution**: Configure proxy settings in environment variables
- **Test**: Try with a known working video like `dQw4w9WgXcQ` first

**2. "407 Proxy Authentication Required"**
- **Cause**: Proxy credentials are incorrect or improperly formatted
- **Solution**: Verify proxy URL format: `http://username:password@host:port`
- **Check**: Contact proxy provider for correct authentication method

**3. Metadata works but captions fail**
- **Cause**: Metadata uses official YouTube oEmbed API, captions use unofficial methods
- **Solution**: This is expected - proxy is only needed for caption/transcript endpoints
- **Note**: Some videos may not have captions available

**4. Server won't start on Railway**
- **Cause**: Missing required environment variables
- **Solution**: Ensure all required env vars are set in Railway dashboard
- **Check**: Railway logs for specific error messages

### Testing Proxy Configuration
```bash
# Test without proxy (should fail for some videos)
curl "https://fetch.youtubesummaries.cc/youtube/captions?video=4v4PJoxm8Bc"

# Test after adding proxy config (should succeed)
# Add PROXY_TYPE=generic and PROXY_URL in Railway dashboard, then redeploy
curl "https://fetch.youtubesummaries.cc/youtube/captions?video=4v4PJoxm8Bc"
```