# Onboarding-x-Grok

A Flask-based REST API that generates onboarding wikis for GitHub repositories. This service returns comprehensive documentation schemas designed for new hires to understand codebases quickly.

## Project Overview

This API provides preprocessed wiki documentation for GitHub repositories, including:
- Repository metadata and overview
- Architecture diagrams (components, edges, callouts)
- Workflow descriptions (write/read/compaction flows)
- Module catalog with ownership and risk information
- Operational readiness (metrics, runbooks)
- Getting started guides and FAQs

## Technology Stack

- **Backend**: Python 3.11 + Flask 3.0
- **Deployment**: Google Cloud Run (containerized with Docker)
- **Production Server**: Gunicorn

## Local Development

### Prerequisites
- Python 3.11+
- pip

### Setup and Run

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the development server**:
   ```bash
   python -m src.app
   ```

   The API will start on `http://localhost:8080`

3. **Test the API**:
   ```bash
   curl "http://localhost:8080/api/getCodeBaseSummary?codebase_url=https://github.com/facebook/rocksdb"
   ```

## API Documentation

### Health Check
**GET** `/`

Returns API health status.

**Response**:
```json
{
  "status": "ok"
}
```

### Get Codebase Summary
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
- `PORT`: Server port (default: 8080, automatically set by Cloud Run)

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
├── src/                   # Source code
│   ├── __init__.py       # Package initialization
│   └── app.py            # Main Flask application
├── docs/                  # Documentation
│   ├── DEPLOYMENT.md     # Google Cloud Run deployment guide
│   ├── SCHEMA.md         # API schema documentation
│   └── QUICKSTART.md     # Quick start guide
├── deploy.sh             # Deployment script
├── requirements.txt      # Python dependencies
├── Dockerfile           # Container configuration
├── .gcloudignore       # Files to ignore during deployment
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Development Roadmap

### Current Status (Prototype)
✅ REST API with comprehensive schema  
✅ Mock data for RocksDB example  
✅ CORS enabled for frontend integration  
✅ Cloud Run deployment ready  

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
