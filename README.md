# Onboarding-x-Grok

Backend API service for generating codebase tutorials and onboarding wikis using Grok Code API. This service analyzes codebases (GitHub repositories or local directories) and generates structured tutorial content including summaries, chapters, knowledge graphs, and visualizations.

## Project Overview

This API provides comprehensive documentation for GitHub repositories, including:
- Repository metadata and overview
- Architecture diagrams (components, edges, callouts)
- Workflow descriptions (write/read/compaction flows)
- Module catalog with ownership and risk information
- Operational readiness (metrics, runbooks)
- Getting started guides and FAQs
- Tutorial generation with knowledge graphs and visualizations

## Features

- **Codebase Analysis**: Analyze GitHub repositories or local codebase directories
- **Tutorial Generation**: Generate structured tutorial content using Grok Code API
- **Knowledge Graphs**: Build and visualize relationships between code components
- **Abstraction Identification**: Identify design patterns and architectural components
- **Visualizations**: Generate dependency graphs, structure trees, and knowledge graphs

## Technology Stack

- **Backend**: Python 3.11+ with Flask 3.0 (production) and FastAPI (development)
- **Deployment**: Google Cloud Run (containerized with Docker)
- **Production Server**: Gunicorn

## Setup

### Prerequisites

- Python 3.11+
- Grok API key from [xAI](https://x.ai/api/) (for tutorial generation features)
- pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd OnboardingxGrok
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Copy `.env.sample` to `.env` (if available) or create a `.env` file
   - Add your Grok API key (for FastAPI tutorial generation):
   ```
   XAI_API_KEY=your_grok_api_key_here
   XAI_MODEL=grok-code-fast-1
   XAI_BASE_URL=https://api.x.ai/v1
   ```
   - Optionally add GitHub token for private repos:
   ```
   GITHUB_TOKEN=your_github_token_here
   ```

## Usage

### Running the API Server

**Flask Server (Production)**:
```bash
python -m src.app
```
The API will start on `http://localhost:8080`

**FastAPI Server (Development)**:
```bash
python main.py
```
Or using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
The API will be available at `http://localhost:8000`
- API documentation: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

## API Documentation

### Health Check
**GET** `/` (Flask) or `/health` (FastAPI)

Returns API health status.

**Response**:
```json
{
  "status": "ok"
}
```

### Get Codebase Summary (Flask)
**GET** `/api/getCodeBaseSummary`

Returns a preprocessed wiki document for a repository.

**Query Parameters**:
- `codebase_url` (required) - Canonical repository URL (e.g., `https://github.com/facebook/rocksdb`)

**Response Schema**:
```json
{
  "wiki": {
    "meta": {
      "name": "RocksDB",
      "repo_url": "https://github.com/facebook/rocksdb",
      "language": ["C++", "C"],
      "last_indexed_iso": "2024-02-01T12:00:00Z",
      "maintainers": [{"name": "Storage Team", "contact": "storage@example.com"}]
    },
    "summary": {
      "one_liner": "Embedded persistent key-value store optimized for fast storage.",
      "problem_solved": ["Low-latency reads/writes...", "..."],
      "architecture_overview": "Log-structured merge-tree (LSM) engine with..."
    },
    "architecture": {
      "components": [
        {
          "id": "api",
          "label": "Public API",
          "description": "DB, ColumnFamilyHandle, Options; entrypoint for users."
        }
      ],
      "edges": [
        {
          "source": "api",
          "target": "write_path",
          "label": "writes"
        }
      ],
      "callouts": [
        {
          "title": "Performance levers",
          "bullets": ["Block cache size and bloom filters", "..."]
        }
      ]
    },
    "workflows": [
      {
        "name": "Write flow",
        "steps": [
          "Client issues WriteBatch via DB::Write with options.",
          "..."
        ]
      }
    ],
    "modules": [
      {
        "path": "db/db_impl.cc",
        "role": "Core DB implementation; coordinates reads/writes and background jobs.",
        "owner": "storage-runtime",
        "risky_changes": ["Threading and mutex ordering", "..."]
      }
    ],
    "operational_readiness": {
      "metrics": [
        {
          "name": "rocksdb_compaction_pending",
          "why": "Backlog signals IO pressure"
        }
      ],
      "runbooks": [
        {
          "title": "Write stalls",
          "summary": "Reduce ingest rate; increase memtable/level size; tune compaction."
        }
      ]
    },
    "getting_started": {
      "dev_setup": [
        "Install dependencies: snappy/zlib/bzip2/lz4/zstd",
        "Build: `cmake -S . -B build && cmake --build build`",
        "..."
      ],
      "sample_usage": "DB* db; Options opts; opts.create_if_missing = true; ..."
    },
    "faq": [
      {
        "q": "When to use universal compaction?",
        "a": "Use for high-update or time-series workloads needing low read amp."
      }
    ]
  }
}
```

**Error Responses**:
- `400 Bad Request`: Missing `codebase_url` parameter
- `404 Not Found`: Codebase not indexed

### Analyze Codebase (FastAPI)
**POST** `/api/analyze`

Analyze a codebase and generate tutorial content.

**Request Body:**
```json
{
  "repo_url": "https://github.com/username/repo",
  "include": ["*.py", "*.js"],
  "exclude": ["tests/*", "node_modules/*"],
  "max_size": 100000,
  "max_abstractions": 10
}
```

Or for local directories:
```json
{
  "local_path": "/path/to/codebase",
  "include": ["*.py"],
  "exclude": ["tests/*"],
  "max_size": 100000
}
```

**Response:**
```json
{
  "summary": "High-level overview of the codebase...",
  "chapters": [
    {
      "title": "Core Components",
      "content": "Detailed explanation...",
      "files": ["src/core.py"],
      "order": 1
    }
  ],
  "knowledge_graph": {
    "nodes": [...],
    "edges": [...]
  },
  "abstractions": [
    {
      "name": "Design Pattern",
      "description": "...",
      "pattern_type": "design_pattern",
      "files": ["src/pattern.py"]
    }
  ],
  "visualizations": {
    "dependency_graph": {...},
    "knowledge_graph": {...},
    "structure_tree": {...}
  }
}
```

## Frontend Integration

The API schema is designed to work with wiki-rendering frameworks. The frontend can:

1. **Display metadata**: Show repo name, languages, maintainers
2. **Render architecture diagrams**: Use `components` and `edges` to generate graph visualizations (e.g., with D3.js, Mermaid, or React Flow)
3. **Show workflows**: Display step-by-step processes
4. **Module catalog**: Present file paths with ownership and risk information
5. **Operational guides**: Display metrics and runbooks
6. **Getting started**: Show setup instructions and code samples
7. **FAQ section**: Display common questions and answers

### Recommended Frontend Frameworks
- **Markdown**: Convert JSON to Markdown and use frameworks like:
  - [GitBook](https://www.gitbook.com/)
  - [Docusaurus](https://docusaurus.io/)
  - [VitePress](https://vitepress.dev/)
- **Custom React App**: Use components to render each section
- **Vue/Nuxt**: Similar component-based approach

## Deployment to Google Cloud Run

### Prerequisites
1. Google Cloud account with billing enabled
2. gcloud CLI installed and configured
3. Docker (optional, for local testing)

### Initial Setup (One-time)

```bash
# Login to Google Cloud
gcloud auth login

# Set your project
gcloud config set project <YOUR_PROJECT_ID>

# Set region
gcloud config set run/region us-central1

# Enable required services
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### Deploy the API

**Option 1: Direct Deploy (Recommended)**
```bash
gcloud run deploy onboarding-wiki-api \
  --source . \
  --allow-unauthenticated \
  --region us-central1
```

This command will:
- Build the Docker image using Cloud Build
- Push it to Google Container Registry
- Deploy to Cloud Run
- Print the service URL when complete

**Option 2: Manual Build and Deploy**
```bash
# Build the image
gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/wiki-api

# Deploy to Cloud Run
gcloud run deploy onboarding-wiki-api \
  --image gcr.io/$GOOGLE_CLOUD_PROJECT/wiki-api \
  --allow-unauthenticated \
  --region us-central1
```

### Test the Deployed API

```bash
# Get the service URL
SERVICE_URL=$(gcloud run services describe onboarding-wiki-api --region us-central1 --format 'value(status.url)')

# Test health endpoint
curl "$SERVICE_URL/"

# Test the API
curl "$SERVICE_URL/api/getCodeBaseSummary?codebase_url=https://github.com/facebook/rocksdb"
```

### Update Deployment

After making changes to the code:
```bash
gcloud run deploy onboarding-wiki-api --source .
```

### Monitor and Manage

```bash
# View logs
gcloud run logs read onboarding-wiki-api --region us-central1

# View service details
gcloud run services describe onboarding-wiki-api --region us-central1

# Delete the service
gcloud run services delete onboarding-wiki-api --region us-central1
```

## Configuration

### Environment Variables

**For Flask (Production)**:
- `PORT`: Server port (default: 8080, automatically set by Cloud Run)

**For FastAPI (Development)**:
- `XAI_API_KEY` (required): Grok API key
- `XAI_MODEL` (optional): Model name (default: `grok-code-fast-1`)
- `XAI_BASE_URL` (optional): API base URL (default: `https://api.x.ai/v1`)
- `GITHUB_TOKEN` (optional): GitHub token for private repos or rate limits
- `DEFAULT_MAX_FILE_SIZE` (optional): Default max file size in bytes (default: 100000)

### Production Considerations

1. **Database Integration**: Replace `PREPROCESSED_WIKIS` in-memory dictionary with:
   - Cloud Firestore
   - Cloud SQL (PostgreSQL/MySQL)
   - Cloud Memorystore (Redis)

2. **Authentication**: Add API key validation or OAuth for private repos

3. **Rate Limiting**: Implement request throttling

4. **Caching**: Add Redis cache layer for frequently accessed wikis

5. **Logging**: Integrate Cloud Logging for better observability

## Project Structure

```
.
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── src/                   # Source code
│   ├── __init__.py       # Package initialization
│   └── app.py            # Main Flask application
├── api/
│   └── routes.py         # API endpoint definitions (FastAPI)
├── services/
│   ├── codebase_analyzer.py      # Codebase crawling and parsing
│   ├── tutorial_generator.py     # Grok API integration for content generation
│   └── visualization_generator.py # Graph and diagram generation
├── utils/
│   ├── grok_client.py    # Grok API client wrapper
│   └── markdown_generator.py # Markdown documentation generator
├── models/
│   └── schemas.py        # Request/response models
├── docs/                  # Documentation
│   ├── DEPLOYMENT.md     # Google Cloud Run deployment guide
│   ├── SCHEMA.md         # API schema documentation
│   └── QUICKSTART.md     # Quick start guide
├── deploy.sh             # Deployment script
├── Dockerfile           # Container configuration
├── .gcloudignore       # Files to ignore during deployment
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Development

The backend is designed to work with a frontend application. The API returns structured JSON that can be consumed by any frontend framework.

### Example Frontend Integration

```javascript
const response = await fetch('http://localhost:8000/api/analyze', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    repo_url: 'https://github.com/username/repo',
    include: ['*.py'],
    exclude: ['tests/*']
  })
});

const tutorial = await response.json();
console.log(tutorial.summary);
console.log(tutorial.chapters);
```

## Development Roadmap

### Current Status (Prototype)
✅ REST API with comprehensive schema  
✅ Mock data for RocksDB example  
✅ CORS enabled for frontend integration  
✅ Cloud Run deployment ready  
✅ FastAPI tutorial generation with Grok Code API

### Next Steps
- [ ] Add database persistence
- [ ] Implement GitHub repo analyzer
- [ ] Add caching layer
- [ ] Create admin endpoints for indexing
- [ ] Add authentication/authorization
- [ ] Build monitoring dashboard

## License

MIT

## Support

For issues or questions, please open a GitHub issue.
