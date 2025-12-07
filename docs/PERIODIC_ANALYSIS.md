# 🕐 Periodic Codebase Analysis - Feature Documentation

## Overview

Automated background job system that periodically analyzes configured codebases and stores the results for use in personalized onboarding plans.

**Status**: ✅ Implemented (with mock data)

**Purpose**: Feature 1 - Chapter-wise information of codebase repositories

## Architecture

```
┌─────────────────────────────────────────────────┐
│  FastAPI Application (main.py)                  │
│  ├── Scheduler (APScheduler)                    │
│  │   └── Runs daily at 2 AM                     │
│  │                                               │
│  └── Startup Event                              │
│      └── Triggers initial analysis              │
└─────────────────────────────────────────────────┘
         │
         ↓
┌─────────────────────────────────────────────────┐
│  Codebase Scheduler Service                     │
│  (services/codebase_scheduler.py)               │
│  ├── analyze_and_store()                        │
│  ├── get_analysis()                             │
│  ├── get_latest_analysis()                      │
│  └── list_all_analyses()                        │
└─────────────────────────────────────────────────┘
         │
         ↓
┌─────────────────────────────────────────────────┐
│  Storage (JSON Files)                           │
│  data/codebase_analyses/                        │
│  ├── facebook_rocksdb_20241207_025727.json      │
│  ├── pallets_flask_20241207_025727.json         │
│  └── tiangolo_fastapi_20241207_025727.json      │
└─────────────────────────────────────────────────┘
```

## Configuration

### Repository Configuration (`config_repos.py`)

```python
# List of repositories to analyze
ANALYSIS_REPOS = [
    "https://github.com/facebook/rocksdb",
    "https://github.com/pallets/flask",
    "https://github.com/tiangolo/fastapi",
]

# Schedule (cron format)
ANALYSIS_SCHEDULE = {
    "hour": 2,      # 2 AM
    "minute": 0
}

# Analysis settings
ANALYSIS_CONFIG = {
    "include_patterns": ["*.py", "*.js", "*.ts"],
    "exclude_patterns": ["**/node_modules/**", "**/__pycache__/**"],
    "max_file_size": 100000,
}
```

## Storage Format

Each analysis is stored as a JSON file:

**Filename**: `{owner}_{repo}_{timestamp}.json`

**Example**: `facebook_rocksdb_20241207_025727.json`

**Structure**:
```json
{
  "repo_url": "https://github.com/facebook/rocksdb",
  "analyzed_at": "2025-12-07T02:57:27.809406",
  "summary": {
    "overview": "...",
    "purpose": "...",
    "key_components": [...],
    "technologies": [...],
    "difficulty_level": "..."
  },
  "chapters": [
    {
      "title": "Getting Started",
      "order": 1,
      "content": "...",
      "sections": [...]
    },
    ...
  ],
  "knowledge_graph": {
    "nodes": [...],
    "edges": [...]
  },
  "metadata": {
    "repo_name": "...",
    "is_mock": true,
    "files_analyzed": 42
  }
}
```

## API Endpoints

### 1. List All Analyses

**GET** `/api/codebases`

Returns a list of all stored codebase analyses.

**Response**:
```json
{
  "success": true,
  "count": 3,
  "analyses": [
    {
      "analysis_id": "facebook_rocksdb_20241207_025727",
      "repo_url": "https://github.com/facebook/rocksdb",
      "repo_name": "facebook_rocksdb",
      "analyzed_at": "2025-12-07T02:57:27.809406",
      "chapters_count": 3
    },
    ...
  ]
}
```

**Example**:
```bash
curl http://localhost:8080/api/codebases
```

### 2. Get Specific Analysis

**GET** `/api/codebases/{analysis_id}`

Retrieve complete analysis by ID.

**Parameters**:
- `analysis_id`: Analysis identifier (e.g., "facebook_rocksdb_20241207_025727")

**Response**:
```json
{
  "success": true,
  "analysis": {
    "repo_url": "...",
    "analyzed_at": "...",
    "summary": {...},
    "chapters": [...],
    "knowledge_graph": {...}
  }
}
```

