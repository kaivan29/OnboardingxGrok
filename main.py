"""
FastAPI Application Entry Point
================================

Purpose:
    This is the main entry point for the Grok Code Tutorial Backend API. It initializes
    the FastAPI application, configures CORS middleware for frontend integration, and
    registers all API routes.

Key Responsibilities:
    - Initialize FastAPI application with metadata
    - Configure CORS middleware to allow frontend requests
    - Register API routes from api/routes.py
    - Provide root endpoint with API information
    - Run the development server when executed directly

Usage:
    Run directly: python main.py
    Or with uvicorn: uvicorn main:app --host 0.0.0.0 --port 8000

Endpoints:
    - GET / : Root endpoint with API info
    - GET /health : Health check (from api/routes.py)
    - POST /api/analyze : Main analysis endpoint (from api/routes.py)
    - GET /docs : Auto-generated API documentation
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import Config
from api.routes import router

# Create FastAPI app
app = FastAPI(
    title=Config.API_TITLE,
    version=Config.API_VERSION,
    description="Backend API for generating codebase tutorials using Grok Code API"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Grok Code Tutorial Backend API",
        "version": Config.API_VERSION,
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

