# 🎯 Product Features - Complete Overview

## Product Vision

**Building the brain/knowledge graph for team-specific codebases and enabling LLM to have the right context for onboarding engineers.**

## Three Core Features

### ✅ Feature 1: Chapter-wise Information of Codebase Repos
**Status**: Implemented (with mock data infrastructure)

**Purpose**: Automatically build and maintain knowledge base of team codebases

**Implementation**:
- 🕐 Periodic background jobs (daily at 2 AM)
- 💾 Stored analyses in `data/codebase_analyses/`
- 📚 Chapter-wise tutorials generated
- 🕸️ Knowledge graphs created
- 📊 Accessible via `/api/codebases` endpoints

**Current Repositories** (configured in `config_repos.py`):
- RocksDB
- Flask
- FastAPI

**Data Structure**:
```json
{
  "summary": "Overview and key components",
  "chapters": [
    {"title": "Getting Started", "sections": [...]},
    {"title": "Core Concepts", "sections": [...]},
    {"title": "API Reference", "sections": [...]}
  ],
  "knowledge_graph": {"nodes": [...], "edges": [...]}
}
```

---

### ✅ Feature 2: Personalized Weekly Plan for Engineers
**Status**: Partially implemented (resume analysis ready)

**Purpose**: Create customized onboarding plans based on:
1. Candidate's background (from resume)
2. Codebase knowledge (from Feature 1)
3. Team mentor input

#### 2a. Resume Analysis ✅
**Implemented**: `/api/analyzeResume`

- Upload PDF resume
- Grok AI extracts:
  - Technical skills (languages, frameworks, tools)
  - Education background
  - Work experience
  - Strengths and knowledge gaps
  - Personalized recommendations

**Example Output**:
```json
{
  "candidate_name": "Elon Musk",
  "technical_skills": {
    "languages": ["JavaScript", "TypeScript", "Python", "Go"],
    "frameworks": ["React", "Node.js", "Express.js"],
    "databases": ["PostgreSQL", "Redis"]
  },
  "strengths": ["Full-stack development", "Product intuition"],
  "knowledge_gaps": ["Limited Kubernetes experience"],
  "recommended_learning_path": [...]
}
```

#### 2b. Mentor Input 🔜
**TODO**: Add endpoint for mentor/team guidelines

Mentors provide:
- Team-specific questions
- Previous challenges & solutions
- Expectations for new hire
- Key milestones

**Proposed Endpoint**:
```python
POST /api/mentorGuidelines
{
  "team": "Backend Infrastructure",
  "key_questions": [
    "Explain our caching strategy",
    "How do we handle circuit breakers?"
  ],
  "common_challenges": [
    {
  "challenge": "Understanding distributed tracing",
      "solution": "Start with Week 2 tutorial, pair with Sarah"
    }
  ],
  "expectations": {
    "week_1": "Complete dev environment setup",
    "week_4": "Ship first feature",
    "week_8": "Independent on-call"
  }
}
```

#### 2c. Plan Generation 🔜
**TODO**: Combine resume + codebase + mentor input

**Proposed Endpoint**:
```python
POST /api/generateOnboardingPlan
{
  "profile_id": "abc123",           # From resume analysis
  "repo_url": "...",                # Which codebase
  "duration_weeks": 8
}
```

**Generated Plan Example**:
```json
{
  "plan": [
    {
      "week": 1,
      "title": "Environment Setup & C++ Basics",
      "rationale": "Candidate lacks C++ (identified gap)",
      "tasks": [
        {
          "task": "Complete C++ fundamentals course",
          "estimated_hours": 10,
          "resources": ["link1", "link2"]
        },
        {
          "task": "Set up RocksDB dev environment",
          "mentor": "Sarah",
          "chapter": "Getting Started"
        }
      ]
    },
    {
      "week": 2,
      "title": "RocksDB Architecture Deep Dive",
      "rationale": "From codebase analysis - core concepts",
      "tasks": [...]
    }
  ]
}
```

---

### 🔜 Feature 3: Grok Chatbot
**Status**: Not yet implemented

**Purpose**: Interactive assistant for new hires with codebase context

**Capabilities**:
- Answer questions about the codebase
- Explain specific code sections
- Suggest learning resources
- Track onboarding progress

**Context Sources**:
1. Codebase analyses (Feature 1)
2. Candidate profile (Feature 2a)
3. Team guidelines (Feature 2b)
4. Onboarding plan (Feature 2c)

