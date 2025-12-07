# Codebase Summary

This document provides an overview of all core files in the Grok Code Tutorial Backend project.

## Project Structure

```
.
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration management
├── api/
│   └── routes.py         # API endpoint definitions
├── models/
│   └── schemas.py        # Pydantic data models
├── services/
│   ├── codebase_analyzer.py      # Codebase crawling and parsing
│   ├── tutorial_generator.py     # Grok API integration for content generation
│   └── visualization_generator.py # Graph and diagram generation
└── utils/
    ├── grok_client.py    # Grok API client wrapper
    └── markdown_generator.py # Markdown documentation generator
```

## File Descriptions

### `main.py`
**Purpose:** FastAPI application entry point

- Initializes the FastAPI application with metadata
- Configures CORS middleware for frontend integration
- Registers all API routes from `api/routes.py`
- Provides root endpoint with API information
- Runs the development server when executed directly

**Key Features:**
- CORS enabled for frontend requests
- Auto-generated API documentation at `/docs`
- Health check and root endpoints

---

### `config.py`
**Purpose:** Centralized configuration management

- Loads environment variables from `.env` file
- Provides default values for configuration options
- Validates required configuration (API keys)
- Stores Grok API settings (API key, model, base URL)
- Stores GitHub token for repository cloning
- Defines default file patterns and analysis parameters

**Configuration Variables:**
- `XAI_API_KEY`: Grok API key (required)
- `XAI_MODEL`: Model name (default: `grok-code-fast-1`)
- `XAI_BASE_URL`: API base URL (default: `https://api.x.ai/v1`)
- `GITHUB_TOKEN`: Optional GitHub token for private repos
- `DEFAULT_MAX_FILE_SIZE`: Maximum file size in bytes (default: 100KB)

---

### `api/routes.py`
**Purpose:** API route handlers

- Defines all FastAPI endpoints for the codebase analysis API
- Validates request data using Pydantic models
- Orchestrates the analysis pipeline:
  1. Codebase analysis (CodebaseAnalyzer)
  2. Tutorial generation (TutorialGenerator with Grok API)
  3. Visualization generation (VisualizationGenerator)
- Handles errors and returns appropriate HTTP status codes
- Returns structured JSON responses

**Endpoints:**
- `GET /health`: Health check endpoint
- `POST /api/analyze`: Main endpoint to analyze codebases
  - Request: `AnalysisRequest` (repo_url or local_path, file patterns, etc.)
  - Response: `AnalysisResponse` (summary, chapters, knowledge graph, visualizations)

---

### `models/schemas.py`
**Purpose:** Pydantic data models for API requests and responses

- Defines request models (`AnalysisRequest`)
- Defines response models (`AnalysisResponse`, `HealthResponse`)
- Defines data structures (KnowledgeGraph, Chapter, Abstraction, Visualization)
- Provides field validation and type checking
- Generates OpenAPI/Swagger documentation automatically

**Key Models:**
- **Request Models:**
  - `AnalysisRequest`: Input for codebase analysis (repo_url, local_path, file patterns)
  
- **Response Models:**
  - `AnalysisResponse`: Complete analysis results
  - `HealthResponse`: Health check response
  
- **Data Structures:**
  - `KnowledgeGraph`: Graph structure with nodes and edges
  - `KnowledgeGraphNode`: Individual node in the graph
  - `KnowledgeGraphEdge`: Relationship between nodes
  - `Chapter`: Tutorial chapter with content and files
  - `Abstraction`: Code pattern or abstraction
  - `Visualization`: Graph visualization data (base64 encoded)

---

### `services/codebase_analyzer.py`
**Purpose:** Codebase analysis service

- Analyzes codebases by crawling files and parsing code structure
- Supports both GitHub repositories (via cloning) and local directories
- Extracts information about classes, functions, imports, and dependencies
- Builds dependency graphs from import statements
- Generates structure summaries

**Main Methods:**
- `analyze()`: Main entry point - analyzes codebase and returns structure
- `_clone_repository()`: Clones GitHub repo to temporary directory
- `_collect_files()`: Collects files matching patterns
- `_read_files()`: Reads file contents
- `_parse_code_structure()`: Parses code to extract structure (Python AST, JS regex)
- `_build_dependency_graph()`: Builds dependency relationships
- `_generate_structure_summary()`: Creates text summary

**Output:**
Returns dictionary with:
- `files`: List of analyzed file paths
- `file_contents`: Dictionary mapping file paths to content
- `structure`: Parsed structure (modules, classes, functions, imports)
- `dependencies`: Dependency graph (file -> imported modules)
- `summary`: Text summary of codebase structure
- `root_path`: Root path of the codebase

---

### `services/tutorial_generator.py`
**Purpose:** Tutorial generation service using Grok API

