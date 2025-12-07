"""
Pydantic Data Models (Schemas)
================================

Purpose:
    Defines all data models for API requests and responses using Pydantic. These models
    provide type validation, automatic serialization/deserialization, and API documentation.

Key Responsibilities:
    - Define request models (AnalysisRequest)
    - Define response models (AnalysisResponse, HealthResponse)
    - Define data structures (KnowledgeGraph, Chapter, Abstraction, Visualization)
    - Provide field validation and type checking
    - Generate OpenAPI/Swagger documentation automatically

Models:
    Request Models:
        - AnalysisRequest: Input for codebase analysis (repo_url, local_path, file patterns)
    
    Response Models:
        - AnalysisResponse: Complete analysis results
        - HealthResponse: Health check response
    
    Data Structures:
        - KnowledgeGraph: Graph structure with nodes and edges
        - KnowledgeGraphNode: Individual node in the graph
        - KnowledgeGraphEdge: Relationship between nodes
        - Chapter: Tutorial chapter with content and files
        - Abstraction: Code pattern or abstraction
        - Visualization: Graph visualization data (base64 encoded)

Usage:
    These models are used by FastAPI for automatic request validation and response
    serialization. They also appear in the auto-generated API documentation at /docs.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    """Request model for codebase analysis."""
    repo_url: Optional[str] = Field(None, description="GitHub repository URL")
    local_path: Optional[str] = Field(None, description="Local directory path")
    include: Optional[List[str]] = Field(
        default=["*.py", "*.js", "*.ts"],
        description="File patterns to include"
    )
    exclude: Optional[List[str]] = Field(
        default=["**/node_modules/**", "**/__pycache__/**", "**/.git/**"],
        description="File patterns to exclude"
    )
    max_size: Optional[int] = Field(
        default=100000,
        description="Maximum file size in bytes"
    )
    max_abstractions: Optional[int] = Field(
        default=10,
        description="Maximum number of abstractions to identify"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "repo_url": "https://github.com/username/repo",
                "include": ["*.py"],
                "exclude": ["tests/*"],
                "max_size": 50000
            }
        }


class KnowledgeGraphNode(BaseModel):
    """Node in the knowledge graph."""
    id: str
    label: str
    type: str = Field(description="Type: 'module', 'class', 'function', 'file'")
    file_path: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class KnowledgeGraphEdge(BaseModel):
    """Edge in the knowledge graph."""
    source: str
    target: str
    relationship: str = Field(description="Type of relationship: 'imports', 'inherits', 'calls', 'contains'")
    metadata: Optional[Dict[str, Any]] = None


class KnowledgeGraph(BaseModel):
    """Knowledge graph structure."""
    nodes: List[KnowledgeGraphNode]
    edges: List[KnowledgeGraphEdge]


class Abstraction(BaseModel):
    """Code abstraction or pattern."""
    name: str
    description: str
    pattern_type: str = Field(description="Type: 'design_pattern', 'architecture', 'abstraction'")
    files: List[str]
    examples: Optional[List[str]] = None


class Chapter(BaseModel):
    """Tutorial chapter."""
    title: str
    content: str
    files: List[str]
    order: int
    sections: Optional[List[Dict[str, Any]]] = None


class Visualization(BaseModel):
    """Visualization data."""
    type: str = Field(description="Type: 'dependency_graph', 'structure_tree', 'knowledge_graph'")
    format: str = Field(description="Format: 'svg', 'png', 'json'")
    data: str = Field(description="Base64 encoded image or JSON string")


class AnalysisResponse(BaseModel):
    """Response model for codebase analysis."""
    summary: str
    chapters: List[Chapter]
    knowledge_graph: KnowledgeGraph
    abstractions: List[Abstraction]
    visualizations: Dict[str, Visualization]
    metadata: Optional[Dict[str, Any]] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str