**Example**:
```bash
curl http://localhost:8080/api/codebases/facebook_rocksdb_20241207_025727
```

### 3. Get Latest Analysis for Repo

**GET** `/api/codebases/repo/latest?repo_url={url}`

Get the most recent analysis for a specific repository.

**Parameters**:
- `repo_url`: Repository URL

**Example**:
```bash
curl "http://localhost:8080/api/codebases/repo/latest?repo_url=https://github.com/facebook/rocksdb"
```

### 4. Manually Trigger Analysis

**POST** `/api/codebases/trigger`

Manually trigger the analysis job (for testing).

**Response**:
```json
{
  "success": true,
  "message": "Codebase analysis job triggered successfully"
}
```

**Example**:
```bash
curl -X POST http://localhost:8080/api/codebases/trigger
```

## Scheduler Behavior

### Startup Behavior
- ✅ Scheduler starts automatically when app starts
- ✅ Initial analysis runs immediately on startup
- ✅ Analyzes all configured repositories

### Periodic Execution
- ⏰ Runs daily at 2 AM (configurable)
- 🔄 Analyzes all repos in `ANALYSIS_REPOS`
- 💾 Stores results with timestamp
- 📊 Keeps historical analyses

### Shutdown Behavior
- 🛑 Gracefully stops scheduler
- ✅ Completes running jobs

## Log Output

When the app starts:
```
INFO:     Started server process [22654]
INFO:     Waiting for application startup.
✅ Background scheduler started - codebase analysis will run daily
🔄 Running initial codebase analysis...
INFO:     Starting analysis for: https://github.com/facebook/rocksdb
INFO:     Analysis stored: data/codebase_analyses/facebook_rocksdb_20241207_025727.json
INFO:     Completed analysis: facebook_rocksdb_20241207_025727
...
INFO:     Application startup complete.
```

## Current Implementation (Mock Data)

### What's Working
- ✅ Periodic job scheduler
- ✅ Storage system (JSON files)
- ✅ API endpoints to retrieve analyses
- ✅ Configuration system
- ✅ Multiple repository support

### Mock Data Structure
Currently returns placeholder data with:
- Summary (overview, purpose, key components)
- Chapters (Getting Started, Core Concepts, API Reference)
- Knowledge graph (nodes and edges)
- Metadata (repo name, file count, etc.)

### Next Step: Real Analysis

Replace mock data with actual analysis:

```python
# In services/codebase_scheduler.py

async def analyze_and_store(self, repo_url: str, config: Dict = None):
    # TODO: Replace this block
    # analysis_result = self._create_mock_analysis(...)
    
    # With real analysis:
    from services.codebase_analyzer import CodebaseAnalyzer
    from services.tutorial_generator import TutorialGenerator
    
    analyzer = CodebaseAnalyzer()
    generator = TutorialGenerator(grok_client)
    
    # Analyze codebase
    analysis = await analyzer.analyze(repo_url=repo_url, ...)
    
    # Generate tutorial content
    summary = await generator.generate_summary(...)
    chapters = await generator.generate_chapters(...)
    knowledge_graph = generator.build_knowledge_graph(...)
    
    # Store results...
```

## Integration with Feature 2 (Personalized Plans)

The stored analyses will be used to create personalized weekly onboarding plans:

```python
# Future implementation
@app.post("/api/generateOnboardingPlan")
async def generate_onboarding_plan(
    profile_id: str,
    repo_url: str,
    duration_weeks: int = 4
):
    # 1. Load candidate profile (from resume analysis)
    profile = await get_profile(profile_id)
    
    # 2. Load latest codebase analysis
    codebase = scheduler_instance.get_latest_analysis(repo_url)
    
    # 3. Match candidate skills with codebase requirements
    gaps = identify_knowledge_gaps(profile, codebase)
    
    # 4. Generate week-by-week plan
    plan = generate_learning_plan(gaps, codebase["chapters"], duration_weeks)
    
    return plan
```

