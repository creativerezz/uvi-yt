import logging

from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routes.youtube import router as youtube_router
from app.routes.service import router as service_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Enrich Swagger-UI with nicer defaults
swagger_ui_parameters = {
    "docExpansion": "none",  # collapse routes by default
    "defaultModelsExpandDepth": -1,  # hide schemas section unless expanded
}

# Custom API metadata (will be visible in /docs)
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Easily fetch YouTube metadata, captions and timestamps. Paste **any** video URL or 11-character ID – no extra JSON required!",
    version="1.0.0",
    contact={
        "name": "YouTube Tools API",
        "url": "https://github.com/chinpeerapat/youtube-api-server",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    swagger_ui_parameters=swagger_ui_parameters,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(youtube_router)
app.include_router(service_router)

@app.get("/", tags=["root"])
async def root():
    """Root endpoint that provides API information"""
    return {
        "message": f"Welcome to the {settings.PROJECT_NAME}",
        "version": "1.1.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "service": "/service/info",
        "status": "/service/status",
        "health": "/health"
    }

@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

def start():
    """Function to start the server"""
    logger.info(f"Starting server on {settings.HOST}:{settings.PORT}")
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)

if __name__ == "__main__":
    start()