**Proposed Endpoint**:
```python
POST /api/chat
{
  "profile_id": "abc123",
  "repo_url": "...",
  "message": "How does RocksDB handle compaction?"
}
```

**Response**:
```json
{
  "answer": "RocksDB uses LSM-tree compaction...",
  "related_chapters": ["Core Concepts"],
  "code_references": ["src/db/compaction.cc"],
  "learning_resources": [...]
}
```

---

## How Features Work Together

### Complete Onboarding Flow

```
┌─────────────────────────────────────────────┐
│  DAY 0: Pre-Onboarding                      │
│  ─────────────────────                      │
│  1. HR uploads candidate resume             │
│     → /api/analyzeResume                    │
│     ← Profile created (skills, gaps)        │
│                                             │
│  2. Mentor provides team guidelines         │
│     → /api/mentorGuidelines                 │
│     ← Guidelines stored                     │
└─────────────────────────────────────────────┘
          ↓
┌─────────────────────────────────────────────┐
│  DAY 1: Onboarding Plan Generated           │
│  ─────────────────────────────              │
│  System combines:                           │
│  • Candidate profile (Feature 2a)           │
│  • Codebase analysis (Feature 1)            │
│  • Mentor guidelines (Feature 2b)           │
│                                             │
│  → /api/generateOnboardingPlan              │
│  ← 8-week personalized plan                 │
└─────────────────────────────────────────────┘
          ↓
┌─────────────────────────────────────────────┐
│  WEEKS 1-8: Active Onboarding              │
│  ────────────────────────────               │
│  New hire:                                  │
│  • Follows weekly plan                      │
│  • Reads chapter-wise tutorials             │
│  • Uses Grok chatbot for questions          │
│  • Completes assignments                    │
│                                             │
│  Mentor:                                    │
│  • Tracks progress                          │
│  • Provides feedback                        │
│  • Adjusts plan as needed                   │
└─────────────────────────────────────────────┘
```

### Data Flow Diagram

```
              Codebase Repos
                   │
                   ↓
   ┌───────────────────────────────┐
   │  Feature 1: Analysis Job      │
   │  (Scheduled, Daily)           │
   └───────────────────────────────┘
                   │
                   ↓
           [Codebase Analyses]
           • Chapters
           • Knowledge Graphs
                   │
                   │
    Resume PDF     │      Mentor Input
        │          │          │
        ↓          ↓          ↓
   ┌────────────────────────────────┐
   │  Feature 2: Plan Generator     │
   │  (On-Demand)                   │
   └────────────────────────────────┘
                   │
                   ↓
         [Onboarding Plan]
         • Week-by-week
         • Personalized
                   │
                   ↓
   ┌────────────────────────────────┐
   │  Feature 3: Grok Chatbot       │
   │  (Interactive)                 │
   └────────────────────────────────┘
                   │
                   ↓
           [Learning Progress]
```

---

## Current Implementation Status

### ✅ Completed

1. **Resume Analysis**
   - PDF upload and parsing
   - Grok AI integration (grok-3 model)
   - Skill extraction
   - Gap identification
   - Personalized recommendations

2. **Codebase Analysis Infrastructure**
   - Periodic job scheduler
   - Storage system (JSON files)
   - API endpoints for retrieval
   - Mock data generation
   - Multiple repository support

3. **Deployment**
   - FastAPI application
   - Google Cloud Run
   - Background scheduler
   - CORS enabled
   - API documentation

### 🔄 In Progress

1. **Real Codebase Analysis**
   - TODO: Replace mock data with actual analysis
   - Services exist: `codebase_analyzer.py`, `tutorial_generator.py`
   - Need to connect to scheduler

### 🔜 Not Yet Started

1. **Mentor Guidelines Input**
   - Endpoint design needed
   - Storage schema needed
   - Integration with plan generator

2. **Onboarding Plan Generator**
   - Matching algorithm (skills vs requirements)
   - Week-by-week planning logic
   - Resource recommendations

3. **Grok Chatbot**
   - Chat endpoint
   - Context management
   - Progress tracking
   - Knowledge base integration

---

## API Endpoints Summary

### Feature 1: Codebase Knowledge Base

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/codebases` | GET | List all analyses |
| `/api/codebases/{id}` | GET | Get specific analysis |
| `/api/codebases/repo/latest` | GET | Latest for a repo |
| `/api/codebases/trigger` | POST | Manual trigger |

### Feature 2a: Resume Analysis

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/analyzeResume` | POST | Upload & analyze resume |
| `/api/getProfile/{id}` | GET | Retrieve profile |

