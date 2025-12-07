"""
API Route Handlers
==================

Purpose:
    Defines all FastAPI endpoints for the codebase analysis API. Handles HTTP requests,
    validates input, orchestrates service calls, and returns structured responses.

Key Responsibilities:
    - Define REST API endpoints
    - Validate request data using Pydantic models
    - Orchestrate the analysis pipeline:
        1. Codebase analysis (CodebaseAnalyzer)
        2. Tutorial generation (TutorialGenerator with Grok API)
        3. Visualization generation (VisualizationGenerator)
    - Handle errors and return appropriate HTTP status codes
    - Return structured JSON responses

Endpoints:
    - GET /health: Health check endpoint
    - POST /api/analyze: Main endpoint to analyze codebases
        Request: AnalysisRequest (repo_url or local_path, file patterns, etc.)
        Response: AnalysisResponse (summary, chapters, knowledge graph, visualizations)

Dependencies:
    - services.codebase_analyzer: Analyzes codebase structure
    - services.tutorial_generator: Generates tutorial content using Grok API
    - services.visualization_generator: Creates graph visualizations
    - utils.grok_client: Grok API client wrapper
"""
from fastapi import APIRouter, HTTPException
from models.schemas import (
    AnalysisRequest,
    AnalysisResponse,
    HealthResponse
)
from services.codebase_analyzer import CodebaseAnalyzer
from services.tutorial_generator import TutorialGenerator
from services.visualization_generator import VisualizationGenerator
from utils.grok_client import GrokClient
from config import Config

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=Config.API_VERSION
    )


@router.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_codebase(request: AnalysisRequest):
    """
    Analyze a codebase and generate tutorial content.
    
    Accepts either a GitHub repository URL or local directory path.
    Returns structured tutorial content including summary, chapters, knowledge graph, and visualizations.
    """
    # Validate request
    if not request.repo_url and not request.local_path:
        raise HTTPException(
            status_code=400,
            detail="Either repo_url or local_path must be provided"
        )
    
    try:
        # Initialize services
        analyzer = CodebaseAnalyzer(max_file_size=request.max_size or Config.DEFAULT_MAX_FILE_SIZE)
        grok_client = GrokClient()
        tutorial_generator = TutorialGenerator(grok_client)
        viz_generator = VisualizationGenerator()
        
        # Analyze codebase
        analysis_result = await analyzer.analyze(
            repo_url=request.repo_url,
            local_path=request.local_path,
            include_patterns=request.include,
            exclude_patterns=request.exclude
        )
        
        # Generate tutorial content using Grok API
        summary = await tutorial_generator.generate_summary(
            codebase_summary=analysis_result["summary"],
            file_contents=analysis_result["file_contents"]
        )
        
        # Generate chapters
        chapters = await tutorial_generator.generate_chapters(
            codebase_summary=analysis_result["summary"],
            file_contents=analysis_result["file_contents"],
            structure=analysis_result["structure"]
        )
        
        # Identify abstractions
        abstractions = await tutorial_generator.identify_abstractions(
            codebase_summary=analysis_result["summary"],
            file_contents=analysis_result["file_contents"],
            max_abstractions=request.max_abstractions or 10
        )
        
        # Build knowledge graph
        knowledge_graph = tutorial_generator.build_knowledge_graph(
            structure=analysis_result["structure"],
            dependencies=analysis_result["dependencies"]
        )
        
        # Generate visualizations
        dependency_viz = viz_generator.generate_dependency_graph(
            dependencies=analysis_result["dependencies"],
            format="svg"
        )
        
        knowledge_viz = viz_generator.generate_knowledge_graph_visualization(
            knowledge_graph=knowledge_graph,
            format="svg"
        )
        
        structure_viz = viz_generator.generate_structure_tree(
            structure=analysis_result["structure"],
            format="svg"
        )
        
        # Cleanup
        await grok_client.close()
        
        # Build response
        return AnalysisResponse(
            summary=summary,
            chapters=chapters,
            knowledge_graph=knowledge_graph,
            abstractions=abstractions,
            visualizations={
                "dependency_graph": dependency_viz,
                "knowledge_graph": knowledge_viz,
                "structure_tree": structure_viz
            },
            metadata={
                "files_analyzed": len(analysis_result["files"]),
                "root_path": analysis_result.get("root_path", ""),
                "model_used": Config.XAI_MODEL
            }
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing codebase: {str(e)}"
        )

