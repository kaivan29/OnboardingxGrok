# Complete Feature Flow: Resume Upload → AI Analysis → Personalized Study Plan

## 📝 Overview

This document describes the complete implementation of the personalized onboarding feature, which includes:

1. **Resume Upload** (Frontend) ✅ DONE
2. **Resume Analysis with Grok AI** (Backend) ✅ DONE
3. **Codebase Analysis** (Backend) ✅ DONE
4. **Study Plan Generation** (Backend) ✅ DONE
5. **Dashboard Display** (Frontend) ✅ DONE

---

## 🔄 Complete User Flow

### Step 1: User Uploads Resume

**Location:** `/client/app/onboarding/page.tsx`

```
User visits /onboarding
  → Uploads PDF resume
  → Frontend calls: POST /api/analyzeResume
  → Shows loading animation (7 steps)
```

**API Call:**
```typescript
const result = await onboardingApi.uploadResume(file);
// Sends: resume file + repo_url + generate_plan=true
```

---

### Step 2: Backend Analyzes Resume

**Location:** `/main.py` - `analyze_resume()` endpoint

**What Happens:**

1. **File Processing**
   - Receives PDF file
   - Calculates file hash (MD5) for duplicate detection
   - Stores in `data/resumes/{hash}_{filename}.pdf`

2. **Text Extraction**
   - Uses PyPDF2 to extract text from PDF
   - Function: `extract_text_from_pdf()`

3. **Grok AI Analysis**
   - Sends resume text to Grok API
   - Function: `analyze_resume_with_grok(resume_text)`
   - Prompt asks Grok to extract:
     - Candidate name
     - Years of experience
     - Education
     - Technical skills (languages, frameworks, tools, databases)
     - Experience summary
     - Strengths
     - Knowledge gaps
     - Recommended learning path

4. **Profile Storage**
   - Creates `profile_id` (first 12 chars of file hash)
   - Stores in `data/analyzed_profiles/{profile_id}.json`
   - Structure:
     ```json
     {
       "profile_id": "abc123...",
       "candidate_email": "user@example.com",
       "uploaded_at": "2024-12-07T...",
       "resume_filename": "john_doe_resume.pdf",
       "file_hash": "abc123...",
       "analysis": {
         "candidate_name": "John Doe",
         "experience_years": 5,
         "technical_skills": {...},
         ...
       }
     }
     ```

---

### Step 3: Codebase Analysis (Already Done)

**Location:** `/services/codebase_analyzer.py` + `/services/codebase_scheduler.py`

**How it Works:**

- **Scheduled Job**: Runs daily at 2 AM (configurable)
- **What it analyzes**: RocksDB codebase (configurable via `config_repos.py`)
- **Storage**: `data/codebase_analyses/{repo}_{timestamp}.json`

**Analysis Output:**
```json
{
  "analysis_id": "facebook_rocksdb_20241207_020000",
  "repo_url": "https://github.com/facebook/rocksdb",
  "analyzed_at": "2024-12-07T02:00:00",
  "summary": {
    "project_name": "RocksDB",
    "description": "...",
    "tech_stack": [...],
    "complexity_level": "advanced"
  },
  "chapters": [
    {
      "chapter_id": 1,
      "title": "Getting Started with RocksDB",
      "content": "...",
      "code_examples": [...]
    }
  ],
  "knowledge_graph": {
    "key_concepts": [...],
    "dependencies": {...}
  }
}
```

---

### Step 4: Study Plan Generation

**Location:** `/services/study_plan_generator.py`

**Triggered by:** 
- Automatically when `generate_plan=true` in resume upload
- Or manually via: `POST /generateStudyPlan`

**How it Works:**

1. **Load User Profile**
   ```python
   profile = generator.get_profile(profile_id)
   # Gets resume analysis from data/analyzed_profiles/
   ```

2. **Load Latest Codebase Analysis**
   ```python
   codebase = generator.get_latest_codebase_analysis(repo_url)
   # Gets latest analysis from data/codebase_analyses/
   ```

3. **Generate Personalized Plan**
   - **With AI** (if Grok available):
     - Combines profile + codebase
     - Sends to Grok with detailed prompt
     - Asks for week-by-week learning plan
   
   - **Fallback** (without AI):
     - Uses template-based generation
     - Matches chapters to user's experience level
     - Distributes across weeks

