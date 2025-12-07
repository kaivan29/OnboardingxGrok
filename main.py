"""
FastAPI Application Entry Point
================================

Purpose:
    Unified FastAPI application combining:
    1. Codebase analysis and tutorial generation (from teammate)
    2. Resume analysis for personalized onboarding (your implementation)

Key Responsibilities:
    - Initialize FastAPI application with metadata
    - Configure CORS middleware for frontend integration
    - Register codebase analysis routes from api/routes.py
    - Register resume analysis endpoints
    - Provide root endpoint with API information
    - Run the development server when executed directly

Usage:
    Run directly: python main.py
    Or with uvicorn: uvicorn main:app --host 0.0.0.0 --port 8080

Endpoints:
    - GET / : Root endpoint with API info
    - GET /health : Health check (from api/routes.py)
    - POST /api/analyze : Codebase analysis endpoint (from api/routes.py)
    - POST /api/analyzeResume : Resume analysis endpoint
    - GET /api/getProfile/{profile_id} : Get analyzed profile
    - GET /api/getCodeBaseSummary : Legacy codebase summary (mock data)
    - GET /docs : Auto-generated API documentation
"""
import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PyPDF2 import PdfReader
from openai import OpenAI

from config import Config

# Try to import codebase analysis router (teammate's code)
try:
    from api.routes import router
    HAS_CODEBASE_ANALYSIS = True
except Exception as e:
    HAS_CODEBASE_ANALYSIS = False
    print(f"Warning: Codebase analysis features disabled due to import error: {e}")

