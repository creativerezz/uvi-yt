# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Critical Non-Obvious Information

- **Proxy bypass required for YouTube caption/transcript endpoints**: YouTubeTranscriptApi uses unofficial methods that are IP-blocked for cloud providers. Configure proxy settings in environment variables (PROXY_TYPE=webshare, WEBSHARE_USERNAME, WEBSHARE_PASSWORD) or caption endpoints will fail silently.
- **Metadata endpoint works without proxy**: /youtube/metadata uses official YouTube oEmbed API and works from any IP, but /youtube/captions and /youtube/timestamps require proxy configuration to avoid "Could not retrieve a transcript" errors.
- **Query parameters over JSON**: All YouTube endpoints accept video URLs/IDs directly as query parameters (e.g., ?video=dQw4w9WgXcQ) instead of JSON bodies - no Content-Type header needed.
- **Console script entry point**: After package installation, run via `youtube-api-server` command (defined in setup.py console_scripts).
- **Test directory configuration**: Tests must be placed in root-level `tests/` directory (pytest.ini specifies testpaths = tests), not alongside source files.
- **Webshare proxy configuration**: Use rotating proxies with PROXY_TYPE=webshare and credentials - generic proxy URLs also supported via PROXY_HTTP/PROXY_HTTPS or PROXY_URL.
- **Environment variable parsing**: BACKEND_CORS_ORIGINS supports comma-separated domains or "*" for development; parsed via split(",") with strip().
- **Railway deployment**: Uses Procfile with `web: python -m app.main` - PORT automatically set by Railway, HOST must be 0.0.0.0.

## Testing Commands

- Run single test: `pytest tests/test_file.py::test_function_name -v`
- Run tests with coverage: `pytest --cov=app --cov-report=html`
- Run proxy test script: `python test_proxy.py`