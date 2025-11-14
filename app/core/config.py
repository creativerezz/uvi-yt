import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """
    Application settings
    
    Reads settings from environment variables or .env file
    """
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "YouTube Tools API"
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # CORS settings - add specific origins in production
    # Parse comma-separated origins from environment variable
    BACKEND_CORS_ORIGINS: list = (
        [origin.strip() for origin in os.getenv("BACKEND_CORS_ORIGINS", "*").split(",")]
        if os.getenv("BACKEND_CORS_ORIGINS")
        else ["*"]
    )
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Proxy settings for YouTube API (to work around IP blocking)
    PROXY_TYPE: str = os.getenv("PROXY_TYPE", "")  # "generic" or "webshare"
    PROXY_URL: str = os.getenv("PROXY_URL", "")  # For generic proxies
    PROXY_HTTP: str = os.getenv("PROXY_HTTP", "")
    PROXY_HTTPS: str = os.getenv("PROXY_HTTPS", "") 
    WEBSHARE_USERNAME: str = os.getenv("WEBSHARE_USERNAME", "")
    WEBSHARE_PASSWORD: str = os.getenv("WEBSHARE_PASSWORD", "")
    
    # Cache settings for transcripts
    CACHE_ENABLED: bool = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "3600"))  # Default: 1 hour
    CACHE_MAX_SIZE: int = int(os.getenv("CACHE_MAX_SIZE", "1000"))  # Maximum number of cached transcripts

# Create settings instance
settings = Settings()