- Generates tutorial content from codebase analysis using the Grok Code API
- Creates summaries, identifies abstractions, generates tutorial chapters
- Builds knowledge graphs from code structure

**Main Methods:**
- `generate_summary()`: Creates comprehensive codebase summary
- `identify_abstractions()`: Identifies design patterns and abstractions
- `generate_chapters()`: Breaks codebase into tutorial chapters
- `build_knowledge_graph()`: Constructs graph from code structure (no API call)
- `_select_key_files()`: Selects important files for API context
- `_organize_files_by_topic()`: Groups files by logical categories
- `_parse_abstractions()`: Parses JSON response from Grok API
- `_parse_chapters()`: Parses chapter data from Grok API

**Grok API Integration:**
Uses different prompts for different tasks:
- `"summarize"`: High-level overview
- `"identify_abstractions"`: Pattern identification
- `"generate_chapters"`: Tutorial chapter generation

**Output:**
- Summary: Text summary of the codebase
- Abstractions: List of identified patterns
- Chapters: List of tutorial chapters with content
- Knowledge Graph: Graph structure with nodes and edges

---

### `services/visualization_generator.py`
**Purpose:** Visualization generation service

- Generates visual representations of codebase structure, dependencies, and knowledge graphs
- Creates SVG and PNG images using NetworkX and Matplotlib

**Main Methods:**
- `generate_dependency_graph()`: Creates dependency visualization
- `generate_knowledge_graph_visualization()`: Visualizes knowledge graph
- `generate_structure_tree()`: Creates hierarchical structure tree
- `_render_graph_svg()`: Renders graph as SVG string
- `_render_graph_png()`: Renders graph as PNG (base64)
- `_render_tree_svg()`: Renders tree structure as SVG
- `_render_tree_png()`: Renders tree structure as PNG

**Visualization Types:**
1. **Dependency Graph**: Shows import relationships between files
2. **Knowledge Graph**: Complete graph with all components and relationships
3. **Structure Tree**: Hierarchical view (files -> classes -> methods)

**Output:**
Returns `Visualization` objects with:
- `type`: Visualization type name
- `format`: "svg" or "png"
- `data`: Base64 encoded image data

---

### `utils/grok_client.py`
**Purpose:** Grok API client wrapper

- Provides a Python client for interacting with the Grok Code API (xAI)
- Handles authentication, request formatting, and response parsing
- Manages HTTP client lifecycle

**Main Methods:**
- `chat_completion()`: Generic chat completion API call
- `analyze_codebase()`: Specialized method for codebase analysis
  - Supports different tasks: "analyze", "summarize", "identify_abstractions", "generate_chapters"
- `close()`: Cleanup HTTP client

**Configuration:**
- API Key: From `Config.XAI_API_KEY`
- Model: `Config.XAI_MODEL` (default: `grok-code-fast-1`)
- Base URL: `Config.XAI_BASE_URL` (default: `https://api.x.ai/v1`)
- Timeout: 300 seconds (5 minutes) for large codebases

**Context Management:**
- Automatically selects key files to stay within API context limits
- Truncates file contents if needed (max ~200k characters)
- Limits each file to 5000 characters in context

---

### `utils/markdown_generator.py`
**Purpose:** Markdown documentation generator

- Converts analysis results into markdown documentation files
- Generates the main `output.md` file with summary and visualizations
- Generates individual chapter markdown files

**Main Methods:**
- `generate_output_md()`: Creates main output.md file
  - Includes summary, structure, abstractions, knowledge graph info
  - Adds visualization sections with explanations
  - Includes analysis metadata
- `generate_chapter_md()`: Creates individual chapter markdown files
  - Formats chapter title and content
  - Lists related files
  - Includes sections if available

**Output Files:**
- `output.md`: Main report with all analysis results
- `chapter_XX_title.md`: Individual chapter files (one per chapter)

---

## Data Flow

1. **Request** → `api/routes.py` receives HTTP request
2. **Validation** → `models/schemas.py` validates request data
3. **Analysis** → `services/codebase_analyzer.py` analyzes codebase structure
4. **Generation** → `services/tutorial_generator.py` uses `utils/grok_client.py` to generate content
5. **Visualization** → `services/visualization_generator.py` creates graphs
6. **Response** → Structured JSON response returned to client
7. **Documentation** → `utils/markdown_generator.py` generates markdown files (optional)

## Key Dependencies

- **FastAPI**: Web framework for API
- **Pydantic**: Data validation and serialization
- **httpx**: Async HTTP client for Grok API
- **NetworkX**: Graph creation and manipulation
- **Matplotlib**: Graph rendering
- **GitPython**: GitHub repository cloning
- **python-dotenv**: Environment variable management