4. **Plan Structure** (matches frontend format):
   ```json
   {
     "weeks": [
       {
         "weekId": 1,
         "title": "Foundation & Environment Setup",
         "description": "...",
         "chapters": [
           {
             "chapterId": "1.1",
             "title": "Understanding RocksDB Architecture",
             "content": "...",
             "readingTime": "15-20 minutes",
             "difficulty": "intermediate"
           }
         ],
         "tasks": [
           {
             "taskId": "task-1-1",
             "title": "Set up RocksDB development environment",
             "description": "...",
             "type": "setup",
             "estimatedTime": "2 hours",
             "priority": "high"
           }
         ]
       }
     ]
   }
   ```

5. **Storage**
   - Saves to `data/study_plans/{plan_id}.json`
   - `plan_id` = `{profile_id}_{repo_hash}_{timestamp}`

---

### Step 5: Frontend Displays Results

#### A. Onboarding Page Shows Preview

**Location:** `/client/app/onboarding/page.tsx`

After upload completes:
1. Shows success message
2. Displays profile summary:
   - Candidate name
   - Years of experience
   - Technical skills (colored badges)
   - Knowledge gaps
3. Shows study plan preview:
   - Grid of week cards
   - Shows: week number, title, chapter count, task count
4. User clicks "Start My Onboarding Journey"
   - Stores `profile_id` and `plan_id` in localStorage
   - Redirects to `/dashboard`

#### B. Dashboard Loads Personalized Plan

**Location:** `/client/app/dashboard/page.tsx`

On page load:
1. **Reads localStorage**
   ```typescript
   const profileId = localStorage.getItem('profile_id');
   const planId = localStorage.getItem('plan_id');
   ```

2. **Fetches User Profile**
   ```typescript
   const profile = await onboardingApi.getProfile(profileId);
   setUserFullName(profile.analysis.candidate_name);
   ```

3. **Fetches Study Plan**
   ```typescript
   const studyPlan = await onboardingApi.getStudyPlan({
     profile_id: profileId,
     plan_id: planId
   });
   ```

4. **Transforms Data for Display**
   - Maps weeks to module cards
   - Assigns status: "continue" (week 1), "start" (middle weeks), "locked" (last week)
   - Calculates progress percentage
   - Counts tasks from current week

5. **Renders Dashboard**
   - Personalized greeting: "Welcome back, {FirstName}!"
   - Progress bar showing completion
   - Tasks due this week
   - Week cards (clickable → `/dashboard/week/{weekId}`)

---

## 🔌 API Endpoints Reference

### Resume & Profile Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/analyzeResume` | Upload resume, analyze, generate plan |
| GET | `/api/getProfile/{profile_id}` | Get profile analysis |

**Upload Resume:**
```bash
curl -X POST http://localhost:8080/api/analyzeResume \
  -F "resume=@resume.pdf" \
  -F "candidate_email=user@example.com" \
  -F "repo_url=https://github.com/facebook/rocksdb" \
  -F "generate_plan=true"
```

**Response:**
```json
{
  "success": true,
  "profile_id": "a1b2c3d4e5f6",
  "is_duplicate": false,
  "message": "Resume analyzed successfully",
  "analysis": {
    "candidate_name": "John Doe",
    "experience_years": 5,
    ...
  },
  "study_plan": {
    "success": true,
    "plan_id": "...",
    "duration_weeks": 4,
    "plan": { "weeks": [...] }
  }
}
```

### Study Plan Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/getStudyPlanByProfile/{profile_id}` | Get latest plan for profile |
| GET | `/api/getStudyPlan/{plan_id}` | Get specific plan by ID |
| POST | `/api/generateStudyPlan` | Generate new plan |

**Generate Study Plan:**
```bash
curl -X POST http://localhost:8080/api/generateStudyPlan \
  -F "profile_id=a1b2c3d4e5f6" \
  -F "repo_url=https://github.com/facebook/rocksdb" \
  -F "duration_weeks=4" \
  -F "use_ai=true"
```

### Codebase Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/codebases` | List all analyzed codebases |
| GET | `/api/codebases/{analysis_id}` | Get specific analysis |
| GET | `/api/codebases/repo/latest?repo_url={url}` | Get latest for repo |
| POST | `/api/triggerCodebaseAnalysis` | Manually trigger analysis |

---

## 📂 Data Storage

