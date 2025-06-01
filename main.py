#!/usr/bin/env python
"""
Main entry point for InfluencerFlow API.
Run directly with: uv run main.py
"""

import os
import uvicorn

def main():
    """Run the FastAPI application using uvicorn."""
    # Default to development environment if not specified
    env = os.environ.get("ENVIRONMENT", "development")
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))
    
    reload_mode = env != "production"
    
    print(f"Starting InfluencerFlow API in {env} environment")
    print(f"Running on http://{host}:{port}")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload_mode,
        log_level="info"
    )

if __name__ == "__main__":
    main() 