### Example Workflow

1. **Codebase Analysis** (Automatic, Daily):
   - System analyzes RocksDB
   - Stores chapters: "Getting Started", "Core Concepts", "API Reference"
   - Stores knowledge graph

2. **Resume Analysis** (On-demand):
   - New hire uploads resume
   - System identifies: Python ✅, C++ ❌, Database basics ✅

3. **Personalized Plan** (Generated):
   - **Week 1**: C++ fundamentals (gap identified)
   - **Week 2**: RocksDB architecture (from codebase analysis)
   - **Week 3**: API implementation (from codebase chapters)
   - **Week 4**: Advanced features

## Files Created

```
Onboarding-x-Grok/
├── config_repos.py                    # Repository configuration
├── services/
│   └── codebase_scheduler.py          # Scheduler service
├── data/
│   └── codebase_analyses/             # Storage directory
│       ├── facebook_rocksdb_*.json
│       ├── pallets_flask_*.json
│       └── tiangolo_fastapi_*.json
└── main.py                            # Updated with scheduler & endpoints
```

## Testing

### Test Endpoints Locally

```bash
# 1. List all analyses
curl http://localhost:8080/api/codebases

# 2. Get specific analysis
curl http://localhost:8080/api/codebases/facebook_rocksdb_20241207_025727

# 3. Get latest for repo
curl "http://localhost:8080/api/codebases/repo/latest?repo_url=https://github.com/facebook/rocksdb"

# 4. Manually trigger analysis
curl -X POST http://localhost:8080/api/codebases/trigger
```

### Check Stored Files

```bash
ls -lh data/codebase_analyses/
cat data/codebase_analyses/facebook_rocksdb_*.json | python3 -m json.tool
```

## Configuration Options

### Change Schedule

Edit `config_repos.py`:
```python
# Run every 6 hours
ANALYSIS_SCHEDULE = {
    "hour": "*/6",  # Every 6 hours
    "minute": 0
}

# Run every day at 9 PM
ANALYSIS_SCHEDULE = {
    "hour": 21,
    "minute": 0
}
```

### Add More Repositories

Edit `config_repos.py`:
```python
ANALYSIS_REPOS = [
    "https://github.com/facebook/rocksdb",
    "https://github.com/your-company/main-repo",
    "https://github.com/your-company/frontend-repo",
    "https://github.com/your-company/backend-repo",
]
```

### Disable Initial Analysis on Startup

In `main.py`, comment out:
```python
@app.on_event("startup")
async def startup_event():
    scheduler.start()
    # Comment this out in production:
    # await scheduled_analysis_job()
```

## Production Deployment

### Environment Variables

```bash
# Set schedule via environment (optional)
export ANALYSIS_HOUR=2
export ANALYSIS_MINUTE=0

# In config_repos.py:
ANALYSIS_SCHEDULE = {
    "hour": int(os.getenv("ANALYSIS_HOUR", 2)),
    "minute": int(os.getenv("ANALYSIS_MINUTE", 0))
}
```

### Database Migration (Future)

Replace JSON storage with database:

```python
# Instead of:
with open(storage_path, 'w') as f:
    json.dump(analysis_result, f)

# Use database:
from database import store_analysis
await store_analysis(repo_url, analysis_result)
```

## Benefits

1. **Automated Knowledge Base**: Always up-to-date codebase documentation
2. **Historical Tracking**: See how codebase evolves over time
3. **Scalable**: Easy to add more repositories
4. **Flexible**: Adjust schedule as needed
5. **Foundation for Personalization**: Powers Feature 2 (personalized plans)

## Next Steps

1. ✅ Mock data system working
2. 🔄 Replace with real codebase analysis
3. 🔜 Add database storage
4. 🔜 Implement Feature 2 (personalized plans)
5. 🔜 Add Feature 3 (Grok chatbot)

---

**Status**: ✅ Feature 1 infrastructure complete (with mock data)

**Ready for**: Integration with real codebase analysis & Feature 2 development
