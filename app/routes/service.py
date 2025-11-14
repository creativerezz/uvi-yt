"""
Service status and information endpoints.
"""
from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.core.config import settings
from app.utils.transcript_cache import get_cache

router = APIRouter(
    prefix="/service",
    tags=["service"],
    responses={404: {"description": "Not found"}},
)


@router.get("/status", summary="Service status")
async def service_status() -> Dict[str, Any]:
    """
    Get comprehensive service status and configuration information.
    
    Returns:
        Dictionary containing service status, version, configuration, and cache stats
    """
    cache = get_cache()
    
    return {
        "status": "operational",
        "version": "1.1.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service": {
            "name": settings.PROJECT_NAME,
            "host": settings.HOST,
            "port": settings.PORT,
            "log_level": settings.LOG_LEVEL,
        },
        "features": {
            "proxy_enabled": bool(settings.PROXY_TYPE),
            "proxy_type": settings.PROXY_TYPE or "none",
            "cache_enabled": cache.enabled,
            "cache_size": cache.size(),
            "cache_max_size": cache.max_size,
            "cache_ttl_seconds": cache.ttl_seconds,
        },
        "endpoints": {
            "metadata": "/youtube/metadata",
            "captions": "/youtube/captions",
            "timestamps": "/youtube/timestamps",
            "cache_stats": "/youtube/cache/stats",
            "cache_clear": "/youtube/cache/clear",
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc",
        },
        "cors": {
            "enabled": True,
            "allowed_origins": settings.BACKEND_CORS_ORIGINS,
        },
    }


