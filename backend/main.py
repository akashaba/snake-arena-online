"""Neon Snake Arena - FastAPI Backend"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import (
    auth_router,
    leaderboard_router,
    spectate_router,
    users_router,
)

# Create FastAPI app
app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    description="Backend API for Neon Snake Arena Online game",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix=settings.api_v1_prefix)
app.include_router(leaderboard_router, prefix=settings.api_v1_prefix)
app.include_router(spectate_router, prefix=settings.api_v1_prefix)
app.include_router(users_router, prefix=settings.api_v1_prefix)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Neon Snake Arena API",
        "version": settings.version,
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
