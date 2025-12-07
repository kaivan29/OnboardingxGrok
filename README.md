# Onboarding-x-Grok

Prototype Flask backend for onboarding wiki generation.

## Setup (local)
1. Create a virtualenv (optional) and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the service:
   ```bash
   flask --app app run --debug
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

## Deploy to Vercel (serverless)
This repository is configured for Vercel Python functions via `vercel-wsgi`.

1. Ensure `vercel.json`, `api/index.py`, and `requirements.txt` are present (already committed).
2. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```
3. Log in:
   ```bash
   vercel login
   ```
4. Deploy from the repo root (first time: accept prompts; set project root to current dir):
   ```bash
   vercel         # preview
   vercel --prod  # production
   ```
5. Test the endpoint:
   ```bash
   curl "https://<your-project>.vercel.app/api/getCodeBaseSummary?codebase_url=https://github.com/facebook/rocksdb"
   ```

Notes:
- Vercel functions are stateless and short-lived—suited for the current read-only API.
- For long-running indexing jobs, use a separate worker on a container host (Fly/Cloud Run/etc.) and keep this endpoint as the read layer.
