---
name: Grok Code Tutorial Backend
overview: Build a backend API service that uses Grok Code API to analyze codebases (GitHub repos or local directories) and generate structured tutorial content including summaries, knowledge graphs, chapters, and visualizations.
todos:
  - id: setup
    content: Set up project structure, requirements.txt, and configuration files
    status: completed
  - id: grok-client
    content: Implement Grok API client wrapper in utils/grok_client.py
    status: completed
    dependencies:
      - setup
  - id: codebase-analyzer
    content: Build codebase analysis service to crawl and parse repositories
    status: completed
    dependencies:
      - setup
  - id: tutorial-generator
    content: Implement tutorial generation service using Grok API for summaries, chapters, and abstractions
    status: completed
    dependencies:
      - grok-client
      - codebase-analyzer
  - id: visualization
    content: Create visualization service for knowledge graphs and diagrams
    status: completed
    dependencies:
      - codebase-analyzer
  - id: api-endpoints
    content: Build FastAPI endpoints for analysis requests and responses
    status: completed
    dependencies:
      - tutorial-generator
      - visualization
  - id: models
    content: Define Pydantic schemas for request/response models
    status: completed
    dependencies:
      - setup
---

# Grok Code Tutorial Backend API

Build a backend service that analyzes codebases using Grok Code API and generates structured tutorial content for frontend consumption.

## Architecture Overview

The backend will be a Python FastAPI service that:

- Accepts repository URLs or local directory paths
- Crawls and analyzes codebases
- Uses Grok Code API for code understanding and tutorial generation
- Returns structured JSON responses (summaries, knowledge graphs, chapters, visualizations)

## Implementation Plan

### 1. Project Setup

- Create `requirements.txt` with dependencies: `fastapi`, `uvicorn`, `httpx`, `pyyaml`, `networkx`, `graphviz`, `python-dotenv`
- Set up project structure:
  - `main.py` - FastAPI application entry point
  - `api/` - API route handlers
  - `services/` - Core business logic
  - `utils/` - Utility functions (Grok API client, code parsing, etc.)
  - `models/` - Data models/schemas
  - `.env.sample` - Environment variable template

### 2. Grok API Integration (`utils/grok_client.py`)

- Create Grok API client wrapper using httpx
- Implement authentication with `XAI_API_KEY`
- Support for `grok-code-fast-1` model (256k context window)
- Implement streaming and non-streaming request methods
- Add retry logic and error handling

### 3. Codebase Analysis Service (`services/codebase_analyzer.py`)

- Implement repository cloning (for GitHub URLs) or directory reading (for local paths)
- File filtering (include/exclude patterns, max file size)
- Code parsing to extract:
  - File structure and dependencies
  - Classes, functions, and their relationships
  - Import statements and module dependencies
  - Key abstractions and patterns

### 4. Tutorial Generation Service (`services/tutorial_generator.py`)

- **Summary Generation**: Use Grok API to generate high-level codebase summary
- **Abstraction Identification**: Prompt Grok to identify core abstractions, design patterns, and architectural components
- **Chapter Generation**: Break down codebase into logical chapters (e.g., "Core Components", "Data Models", "API Endpoints")
- **Knowledge Graph Construction**: Build graph structure showing relationships between modules, classes, and functions
- Implement prompt engineering for consistent, structured outputs

### 5. Visualization Service (`services/visualization_generator.py`)

- Generate knowledge graph visualizations using NetworkX and Graphviz
- Create dependency diagrams
- Generate code structure trees
- Export visualizations as SVG/PNG or graph data as JSON

### 6. API Endpoints (`api/routes.py`)

- `POST /api/analyze` - Main endpoint to analyze a repository
  - Request: `{ "repo_url": "...", "include": ["*.py"], "exclude": ["tests/*"], "max_size": 50000 }`
  - Or: `{ "local_path": "/path/to/code", ... }`
  - Response: `{ "summary": "...", "chapters": [...], "knowledge_graph": {...}, "visualizations": [...] }`
- `GET /api/health` - Health check endpoint
- `GET /api/status/{job_id}` - Check status of async analysis jobs (optional)

### 7. Data Models (`models/schemas.py`)

- Define Pydantic models for:
  - Analysis request/response
  - Chapter structure
  - Knowledge graph nodes and edges
  - Visualization metadata

### 8. Configuration (`config.py`)

- Environment variable management
- Grok API configuration (model, endpoint, API key)
- Default analysis parameters

## Key Files to Create

- `main.py` - FastAPI app initialization
- `api/routes.py` - API endpoint definitions
- `services/codebase_analyzer.py` - Codebase crawling and parsing
- `services/tutorial_generator.py` - Grok API integration for content generation
- `services/visualization_generator.py` - Graph and diagram generation
- `utils/grok_client.py` - Grok API client wrapper
- `models/schemas.py` - Request/response models
- `config.py` - Configuration management
- `requirements.txt` - Python dependencies
- `.env.sample` - Environment variable template

## Output Format

The API will return structured JSON:

```json
{
  "summary": "High-level overview of the codebase...",
  "chapters": [
    {
      "title": "Core Components",
      "content": "...",
      "files": ["src/core.py", ...]
    }
  ],
  "knowledge_graph": {
    "nodes": [...],
    "edges": [...]
  },
  "abstractions": [
    {
      "name": "Component Pattern",
      "description": "...",
      "files": [...]
    }
  ],
  "visualizations": {
    "dependency_graph": "base64_encoded_svg",
    "structure_tree": "base64_encoded_svg"
  }
}
```

## Environment Variables

- `XAI_API_KEY` - Grok API key (required)
- `XAI_MODEL` - Model name (default: `grok-code-fast-1`)
- `XAI_BASE_URL` - API base URL (default: `https://api.x.ai/v1`)
- `GITHUB_TOKEN` - Optional, for private repos or rate limit handling