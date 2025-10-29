# YouTube API Server

A FastAPI-based server providing API endpoints for extracting and processing YouTube video data, including metadata, captions, and timestamps.

## Features

- Extract video metadata using YouTube's oEmbed API
- Retrieve video captions/transcripts
- Generate timestamped captions
- RESTful API with Swagger/OpenAPI documentation
- Docker support for easy deployment

## Requirements

- Python 3.8+
- FastAPI
- youtube-transcript-api
- Docker (optional)

## Installation

### Using Python

1. Clone the repository:

   ```bash
   git clone https://github.com/chinpeerapat/youtube-api-server.git
   cd youtube-api-server
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file from the example:

   ```bash
   cp .env.example .env
   ```

5. (Optional) Configure proxy settings in `.env` for bypassing YouTube restrictions:

   ```env
   PROXY_TYPE=webshare
   WEBSHARE_USERNAME=your-username
   WEBSHARE_PASSWORD=your-password
   ```

6. Run the server:

   ```bash
   python -m app.main
   ```

### Using Docker

1. Clone the repository:

   ```bash
   git clone https://github.com/chinpeerapat/youtube-api-server.git
   cd youtube-api-server
   ```

2. Build and start the Docker container:

   ```bash
   docker-compose up -d
   ```

## Usage

Once the server is running, you can access:

- API documentation: <http://localhost:8000/docs>
- Alternative API documentation: <http://localhost:8000/redoc>

### API Endpoints

#### 1. Get Video Metadata

```md
POST /youtube/video-data
```

Request body:

```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

Response:

```json
{
  "title": "Video Title",
  "author_name": "Channel Name",
  "author_url": "https://www.youtube.com/channel/...",
  "type": "video",
  "height": 113,
  "width": 200,
  "version": "1.0",
  "provider_name": "YouTube",
  "provider_url": "https://www.youtube.com/",
  "thumbnail_url": "https://i.ytimg.com/vi/..."
}
```

#### 2. Get Video Captions

```md
POST /youtube/video-captions
```

Request body:

```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "languages": ["en"]
}
```

Response:

```md
"Text of the captions..."
```

#### 3. Get Video Timestamps

```md
POST /youtube/video-timestamps
```

Request body:

```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "languages": ["en"]
}
```

Response:

```json
[
  "0:00 - Caption at the beginning",
  "0:05 - Next caption",
  "0:10 - Another caption"
]
```

## Proxy Configuration

The server supports proxy configuration to bypass YouTube API restrictions. Two proxy types are supported:

### Webshare Proxy (Recommended)

Webshare provides rotating residential proxies that work well with YouTube's API:

```env
PROXY_TYPE=webshare
WEBSHARE_USERNAME=your-username
WEBSHARE_PASSWORD=your-password
```

### Generic Proxy

For other proxy providers, use the generic proxy configuration:

```env
PROXY_TYPE=generic
PROXY_URL=http://proxy.example.com:8080
# Or specify separate HTTP/HTTPS proxies:
PROXY_HTTP=http://proxy.example.com:8080
PROXY_HTTPS=https://proxy.example.com:8443
```

## Project Structure

```md
youtube-api-server/
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI application initialization
│   ├── models/                # Pydantic models
│   │   ├── __init__.py
│   │   └── youtube.py
│   ├── routes/                # API routes
│   │   ├── __init__.py
│   │   └── youtube.py
│   └── utils/                 # Utility functions
│       ├── __init__.py
│       └── youtube_tools.py
├── .env.example               # Example environment variables
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
└── docker-compose.yml         # Docker Compose configuration
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
