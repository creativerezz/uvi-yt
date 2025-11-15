# Frontend API Documentation

Complete guide for frontend developers to consume the YouTube API Server.

**Production URL**: `https://fetch.youtubesummaries.cc`

## Table of Contents

- [Quick Start](#quick-start)
- [Authentication](#authentication)
- [CORS Configuration](#cors-configuration)
- [API Endpoints](#api-endpoints)
  - [Get Video Metadata](#1-get-video-metadata)
  - [Get Video Captions](#2-get-video-captions)
  - [Get Video Timestamps](#3-get-video-timestamps)
  - [Cache Statistics](#4-cache-statistics)
  - [Clear Cache](#5-clear-cache)
  - [Service Status](#6-service-status)
  - [Health Check](#7-health-check)
- [Error Handling](#error-handling)
- [Code Examples](#code-examples)
- [TypeScript Types](#typescript-types)
- [Best Practices](#best-practices)

---

## Quick Start

### Base URL

```javascript
const API_BASE_URL = 'https://fetch.youtubesummaries.cc';
```

### Basic Example

```javascript
// Fetch video metadata
const response = await fetch(
  `${API_BASE_URL}/youtube/metadata?video=dQw4w9WgXcQ`
);
const data = await response.json();
console.log(data.title); // "Rick Astley - Never Gonna Give You Up..."
```

---

## Authentication

**No authentication required** - All endpoints are publicly accessible.

---

## CORS Configuration

The API supports CORS and accepts requests from:
- **Development**: All origins (`*`)
- **Production**: Configured domains (check with `/service/status`)

### CORS Headers

The API automatically handles CORS with these headers:
- `Access-Control-Allow-Origin: *` (or configured domains)
- `Access-Control-Allow-Methods: *`
- `Access-Control-Allow-Headers: *`
- `Access-Control-Allow-Credentials: true`

---

## API Endpoints

### 1. Get Video Metadata

Retrieve video information including title, author, thumbnail, and more.

**Endpoint**: `GET /youtube/metadata`

**Query Parameters**:
- `video` (required): YouTube video URL or ID
  - Examples: 
    - `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
    - `https://youtu.be/dQw4w9WgXcQ`
    - `dQw4w9WgXcQ`

**Response** (200 OK):
```json
{
  "title": "Rick Astley - Never Gonna Give You Up (Official Video) (4K Remaster)",
  "author_name": "Rick Astley",
  "author_url": "https://www.youtube.com/@RickAstleyYT",
  "type": "video",
  "height": 113,
  "width": 200,
  "version": "1.0",
  "provider_name": "YouTube",
  "provider_url": "https://www.youtube.com/",
  "thumbnail_url": "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg"
}
```

**JavaScript Example**:
```javascript
async function getVideoMetadata(videoId) {
  try {
    const response = await fetch(
      `https://fetch.youtubesummaries.cc/youtube/metadata?video=${encodeURIComponent(videoId)}`
    );
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching metadata:', error);
    throw error;
  }
}

// Usage
const metadata = await getVideoMetadata('dQw4w9WgXcQ');
console.log(metadata.title);
console.log(metadata.thumbnail_url);
```

---

### 2. Get Video Captions

Get plain-text captions/transcripts for a video.

**Endpoint**: `GET /youtube/captions`

**Query Parameters**:
- `video` (required): YouTube video URL or ID
- `languages` (optional): Array of language codes (ISO 639-1)
  - Default: `["en"]`
  - Examples: `["en"]`, `["en", "es"]`, `["fr"]`

**Response** (200 OK):
```
"[♪♪♪] ♪ We're no strangers to love ♪ ♪ You know the rules and so do I ♪ ♪ A full commitment's what I'm thinking of ♪..."
```

**JavaScript Example**:
```javascript
async function getVideoCaptions(videoId, languages = ['en']) {
  try {
    const params = new URLSearchParams({
      video: videoId,
      languages: languages.join(',')
    });
    
    const response = await fetch(
      `https://fetch.youtubesummaries.cc/youtube/captions?${params}`
    );
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }
    
    const captions = await response.text();
    return captions;
  } catch (error) {
    console.error('Error fetching captions:', error);
    throw error;
  }
}

// Usage
const captions = await getVideoCaptions('dQw4w9WgXcQ');
console.log(captions);

// With multiple languages (fallback)
const captionsMulti = await getVideoCaptions('dQw4w9WgXcQ', ['en', 'es']);
```

**Note**: The response is plain text, not JSON. Use `.text()` instead of `.json()`.

---

### 3. Get Video Timestamps

Get captions with formatted timestamps.

**Endpoint**: `GET /youtube/timestamps`

**Query Parameters**:
- `video` (required): YouTube video URL or ID
- `languages` (optional): Array of language codes (ISO 639-1)
  - Default: `["en"]`

**Response** (200 OK):
```json
[
  "0:01 - [♪♪♪]",
  "0:18 - ♪ We're no strangers to love ♪",
  "0:22 - ♪ You know the rules\nand so do I ♪",
  "0:27 - ♪ A full commitment's\nwhat I'm thinking of ♪"
]
```

**JavaScript Example**:
```javascript
async function getVideoTimestamps(videoId, languages = ['en']) {
  try {
    const params = new URLSearchParams({
      video: videoId,
      languages: languages.join(',')
    });
    
    const response = await fetch(
      `https://fetch.youtubesummaries.cc/youtube/timestamps?${params}`
    );
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }
    
    const timestamps = await response.json();
    return timestamps;
  } catch (error) {
    console.error('Error fetching timestamps:', error);
    throw error;
  }
}

// Usage
const timestamps = await getVideoTimestamps('dQw4w9WgXcQ');
timestamps.forEach(entry => {
  console.log(entry); // "0:01 - [♪♪♪]"
});
```

---

### 4. Cache Statistics

Get current cache statistics and configuration.

**Endpoint**: `GET /youtube/cache/stats`

**Response** (200 OK):
```json
{
  "enabled": true,
  "size": 42,
  "max_size": 1000,
  "ttl_seconds": 3600
}
```

**JavaScript Example**:
```javascript
async function getCacheStats() {
  const response = await fetch(
    'https://fetch.youtubesummaries.cc/youtube/cache/stats'
  );
  return await response.json();
}

const stats = await getCacheStats();
console.log(`Cache: ${stats.size}/${stats.max_size} entries`);
```

---

### 5. Clear Cache

Clear all cached transcripts (admin/utility endpoint).

**Endpoint**: `DELETE /youtube/cache/clear`

**Response** (200 OK):
```json
{
  "message": "Cache cleared successfully",
  "size": 0
}
```

**JavaScript Example**:
```javascript
async function clearCache() {
  const response = await fetch(
    'https://fetch.youtubesummaries.cc/youtube/cache/clear',
    { method: 'DELETE' }
  );
  return await response.json();
}
```

---

### 6. Performance Test

Test transcript fetching performance (cache miss vs cache hit).

**Endpoint**: `GET /youtube/performance/test`

**Query Parameters**:
- `video` (required): YouTube video URL or ID
- `runs` (optional): Number of test runs (2-10, default: 3)
- `languages` (optional): Array of language codes

**Response** (200 OK):
```json
{
  "video_id": "dQw4w9WgXcQ",
  "runs": 5,
  "successful_runs": 5,
  "cache_miss": {
    "time_seconds": 2.345,
    "time_ms": 2345.0
  },
  "cache_hits": {
    "count": 4,
    "times_seconds": [0.012, 0.011, 0.013, 0.012],
    "times_ms": [12.0, 11.0, 13.0, 12.0],
    "avg_seconds": 0.012,
    "avg_ms": 12.0,
    "min_seconds": 0.011,
    "max_seconds": 0.013
  },
  "speedup": 195.42
}
```

**JavaScript Example**:
```javascript
async function testPerformance(videoId, runs = 5) {
  const params = new URLSearchParams({
    video: videoId,
    runs: runs.toString()
  });
  
  const response = await fetch(
    `https://fetch.youtubesummaries.cc/youtube/performance/test?${params}`
  );
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || `HTTP error! status: ${response.status}`);
  }
  
  return await response.json();
}

// Usage
const perf = await testPerformance('dQw4w9WgXcQ', 5);
console.log(`Cache miss: ${perf.cache_miss.time_ms}ms`);
console.log(`Cache hit avg: ${perf.cache_hits.avg_ms}ms`);
console.log(`Speedup: ${perf.speedup.toFixed(2)}x faster`);
```

---

### 7. Service Status

Get comprehensive service status and configuration.

**Endpoint**: `GET /service/status`

**Response** (200 OK):
```json
{
  "status": "operational",
  "version": "1.1.0",
  "timestamp": "2024-12-XXT12:00:00Z",
  "service": {
    "name": "YouTube API Server",
    "host": "0.0.0.0",
    "port": 8000,
    "log_level": "INFO"
  },
  "features": {
    "proxy_enabled": true,
    "proxy_type": "webshare",
    "cache_enabled": true,
    "cache_size": 42,
    "cache_max_size": 1000,
    "cache_ttl_seconds": 3600
  },
  "endpoints": {
    "metadata": "/youtube/metadata",
    "captions": "/youtube/captions",
    "timestamps": "/youtube/timestamps",
    "cache_stats": "/youtube/cache/stats",
    "cache_clear": "/youtube/cache/clear",
    "health": "/health",
    "docs": "/docs",
    "redoc": "/redoc"
  },
  "cors": {
    "enabled": true,
    "allowed_origins": ["*"]
  }
}
```

---

### 8. Health Check

Simple health check endpoint.

**Endpoint**: `GET /health`

**Response** (200 OK):
```json
{
  "status": "healthy"
}
```

---

## Error Handling

### Error Response Format

All errors return JSON with a `detail` field:

```json
{
  "detail": "Error message here"
}
```

### HTTP Status Codes

- `200 OK` - Success
- `400 Bad Request` - Invalid request (missing parameters, invalid video ID)
- `500 Internal Server Error` - Server error (transcript unavailable, API error)

### Error Handling Example

```javascript
async function safeApiCall(url) {
  try {
    const response = await fetch(url);
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `HTTP ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    // Handle network errors
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      throw new Error('Network error: Unable to reach API');
    }
    
    // Handle API errors
    throw error;
  }
}

// Usage with error handling
try {
  const metadata = await safeApiCall(
    'https://fetch.youtubesummaries.cc/youtube/metadata?video=invalid'
  );
} catch (error) {
  console.error('API Error:', error.message);
  // Show user-friendly error message
  alert(`Failed to fetch video: ${error.message}`);
}
```

---

## Code Examples

### React Hook Example

```javascript
import { useState, useEffect } from 'react';

function useYouTubeMetadata(videoId) {
  const [metadata, setMetadata] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!videoId) return;

    const fetchMetadata = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const response = await fetch(
          `https://fetch.youtubesummaries.cc/youtube/metadata?video=${encodeURIComponent(videoId)}`
        );
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Failed to fetch metadata');
        }
        
        const data = await response.json();
        setMetadata(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchMetadata();
  }, [videoId]);

  return { metadata, loading, error };
}

// Usage in component
function VideoInfo({ videoId }) {
  const { metadata, loading, error } = useYouTubeMetadata(videoId);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!metadata) return null;

  return (
    <div>
      <h2>{metadata.title}</h2>
      <p>By: {metadata.author_name}</p>
      <img src={metadata.thumbnail_url} alt={metadata.title} />
    </div>
  );
}
```

### Vue.js Composable Example

```javascript
import { ref, watch } from 'vue';

export function useYouTubeCaptions(videoId, languages = ['en']) {
  const captions = ref('');
  const loading = ref(false);
  const error = ref(null);

  const fetchCaptions = async () => {
    if (!videoId.value) return;

    loading.value = true;
    error.value = null;

    try {
      const params = new URLSearchParams({
        video: videoId.value,
        languages: languages.value.join(',')
      });

      const response = await fetch(
        `https://fetch.youtubesummaries.cc/youtube/captions?${params}`
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to fetch captions');
      }

      captions.value = await response.text();
    } catch (err) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  };

  watch([videoId, languages], fetchCaptions, { immediate: true });

  return { captions, loading, error, refetch: fetchCaptions };
}
```

### Vanilla JavaScript Class Example

```javascript
class YouTubeAPI {
  constructor(baseURL = 'https://fetch.youtubesummaries.cc') {
    this.baseURL = baseURL;
  }

  async request(endpoint, options = {}) {
    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || `HTTP ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  async getMetadata(videoId) {
    return this.request(`/youtube/metadata?video=${encodeURIComponent(videoId)}`);
  }

  async getCaptions(videoId, languages = ['en']) {
    const params = new URLSearchParams({
      video: videoId,
      languages: languages.join(',')
    });
    const response = await fetch(`${this.baseURL}/youtube/captions?${params}`);
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `HTTP ${response.status}`);
    }
    return await response.text();
  }

  async getTimestamps(videoId, languages = ['en']) {
    const params = new URLSearchParams({
      video: videoId,
      languages: languages.join(',')
    });
    return this.request(`/youtube/timestamps?${params}`);
  }

  async getCacheStats() {
    return this.request('/youtube/cache/stats');
  }

  async clearCache() {
    return this.request('/youtube/cache/clear', { method: 'DELETE' });
  }

  async getServiceStatus() {
    return this.request('/service/status');
  }

  async healthCheck() {
    return this.request('/health');
  }
}

// Usage
const api = new YouTubeAPI();
const metadata = await api.getMetadata('dQw4w9WgXcQ');
const captions = await api.getCaptions('dQw4w9WgXcQ');
```

---

## TypeScript Types

```typescript
// API Types
interface VideoMetadata {
  title: string;
  author_name: string;
  author_url: string;
  type: string;
  height: number;
  width: number;
  version?: string;
  provider_name?: string;
  provider_url?: string;
  thumbnail_url: string;
}

interface CacheStats {
  enabled: boolean;
  size: number;
  max_size: number;
  ttl_seconds: number;
}

interface ServiceStatus {
  status: 'operational' | 'degraded' | 'down';
  version: string;
  timestamp: string;
  service: {
    name: string;
    host: string;
    port: number;
    log_level: string;
  };
  features: {
    proxy_enabled: boolean;
    proxy_type: string;
    cache_enabled: boolean;
    cache_size: number;
    cache_max_size: number;
    cache_ttl_seconds: number;
  };
  endpoints: Record<string, string>;
  cors: {
    enabled: boolean;
    allowed_origins: string[] | string;
  };
}

interface APIError {
  detail: string;
}

// Usage with typed API client
class YouTubeAPIClient {
  private baseURL: string;

  constructor(baseURL = 'https://fetch.youtubesummaries.cc') {
    this.baseURL = baseURL;
  }

  async getMetadata(videoId: string): Promise<VideoMetadata> {
    const response = await fetch(
      `${this.baseURL}/youtube/metadata?video=${encodeURIComponent(videoId)}`
    );
    if (!response.ok) {
      const error: APIError = await response.json();
      throw new Error(error.detail);
    }
    return response.json();
  }

  async getCaptions(videoId: string, languages: string[] = ['en']): Promise<string> {
    const params = new URLSearchParams({
      video: videoId,
      languages: languages.join(',')
    });
    const response = await fetch(`${this.baseURL}/youtube/captions?${params}`);
    if (!response.ok) {
      const error: APIError = await response.json();
      throw new Error(error.detail);
    }
    return response.text();
  }

  async getTimestamps(videoId: string, languages: string[] = ['en']): Promise<string[]> {
    const params = new URLSearchParams({
      video: videoId,
      languages: languages.join(',')
    });
    const response = await fetch(`${this.baseURL}/youtube/timestamps?${params}`);
    if (!response.ok) {
      const error: APIError = await response.json();
      throw new Error(error.detail);
    }
    return response.json();
  }

  async getCacheStats(): Promise<CacheStats> {
    const response = await fetch(`${this.baseURL}/youtube/cache/stats`);
    return response.json();
  }

  async getServiceStatus(): Promise<ServiceStatus> {
    const response = await fetch(`${this.baseURL}/service/status`);
    return response.json();
  }
}
```

---

## Best Practices

### 1. URL Encoding

Always encode video IDs/URLs:

```javascript
// ✅ Good
const videoId = encodeURIComponent('dQw4w9WgXcQ');
const url = `https://fetch.youtubesummaries.cc/youtube/metadata?video=${videoId}`;

// ❌ Bad
const url = `https://fetch.youtubesummaries.cc/youtube/metadata?video=dQw4w9WgXcQ`;
```

### 2. Error Handling

Always handle errors gracefully:

```javascript
try {
  const data = await fetch(url);
  // Handle success
} catch (error) {
  // Log error
  console.error('API Error:', error);
  // Show user-friendly message
  showError('Unable to fetch video data. Please try again.');
}
```

### 3. Loading States

Show loading indicators:

```javascript
const [loading, setLoading] = useState(false);

async function fetchData() {
  setLoading(true);
  try {
    const data = await api.getMetadata(videoId);
    // Handle data
  } finally {
    setLoading(false);
  }
}
```

### 4. Caching

The API already caches transcripts, but you can cache metadata client-side:

```javascript
const cache = new Map();

async function getMetadataCached(videoId) {
  if (cache.has(videoId)) {
    return cache.get(videoId);
  }
  
  const metadata = await api.getMetadata(videoId);
  cache.set(videoId, metadata);
  return metadata;
}
```

### 5. Rate Limiting

While the API doesn't enforce rate limits, be respectful:

```javascript
// Debounce rapid requests
import { debounce } from 'lodash';

const debouncedFetch = debounce(async (videoId) => {
  return await api.getMetadata(videoId);
}, 300);
```

### 6. Video ID Extraction

Extract video ID from various YouTube URL formats:

```javascript
function extractVideoId(urlOrId) {
  // If it's already an ID (11 characters)
  if (/^[a-zA-Z0-9_-]{11}$/.test(urlOrId)) {
    return urlOrId;
  }
  
  // Extract from URL
  const patterns = [
    /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)/,
    /youtube\.com\/v\/([^&\n?#]+)/
  ];
  
  for (const pattern of patterns) {
    const match = urlOrId.match(pattern);
    if (match) return match[1];
  }
  
  return null;
}

// Usage
const videoId = extractVideoId('https://youtu.be/dQw4w9WgXcQ');
// Returns: 'dQw4w9WgXcQ'
```

### 7. Language Fallback

Handle language preferences with fallback:

```javascript
async function getCaptionsWithFallback(videoId, preferredLanguages = ['en']) {
  try {
    return await api.getCaptions(videoId, preferredLanguages);
  } catch (error) {
    // Try English as fallback
    if (!preferredLanguages.includes('en')) {
      return await api.getCaptions(videoId, ['en']);
    }
    throw error;
  }
}
```

---

## Testing

### Test API Connection

```javascript
async function testConnection() {
  try {
    const status = await fetch('https://fetch.youtubesummaries.cc/health');
    const data = await status.json();
    console.log('API Status:', data.status); // "healthy"
    return true;
  } catch (error) {
    console.error('API unavailable:', error);
    return false;
  }
}
```

### Test with Sample Video

```javascript
// Test with a known video
const testVideoId = 'dQw4w9WgXcQ'; // Rick Astley - Never Gonna Give You Up

async function testAPI() {
  console.log('Testing metadata...');
  const metadata = await api.getMetadata(testVideoId);
  console.log('Title:', metadata.title);
  
  console.log('Testing captions...');
  const captions = await api.getCaptions(testVideoId);
  console.log('Captions length:', captions.length);
  
  console.log('Testing timestamps...');
  const timestamps = await api.getTimestamps(testVideoId);
  console.log('Timestamps count:', timestamps.length);
}
```

### Performance Testing

Test transcript fetching speed and cache effectiveness:

```javascript
async function testPerformance(videoId) {
  console.log(`Testing performance for video: ${videoId}`);
  
  const perf = await testPerformance(videoId, 5);
  
  console.log('Performance Results:');
  console.log(`  Cache Miss (first request): ${perf.cache_miss.time_ms.toFixed(2)}ms`);
  console.log(`  Cache Hit (avg): ${perf.cache_hits.avg_ms.toFixed(2)}ms`);
  console.log(`  Speedup: ${perf.speedup.toFixed(2)}x faster`);
  console.log(`  Successful runs: ${perf.successful_runs}/${perf.runs}`);
  
  return perf;
}

// Test performance
const perf = await testPerformance('dQw4w9WgXcQ');
```

**Performance Test Script**: For server-side testing, use the included `test_transcript_speed.py` script:

```bash
# Test local server
python test_transcript_speed.py

# Test production server
python test_transcript_speed.py https://fetch.youtubesummaries.cc

# Test specific videos
python test_transcript_speed.py http://localhost:8000 dQw4w9WgXcQ,jNQXAC9IVRw 5
```

---

## Support

- **API Documentation**: `https://fetch.youtubesummaries.cc/docs`
- **Service Status**: `https://fetch.youtubesummaries.cc/service/info`
- **GitHub**: `https://github.com/creativerezz`

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for API version history and updates.

