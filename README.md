# Onboarding-x-Grok

Next.js frontend scaffold + Flask API for onboarding wiki generation.

## Setup (local, Flask API)
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the dev server:
   ```bash
   python app.py
   ```
3. Hit the API:
   ```bash
   curl "http://localhost:8080/api/getCodeBaseSummary?codebase_url=https://github.com/facebook/rocksdb"
   ```

## API
### GET /api/getCodeBaseSummary
Returns a preprocessed wiki document for a repository.

Query params:
- `codebase_url` (required) — canonical repo URL, e.g. `https://github.com/facebook/rocksdb`

Response shape:
```json
{
  "wiki": {
    "meta": {
      "name": "RocksDB",
      "repo_url": "...",
      "language": ["C++", "C"],
      "last_indexed_iso": "2024-02-01T12:00:00Z",
      "maintainers": [{"name": "Storage Team", "contact": "storage@example.com"}]
    },
    "summary": {
      "one_liner": "...",
      "problem_solved": ["...", "..."],
      "architecture_overview": "..."
    },
    "architecture": {
      "components": [{"id": "api", "label": "Public API", "description": "..."}],
      "edges": [{"source": "api", "target": "write_path", "label": "writes"}],
      "callouts": [{"title": "Performance levers", "bullets": ["...", "..."]}]
    },
    "workflows": [{"name": "Write flow", "steps": ["...", "..."]}],
    "modules": [
      {
        "path": "db/db_impl.cc",
        "role": "Core DB implementation; coordinates reads/writes and background jobs.",
        "owner": "storage-runtime",
        "risky_changes": ["Threading and mutex ordering", "..."]
      }
    ],
    "operational_readiness": {
      "metrics": [{"name": "rocksdb_compaction_pending", "why": "Backlog signals IO pressure"}],
      "runbooks": [{"title": "Write stalls", "summary": "..."}]
    },
    "getting_started": {
      "dev_setup": ["Install dependencies: ..."],
      "sample_usage": "DB* db; Options opts; ..."
    },
    "faq": [{"q": "When to use universal compaction?", "a": "..."}]
  }
}
```

The schema is designed so frontend can render:
- Header with repo metadata and one-liner
- Problem/overview and architecture graph (nodes from `components`, edges from `edges`)
- Workflows as step lists
- Module catalog with risk callouts
- Ops readiness (metrics + runbooks)
- Getting started and FAQ

## Deploy to Google Cloud Run (Flask API)
This repo includes a `Dockerfile` for the Flask API. Cloud Run will build and run it with Gunicorn.

1. Install and init gcloud (once):
   ```bash
   gcloud auth login
   gcloud auth configure-docker
   gcloud config set project <YOUR_PROJECT_ID>
   gcloud config set run/region us-central1
   gcloud services enable run.googleapis.com artifactregistry.googleapis.com
   ```
2. Deploy directly from source (Cloud Build will use the Dockerfile):
   ```bash
   gcloud run deploy wiki-api --source . --allow-unauthenticated
   ```
   The command prints the service URL when finished.
3. Test:
   ```bash
   curl "<SERVICE_URL>/api/getCodeBaseSummary?codebase_url=https://github.com/facebook/rocksdb"
   ```

Notes:
- The Flask API is stateless and read-only; swap out `PREPROCESSED_WIKIS` in `app.py` for a real datastore.
- If you prefer manual build + deploy:
   ```bash
   gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/wiki-api
   gcloud run deploy wiki-api --image gcr.io/$GOOGLE_CLOUD_PROJECT/wiki-api --allow-unauthenticated
   ```