### Feature 2b: Mentor Guidelines (TODO)

| Endpoint | Method | Purpose |
|----------|--------|---------|  
| `/api/mentorGuidelines` | POST | Submit guidelines |
| `/api/mentorGuidelines/{team}` | GET | Get team guidelines |

### Feature 2c: Plan Generation (TODO)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/generateOnboardingPlan` | POST | Create personalized plan |
| `/api/onboardingPlans/{id}` | GET | Retrieve plan |
| `/api/onboardingPlans/{id}/progress` | POST | Update progress |

### Feature 3: Chatbot (TODO)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/chat` | POST | Send message |
| `/api/chat/history/{profile_id}` | GET | Chat history |

---

## Data Storage

```
data/
├── resumes/                    # Uploaded PDF resumes
├── analyzed_profiles/          # Resume analysis results
├── codebase_analyses/          # Periodic codebase analyses ✅
├── mentor_guidelines/          # Team-specific guidelines 🔜
├── onboarding_plans/          # Generated plans 🔜
└── chat_history/              # Chatbot conversations 🔜
```

---

## Configuration Files

```
config.py              # API keys, models (Grok)
config_repos.py        # Repositories to analyze ✅
config_teams.py        # Team configurations 🔜
```

---

## Next Implementation Steps

### Step 1: Connect Real Codebase Analysis
```python
# In services/codebase_scheduler.py
# Replace _create_mock_analysis with:
analyzer = CodebaseAnalyzer()
tutorial_gen = TutorialGenerator(grok_client)
result = await analyzer.analyze(repo_url)
summary = await tutorial_gen.generate_summary(result)
chapters = await tutorial_gen.generate_chapters(result)
```

### Step 2: Add Mentor Guidelines Endpoint
```python
@app.post("/api/mentorGuidelines")
async def submit_mentor_guidelines(guidelines: MentorGuidelines):
    # Store in data/mentor_guidelines/
    pass
```

### Step 3: Implement Plan Generator
```python
@app.post("/api/generateOnboardingPlan")
async def generate_plan(request: PlanRequest):
    # 1. Load profile
    # 2. Load codebase analysis
    # 3. Load team guidelines
    # 4. Match skills → Generate weeks
    pass
```

### Step 4: Add Grok Chatbot
```python
@app.post("/api/chat")
async def chat(message: ChatMessage):
    # Build context from analyses + profile
    # Call Grok with context
    # Return answer + references
    pass
```

---

## Testing the Current System

```bash
# 1. Analyze a resume
curl -X POST http://localhost:8080/api/analyzeResume \
  -F "resume=@examples/elon_musk_junior_backend_resume_one_page.pdf" \
  -F "candidate_email=elon@test.com"

# Response: profile_id = "abc123"

# 2. List codebase analyses
curl http://localhost:8080/api/codebases

# 3. Get RocksDB analysis
curl "http://localhost:8080/api/codebases/repo/latest?repo_url=https://github.com/facebook/rocksdb"

# 4. (Future) Generate onboarding plan
# curl -X POST http://localhost:8080/api/generateOnboardingPlan \
#   -H "Content-Type: application/json" \
#   -d '{"profile_id": "abc123", "repo_url": "...", "duration_weeks": 8}'
```

---

## Success Metrics (Future)

1. **Time to First Commit**: Reduce from 4 weeks → 2 weeks
2. **Onboarding Satisfaction**: Track new hire survey scores
3. **Knowledge Retention**: Quiz scores at week 4 and week 8
4. **Mentor Time Saved**: Hours saved by automated plan generation
5. **Chatbot Effectiveness**: % of questions answered without human intervention

---

## Summary

| Feature | Status | Infrastructure | Next Step |
|---------|--------|----------------|-----------|
| **1. Codebase Knowledge** | ✅ 70% | Scheduler ✅, Storage ✅, APIs ✅ | Connect real analysis |
| **2a. Resume Analysis** | ✅ 100% | Grok ✅, Storage ✅, APIs ✅ | None |
| **2b. Mentor Input** | 🔜 0% | - | Design & implement |
| **2c. Plan Generator** | 🔜 0% | - | Design & implement |
| **3. Grok Chatbot** | 🔜 0% | Grok client ✅ | Design & implement |

**Overall Progress**: 🟢 Feature 1 infrastructure complete, Feature 2a complete, Ready for Feature 2b-c and Feature 3

---

**Current Deliverable**: ✅ Automated codebase analysis + AI-powered resume analysis

**Next Milestone**: 🎯 Combine them into personalized onboarding plans
