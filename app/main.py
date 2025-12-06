from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import app as v1_router
from app.middleware.correlation_id import CorrelationIDMiddleware
from app.core.logging import logger
from app.core.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for application startup and shutdown.
    """
    # Startup
    logger.info("Starting %s", settings.PROJECT_NAME)
    logger.info("Database tables will be created via Alembic migrations")
    
    yield
    
    # Shutdown
    logger.info("Shutting down %s", settings.PROJECT_NAME)
    await engine.dispose()


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DB_ECHO,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add correlation ID middleware (first, before CORS)
app.add_middleware(CorrelationIDMiddleware)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include v1 API routes
app.include_router(v1_router, prefix="/api/v1")


@app.get("/", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app_name": settings.PROJECT_NAME
    }
