# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2024-12-XX

### Added
- **Transcript caching system** with configurable TTL and LRU eviction
  - In-memory cache for YouTube transcripts to reduce API calls
  - Configurable cache settings via environment variables:
    - `CACHE_ENABLED` (default: true)
    - `CACHE_TTL_SECONDS` (default: 3600 = 1 hour)
    - `CACHE_MAX_SIZE` (default: 1000)
  - Cache management endpoints:
    - `GET /youtube/cache/stats` - View cache statistics
    - `DELETE /youtube/cache/clear` - Clear all cached transcripts
- Shared transcript fetching method to avoid duplicate API calls
- Cache statistics endpoint for monitoring cache performance

### Changed
- Refactored transcript fetching to use shared `_fetch_transcript()` method
- Both `get_video_captions()` and `get_video_timestamps()` now share cached transcripts

## [1.0.0] - 2024-12-XX

### Added
- **YouTube API Server** - FastAPI-based server for YouTube data extraction
- **Video Metadata Endpoint** (`GET /youtube/metadata`)
  - Extract video metadata using YouTube's oEmbed API
  - Returns title, author, thumbnail, and other video information
- **Video Captions Endpoint** (`GET /youtube/captions`)
  - Retrieve plain-text captions/transcripts
  - Supports multiple language preferences
  - Defaults to English if not specified
- **Video Timestamps Endpoint** (`GET /youtube/timestamps`)
  - Generate timestamped captions with formatted timestamps
  - Same language support as captions endpoint
- **Query Parameter Support**
  - All endpoints accept video URLs or IDs as query parameters
  - No JSON body required - simple URL paste works
  - Supports multiple YouTube URL formats:
    - Standard: `https://www.youtube.com/watch?v=VIDEO_ID`
    - Short: `https://youtu.be/VIDEO_ID`
    - Embedded: `https://www.youtube.com/embed/VIDEO_ID`
    - Plain video ID: `VIDEO_ID`
- **Proxy Support**
  - Webshare rotating proxy support for bypassing YouTube IP blocks
  - Generic proxy support for custom proxy providers
  - Configurable via environment variables
- **Docker Support**
  - Dockerfile for containerized deployment
  - Docker Compose configuration
- **Railway Deployment**
  - Railway.json configuration
  - Procfile for Railway deployment
  - Environment variable configuration
- **API Documentation**
  - Swagger UI at `/docs`
  - ReDoc at `/redoc`
  - OpenAPI schema generation
- **Health Check Endpoint** (`GET /health`)
- **CORS Middleware** for cross-origin requests
- **Environment Configuration**
  - `.env` file support via python-dotenv
  - `.envrc` for direnv users
  - Comprehensive `.env.example` template
- **Logging Configuration**
  - Configurable log levels
  - Structured logging format

### Documentation
- Comprehensive README.md with usage examples
- AGENTS.md for AI agent guidance
- CLAUDE.md for Claude Code assistance
- PROXY_SETUP.md for proxy configuration
- QUICKSTART.md for quick setup guide

---

## Version History

- **1.1.0** - Added transcript caching system
- **1.0.0** - Initial release with core YouTube API functionality

---

## Future Plans

### Planned Features
- [ ] Rate limiting per IP/user
- [ ] API key authentication
- [ ] Batch video processing
- [ ] Video search functionality
- [ ] Playlist support
- [ ] Webhook notifications
- [ ] Metrics and analytics endpoint
- [ ] Redis cache backend option
- [ ] Database persistence for frequently accessed videos

### Under Consideration
- [ ] GraphQL API endpoint
- [ ] WebSocket support for real-time updates
- [ ] Video download support (metadata only)
- [ ] Channel information endpoints