```
data/
├── resumes/
│   └── {hash}_{filename}.pdf          # Uploaded resume PDFs
├── analyzed_profiles/
│   └── {profile_id}.json              # User profile + AI analysis
├── codebase_analyses/
│   └── {repo}_{timestamp}.json        # Codebase analysis results
└── study_plans/
    └── {plan_id}.json                 # Personalized study plans
```

---

## 🔑 Environment Variables

```bash
# Required for AI features
GROK_API_KEY=your_grok_api_key_here

# Optional (has defaults)
PORT=8080
```

**Get Grok API Key:** https://console.x.ai/

---

## 🎯 Key Features

### ✅ Duplicate Detection
- Uses MD5 hash of resume content
- If same resume uploaded again → returns existing profile
- Prevents redundant AI analysis

### ✅ Personalization
- Study plan adapts to:
  - User's experience level
  - Known technologies
  - Identified knowledge gaps
  - Codebase complexity

### ✅ AI-Powered or Fallback
- **With Grok API**: Intelligent, context-aware plans
- **Without API**: Template-based generation still works

### ✅ Scheduled Analysis
- RocksDB codebase analyzed daily
- Always has fresh analysis for new users
- Can manually trigger via API

---

## 🧪 Testing the Complete Flow

### 1. Test Resume Upload

```bash
# Use example resume
cd /Users/zy/Desktop/Onboarding-x-Grok
python3 examples/test_resume_api.py
```

Or use the frontend:
1. Visit http://localhost:3000/onboarding
2. Upload a PDF resume
3. Wait for analysis (30-60 seconds)
4. Review results
5. Click "Start My Onboarding Journey"

### 2. Verify Data Storage

```bash
# Check profile was created
ls -la data/analyzed_profiles/

# Check study plan was created
ls -la data/study_plans/

# View profile JSON
cat data/analyzed_profiles/{profile_id}.json | jq
```

### 3. Test Dashboard

1. Visit http://localhost:3000/dashboard
2. Should see your name from resume
3. Should see personalized week cards
4. Click on "Week 1" card
5. Should navigate to week detail page

---

## 🐛 Troubleshooting

### Dashboard shows "Please upload your resume first"
- **Issue**: No `profile_id` in localStorage
- **Fix**: Go to `/onboarding` and upload a resume

### Analysis returns mock data
- **Issue**: `GROK_API_KEY` not set
- **Fix**: Add to `.env` file or environment
- **Note**: System still works with fallback data

### "Profile not found" error
- **Issue**: Profile file doesn't exist
- **Check**: `data/analyzed_profiles/` directory
- **Fix**: Re-upload resume

### Study plan not showing in dashboard
- **Issue**: Plan generation failed or localStorage cleared
- **Check**: Browser console for errors
- **Fix**: Re-upload resume with `generate_plan=true`

---

## 📊 Data Flow Diagram

```
User Uploads Resume (PDF)
         ↓
Extract Text (PyPDF2)
         ↓
Grok AI Analysis
         ↓
Save Profile (data/analyzed_profiles/)
         ↓
Load Codebase Analysis (data/codebase_analyses/)
         ↓
Generate Study Plan (Grok AI or Fallback)
         ↓
Save Study Plan (data/study_plans/)
         ↓
Return to Frontend
         ↓
Store profile_id + plan_id (localStorage)
         ↓
Dashboard Loads Data
         ↓
Display Personalized Learning Path
```

---

## 🚀 Next Steps

### Possible Enhancements:

1. **Progress Tracking**
   - Mark chapters as complete
   - Update progress percentage
   - Save to backend

2. **Multiple Codebases**
   - Let users choose which codebase to learn
   - Generate plans for different repos

3. **Team Management**
   - Admin dashboard for managers
   - View team member progress
   - Assign specific learning paths

4. **Assessments**
   - Quiz at end of each week
   - Validate learning
   - Adjust next week based on results

5. **Notifications**
   - Email reminders for tasks
   - Weekly progress summaries
   - Slack integration

---

## 📖 Related Documentation

- [Resume API Documentation](RESUME_API.md)
- [Study Plan Quickstart](STUDY_PLAN_QUICKSTART.md)
- [Codebase Summary](CODEBASE_SUMMARY.md)
- [FastAPI Migration Success](FASTAPI_MIGRATION_SUCCESS.md)

---

**Last Updated:** December 7, 2024  
**Status:** ✅ Feature Complete & Integrated
