from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.router import api_router

# Create FastAPI app
app = FastAPI(
    title="InfluencerFlow AI Platform API",
    description="Backend API for InfluencerFlow AI Platform",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to InfluencerFlow AI Platform API",
        "docs": "/docs",
        "version": "0.1.0",
    }

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# Startup event
@app.on_event("startup")
async def startup_event():
    # Initialize services, connect to DB, etc.
    print("Starting InfluencerFlow API...")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    # Close connections, clean up resources
    print("Shutting down InfluencerFlow API...")