# Configuration
UPLOAD_FOLDER = Path("data/resumes")
ANALYZED_FOLDER = Path("data/analyzed_profiles")
ALLOWED_EXTENSIONS = {"pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Ensure directories exist
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
ANALYZED_FOLDER.mkdir(parents=True, exist_ok=True)

# Initialize Grok client for resume analysis
grok_client = OpenAI(
    api_key=Config.XAI_API_KEY,
    base_url=Config.XAI_BASE_URL
)

# Create FastAPI app
app = FastAPI(
    title="Onboarding-x-Grok API",
    version="2.0.0",
    description="Unified API for codebase analysis and personalized engineer onboarding"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and initialize background scheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.codebase_scheduler import scheduler_instance, scheduled_analysis_job
from config_repos import ANALYSIS_SCHEDULE

# Create scheduler
scheduler = AsyncIOScheduler()

# Schedule periodic analysis job (daily at 2 AM by default)
scheduler.add_job(
    scheduled_analysis_job,
    'cron',
    hour=ANALYSIS_SCHEDULE.get("hour", 2),
    minute=ANALYSIS_SCHEDULE.get("minute", 0),
    id='codebase_analysis_job'
)

# Startup event to start scheduler
@app.on_event("startup")
async def startup_event():
    """Start the background scheduler when the app starts."""
    scheduler.start()
    print("✅ Background scheduler started - codebase analysis will run daily")
    # Run once on startup for testing (comment out in production)
    print("🔄 Running initial codebase analysis...")
    await scheduled_analysis_job()

# Shutdown event to stop scheduler
@app.on_event("shutdown")
async def shutdown_event():
    """Stop the background scheduler when the app shuts down."""
    scheduler.shutdown()
    print("🛑 Background scheduler stopped")

# Include codebase analysis router from teammate (if available)
if HAS_CODEBASE_ANALYSIS:
    app.include_router(router)


# Helper functions for resume analysis
def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text content from a PDF file."""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")


async def analyze_resume_with_grok(resume_text: str) -> dict:
    """
    Analyze resume using Grok API to extract CS background and experience.
    Returns a structured JSON with the candidate's profile.
    """
    # Prompt for Grok to analyze the resume
    prompt = f"""Analyze the following resume and extract key information about the candidate's computer science background and experience.

Resume:
{resume_text}

Please provide a detailed analysis in the following JSON format:
{{
    "candidate_name": "string - candidate's name",
    "experience_years": "number - total years of professional experience",
    "education": [
        {{
            "degree": "string",
            "institution": "string",
            "graduation_year": "number"
        }}
    ],
    "technical_skills": {{
        "languages": ["list of programming languages"],
        "frameworks": ["list of frameworks"],
        "tools": ["list of tools and technologies"],
        "databases": ["list of database technologies"]
    }},
    "experience_summary": [
        {{
            "role": "string",
            "company": "string",
            "duration": "string",
            "technologies": ["list of technologies used"],
            "key_achievements": ["list of notable achievements"]
        }}
    ],
    "strengths": ["list of technical strengths based on experience"],
    "knowledge_gaps": ["areas where candidate might need additional learning"],
    "recommended_learning_path": ["personalized recommendations for onboarding"]
}}

Return ONLY the JSON object, no additional text."""

    try:
        response = grok_client.chat.completions.create(
            model=Config.XAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert technical recruiter and engineering manager who analyzes resumes to understand candidates' technical backgrounds and create personalized onboarding plans."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )
        
        # Extract JSON from response
        analysis_text = response.choices[0].message.content.strip()
        
        # Try to parse as JSON
        if analysis_text.startswith("```json"):
            analysis_text = analysis_text[7:-3].strip()
        elif analysis_text.startswith("```"):
            analysis_text = analysis_text[3:-3].strip()
        
        analysis = json.loads(analysis_text)
        return analysis
        
    except Exception as e:
        raise ValueError(f"Failed to analyze resume with Grok: {str(e)}")


# Resume Analysis Endpoints

@app.post("/api/analyzeResume")
async def analyze_resume(
    resume: UploadFile = File(...),
    candidate_email: Optional[str] = Form(None)
):
    """
    Upload and analyze a resume PDF using Grok API.
    
    Returns:
        JSON with analysis results and profile_id
    """
    # Validate file type
    if not allowed_file(resume.filename):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Check file size
    contents = await resume.read()
    file_size = len(contents)
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum {MAX_FILE_SIZE / 1024 / 1024}MB"
        )
    
    try:
        # Generate unique ID for this profile
        timestamp = datetime.now().isoformat()
        profile_id = hashlib.md5(f"{candidate_email}{timestamp}".encode()).hexdigest()[:12]
        
        # Save uploaded PDF
        resume_path = UPLOAD_FOLDER / f"{profile_id}_{resume.filename}"
        with open(resume_path, 'wb') as f:
            f.write(contents)
        
        # Extract text from PDF
        resume_text = extract_text_from_pdf(resume_path)
        
        if not resume_text or len(resume_text) < 100:
            raise HTTPException(
                status_code=400,
                detail="Could not extract sufficient text from PDF"
            )
        
        # Analyze with Grok
        analysis = await analyze_resume_with_grok(resume_text)
        
        # Add metadata
        profile_data = {
            "profile_id": profile_id,
            "candidate_email": candidate_email or "unknown",
            "uploaded_at": timestamp,
            "resume_filename": resume.filename,
            "analysis": analysis
        }
        
        # Save analysis to file
        analysis_path = ANALYZED_FOLDER / f"{profile_id}.json"
        with open(analysis_path, 'w') as f:
            json.dump(profile_data, f, indent=2)
        
        # Return analysis
        return {
            "success": True,
            "profile_id": profile_id,
            "message": "Resume analyzed successfully",
            "analysis": analysis
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/api/getProfile/{profile_id}")
async def get_profile(profile_id: str):
    """
    Retrieve a previously analyzed profile by ID.
    
    Args:
        profile_id: The unique profile identifier
    
    Returns:
        JSON with the stored profile analysis
    """
    analysis_path = ANALYZED_FOLDER / f"{profile_id}.json"
    
    if not analysis_path.exists():
        raise HTTPException(status_code=404, detail="Profile not found")
    
    try:
        with open(analysis_path, 'r') as f:
            profile_data = json.load(f)
        return profile_data
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load profile: {str(e)}"
        )


# Legacy endpoint for backward compatibility
@app.get("/api/getCodeBaseSummary")
async def get_code_base_summary(codebase_url: str):
    """
    Legacy endpoint - now returns real stored analysis data.
    
    For the latest analysis, use: GET /api/codebases/repo/latest?repo_url={url}
    For all analyses, use: GET /api/codebases
    """
    if not codebase_url:
        raise HTTPException(status_code=400, detail="missing codebase_url")
    
    # Try to get the latest stored analysis
    analysis = scheduler_instance.get_latest_analysis(codebase_url)
    
    if not analysis:
        # Fallback to hardcoded mock data for backward compatibility
        PREPROCESSED_WIKIS = {
            "https://github.com/facebook/rocksdb": {
                "meta": {
                    "name": "RocksDB",
                    "repo_url": "https://github.com/facebook/rocksdb",
                    "language": ["C++", "C"],
                    "last_indexed_iso": "2024-02-01T12:00:00Z",
                    "maintainers": [
                        {"name": "Storage Team", "contact": "storage@example.com"}
                    ],
                },
                "summary": {
                    "one_liner": "Embedded persistent key-value store optimized for fast storage.",
                    "problem_solved": [
                        "Low-latency reads/writes on fast storage hardware"
                    ],
                },
            }
        }
        
        wiki = PREPROCESSED_WIKIS.get(codebase_url)
        if not wiki:
            raise HTTPException(
                status_code=404,
                detail=f"No analysis found for {codebase_url}. Use POST /api/codebases/trigger to analyze it."
            )
        return {"wiki": wiki}
    
    # Convert stored analysis to legacy wiki format for backward compatibility
    wiki = {
        "meta": {
            "name": analysis["metadata"]["repo_name"],
            "repo_url": analysis["repo_url"],
            "last_indexed_iso": analysis["analyzed_at"],
        },
        "summary": analysis["summary"],
        "chapters": analysis["chapters"],
        "knowledge_graph": analysis.get("knowledge_graph", {}),
    }
    
    return {"wiki": wiki}


# Codebase Analysis Storage Endpoints

@app.get("/api/codebases")
async def list_codebase_analyses():
    """
    List all stored codebase analyses.
    
    Returns a list of all analyzed codebases with metadata.
    """
    analyses = scheduler_instance.list_all_analyses()
    return {
        "success": True,
        "count": len(analyses),
        "analyses": analyses
    }


@app.get("/api/codebases/{analysis_id}")
async def get_codebase_analysis(analysis_id: str):
    """
    Get a specific codebase analysis by ID.
    
    Args:
        analysis_id: The analysis identifier (e.g., "facebook_rocksdb_20241207_020000")
    
    Returns:
        Complete analysis including summary, chapters, and knowledge graph.
    """
    analysis = scheduler_instance.get_analysis(analysis_id)
    
    if not analysis:
        raise HTTPException(
            status_code=404,
            detail=f"Analysis not found: {analysis_id}"
        )
    
    return {
        "success": True,
        "analysis": analysis
    }


@app.get("/api/codebases/repo/latest")
async def get_latest_codebase_analysis(repo_url: str):
    """
    Get the latest analysis for a specific repository.
    
    Args:
        repo_url: Repository URL (e.g., "https://github.com/facebook/rocksdb")
    
    Returns:
        Most recent analysis for the repository.
    """
    analysis = scheduler_instance.get_latest_analysis(repo_url)
    
    if not analysis:
        raise HTTPException(
            status_code=404,
            detail=f"No analysis found for repository: {repo_url}"
        )
    
    return {
        "success": True,
        "analysis": analysis
    }


@app.post("/api/codebases/trigger")
async def trigger_codebase_analysis():
    """
    Manually trigger codebase analysis job (for testing).
    
    Normally runs daily via scheduler, but can be triggered manually.
    """
    try:
        await scheduled_analysis_job()
        return {
            "success": True,
            "message": "Codebase analysis job triggered successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to trigger analysis: {str(e)}"
        )


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Onboarding-x-Grok Unified API",
        "version": "2.0.0",
        "features": {
            "codebase_analysis": "POST /api/analyze - Analyze codebases with Grok",
            "resume_analysis": "POST /api/analyzeResume - Analyze resumes for onboarding",
            "profile_retrieval": "GET /api/getProfile/{id} - Get analyzed profiles"
        },
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)