@router.get("/info", summary="Service information page", response_class=HTMLResponse)
async def service_info() -> str:
    """
    Get an HTML service information page.
    
    Returns:
        HTML page with service information, status, and links
    """
    cache = get_cache()
    status_data = await service_status()
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{settings.PROJECT_NAME} - Service Status</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
                color: #333;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 12px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }}
            .header h1 {{
                font-size: 2.5em;
                margin-bottom: 10px;
            }}
            .header p {{
                font-size: 1.2em;
                opacity: 0.9;
            }}
            .status-badge {{
                display: inline-block;
                background: #10b981;
                color: white;
                padding: 8px 16px;
                border-radius: 20px;
                font-weight: bold;
                margin-top: 15px;
                font-size: 0.9em;
            }}
            .content {{
                padding: 40px;
            }}
            .section {{
                margin-bottom: 40px;
            }}
            .section h2 {{
                color: #667eea;
                font-size: 1.8em;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 2px solid #e5e7eb;
            }}
            .info-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }}
            .info-card {{
                background: #f9fafb;
                padding: 20px;
                border-radius: 8px;
                border-left: 4px solid #667eea;
            }}
            .info-card h3 {{
                color: #667eea;
                margin-bottom: 10px;
                font-size: 1.1em;
            }}
            .info-card p {{
                color: #6b7280;
                margin: 5px 0;
            }}
            .endpoint-list {{
                list-style: none;
                margin-top: 15px;
            }}
            .endpoint-list li {{
                padding: 12px;
                margin: 8px 0;
                background: #f9fafb;
                border-radius: 6px;
                border-left: 3px solid #667eea;
            }}
            .endpoint-list li strong {{
                color: #667eea;
                font-family: 'Courier New', monospace;
            }}
            .endpoint-list li code {{
                background: #e5e7eb;
                padding: 2px 6px;
                border-radius: 3px;
                font-size: 0.9em;
            }}
            .footer {{
                background: #f9fafb;
                padding: 30px;
                text-align: center;
                color: #6b7280;
                border-top: 1px solid #e5e7eb;
            }}
            .footer a {{
                color: #667eea;
                text-decoration: none;
            }}
            .footer a:hover {{
                text-decoration: underline;
            }}
            .badge {{
                display: inline-block;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 0.8em;
                font-weight: bold;
                margin-left: 8px;
            }}
            .badge-success {{
                background: #d1fae5;
                color: #065f46;
            }}
            .badge-info {{
                background: #dbeafe;
                color: #1e40af;
            }}
            .badge-warning {{
                background: #fef3c7;
                color: #92400e;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{settings.PROJECT_NAME}</h1>
                <p>YouTube API Server - Service Information</p>
                <div class="status-badge">✓ Operational</div>
            </div>
            
            <div class="content">
                <div class="section">
                    <h2>Service Information</h2>
                    <div class="info-grid">
                        <div class="info-card">
                            <h3>Version</h3>
                            <p><strong>{status_data['version']}</strong></p>
                        </div>
                        <div class="info-card">
                            <h3>Status</h3>
                            <p><strong>{status_data['status'].title()}</strong></p>
                        </div>
                        <div class="info-card">
                            <h3>Host</h3>
                            <p><code>{status_data['service']['host']}:{status_data['service']['port']}</code></p>
                        </div>
                        <div class="info-card">
                            <h3>Log Level</h3>
                            <p><strong>{status_data['service']['log_level']}</strong></p>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>Features & Configuration</h2>
                    <div class="info-grid">
                        <div class="info-card">
                            <h3>Proxy</h3>
                            <p>Type: <strong>{status_data['features']['proxy_type'].title()}</strong></p>
                            <p>Status: <span class="badge {'badge-success' if status_data['features']['proxy_enabled'] else 'badge-warning'}">
                                {'Enabled' if status_data['features']['proxy_enabled'] else 'Disabled'}
                            </span></p>
                        </div>
                        <div class="info-card">
                            <h3>Cache</h3>
                            <p>Status: <span class="badge {'badge-success' if status_data['features']['cache_enabled'] else 'badge-warning'}">
                                {'Enabled' if status_data['features']['cache_enabled'] else 'Disabled'}
                            </span></p>
                            <p>Size: <strong>{status_data['features']['cache_size']}</strong> / {status_data['features']['cache_max_size']}</p>
                            <p>TTL: <strong>{status_data['features']['cache_ttl_seconds']}s</strong></p>
                        </div>
                        <div class="info-card">
                            <h3>CORS</h3>
                            <p>Status: <span class="badge badge-success">Enabled</span></p>
                            <p>Origins: <code>{', '.join(status_data['cors']['allowed_origins']) if isinstance(status_data['cors']['allowed_origins'], list) else status_data['cors']['allowed_origins']}</code></p>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>API Endpoints</h2>
                    <ul class="endpoint-list">
                        <li>
                            <strong>GET</strong> <code>{status_data['endpoints']['metadata']}</code>
                            <br>Get video metadata (title, author, thumbnail)
                        </li>
                        <li>
                            <strong>GET</strong> <code>{status_data['endpoints']['captions']}</code>
                            <br>Get plain-text captions/transcripts
                        </li>
                        <li>
                            <strong>GET</strong> <code>{status_data['endpoints']['timestamps']}</code>
                            <br>Get timestamped captions
                        </li>
                        <li>
                            <strong>GET</strong> <code>{status_data['endpoints']['cache_stats']}</code>
                            <br>View cache statistics
                        </li>
                        <li>
                            <strong>DELETE</strong> <code>{status_data['endpoints']['cache_clear']}</code>
                            <br>Clear transcript cache
                        </li>
                        <li>
                            <strong>GET</strong> <code>{status_data['endpoints']['health']}</code>
                            <br>Health check endpoint
                        </li>
                        <li>
                            <strong>GET</strong> <code>{status_data['endpoints']['docs']}</code>
                            <br>Swagger API documentation
                        </li>
                        <li>
                            <strong>GET</strong> <code>{status_data['endpoints']['redoc']}</code>
                            <br>ReDoc API documentation
                        </li>
                    </ul>
                </div>
            </div>
            
            <div class="footer">
                <p>Last updated: {status_data['timestamp']}</p>
                <p>
                    <a href="/docs">API Documentation</a> | 
                    <a href="/service/status">JSON Status</a> | 
                    <a href="/health">Health Check</a>
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content

