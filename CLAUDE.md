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

- **POST /youtube/video-data**: Extract video metadata using YouTube oEmbed API
- **POST /youtube/video-captions**: Get video transcripts/captions via youtube-transcript-api
- **POST /youtube/video-timestamps**: Generate timestamped captions
- **GET /health**: Health check endpoint
- **GET /docs**: Swagger/OpenAPI documentation

## Technology Stack

- **Framework**: FastAPI with Uvicorn ASGI server
- **Data Validation**: Pydantic v2 for request/response models
- **YouTube Integration**: youtube-transcript-api for transcript extraction
- **HTTP Clients**: httpx and requests for external API calls
- **Configuration**: python-dotenv for environment management
- **Testing**: pytest with asyncio support
- **Containerization**: Docker and Docker Compose

## Development Workflow

### Environment Setup
1. Create virtual environment: `python -m venv venv`
2. Activate environment: `source venv/bin/activate` (Unix) or `venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Copy environment template: `cp .env.example .env`
5. Start development server: `python -m app.main`

### Configuration
Environment variables are defined in `.env` file:
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `LOG_LEVEL`: Logging level (default: INFO)

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