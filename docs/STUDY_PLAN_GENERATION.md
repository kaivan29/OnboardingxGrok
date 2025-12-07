# 🎓 Study Plan Generation - Feature Documentation

## Overview

The Study Plan Generator creates personalized weekly onboarding plans for new engineers by combining:
1. **User Profile** - Analysis from resume upload (skills, experience, knowledge gaps)
2. **Codebase Analysis** - Structured chapters and concepts from the target repository
3. **AI-Powered Personalization** - Grok AI tailors content to address individual needs

The output matches the format expected by the frontend (`client/lib/data/week-content.ts`), enabling seamless integration.

## API Endpoint

### POST `/api/generateStudyPlan`

Generate a personalized study plan based on user profile and codebase analysis.

**Request Format:** `multipart/form-data`

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `profile_id` | string | Yes | User profile ID from resume analysis |
| `repo_url` | string | Yes | Repository URL (e.g., `https://github.com/facebook/rocksdb`) |
| `duration_weeks` | integer | No | Number of weeks (default: 4) |
| `use_ai` | boolean | No | Use AI generation (default: true) |

**Example Request:**

```bash
curl -X POST http://localhost:8080/api/generateStudyPlan \
  -F "profile_id=abc123def456" \
  -F "repo_url=https://github.com/facebook/rocksdb" \
  -F "duration_weeks=4" \
  -F "use_ai=true"
```

**Success Response (200):**

```json
{
  "success": true,
  "profile_id": "abc123def456",
  "repo_url": "https://github.com/facebook/rocksdb",
  "generated_at": "2025-12-07T10:30:00",
  "duration_weeks": 4,
  "plan_id": "abc123def456_rocksdb_20251207_103000",
  "plan": {
    "weeks": [
      {
        "weekId": 1,
        "title": "Foundations & Setup",
        "status": "start",
        "overview": "# Overview\n\nMarkdown content...",
        "chapters": [
          {
            "id": "environment-setup",
            "title": "Environment Setup",
            "content": "# Environment Setup\n\nDetailed markdown...",
            "subItems": [
              {"id": "prerequisites", "title": "Prerequisites"},
              {"id": "installation", "title": "Installation"}
            ]
          }
        ],
        "tasks": [
          {
            "id": "task-1-1",
            "title": "Complete Environment Setup",
            "description": "Set up your local development environment...",
            "assignedBy": "Onboarding Team",
            "timeAgo": "1 hr ago",
            "progress": 0
          }
        ]
      }
    ]
  }
}
```

**Error Responses:**

### 400 Bad Request
```json
{
  "detail": "Profile not found: abc123"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Failed to generate study plan: <error details>"
}
```

## Architecture

### Components

```
services/study_plan_generator.py
├── StudyPlanGenerator (main class)
│   ├── get_profile() - Load user profile
│   ├── get_latest_codebase_analysis() - Load codebase data
│   ├── generate_plan_with_grok() - AI-powered generation
│   └── generate_fallback_plan() - Template-based generation
└── get_generator() - Singleton accessor
```

### Data Flow

```
1. Resume Upload
   └─> /api/analyzeResume
       └─> Profile saved: data/analyzed_profiles/{profile_id}.json

2. Codebase Analysis (scheduled daily)
   └─> Periodic Job
       └─> Analysis saved: data/codebase_analyses/{repo}_{timestamp}.json

3. Study Plan Generation
   └─> /api/generateStudyPlan
       ├─> Load profile from step 1
       ├─> Load latest codebase analysis from step 2
       ├─> Generate plan (AI or fallback)
       └─> Plan saved: data/study_plans/{plan_id}.json
```

## Output Format

The generated plan matches the TypeScript interface in `client/lib/data/week-content.ts`:

```typescript
type WeekContent = {
  weekId: number;
  title: string;
  status: "completed" | "continue" | "start" | "locked";
  overview: string; // Markdown
  chapters: Chapter[];
  tasks: WeeklyTask[];
}

type Chapter = {
  id: string;
  title: string;
  content: string; // Markdown
  subItems?: SubItem[];
}

type WeeklyTask = {
  id: string;
  title: string;
  description: string;
  assignedBy: string;
  timeAgo: string;
  progress: number; // 0-100
}
```

## Generation Modes

### 1. AI-Powered Generation (Recommended)

**When:** Grok API key is configured

**How it works:**
- Analyzes user's knowledge gaps and strengths
- Maps codebase complexity to user's experience level
- Creates custom learning paths addressing specific needs
- Generates unique markdown content for each chapter
- Assigns relevant tasks based on codebase structure

**Advantages:**
- Highly personalized
- Adapts to individual learning needs
- Context-aware task generation
- Natural language explanations

**Example:**
```python
result = await generator.generate_study_plan(
    profile_id="abc123",
    repo_url="https://github.com/facebook/rocksdb",
    duration_weeks=4,
    use_ai=True  # Use AI
)
```

### 2. Fallback Generation

**When:** Grok API not available or `use_ai=False`

**How it works:**
- Uses template-based approach
- Incorporates codebase chapters directly
- Generic but structured content
- Standard task assignments

**Advantages:**
- Works without API key
- Consistent structure
- Fast generation
- Predictable output

**Example:**
```python
result = await generator.generate_study_plan(
    profile_id="abc123",
    repo_url="https://github.com/facebook/rocksdb",
    duration_weeks=4,
    use_ai=False  # Use fallback
)
```

## Usage Example

### Complete Workflow

```python
import requests

# Step 1: Analyze Resume
with open('resume.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8080/api/analyzeResume',
        files={'resume': f},
        data={'candidate_email': 'john@example.com'}
    )
    profile_id = response.json()['profile_id']

# Step 2: Generate Study Plan
response = requests.post(
    'http://localhost:8080/api/generateStudyPlan',
    data={
        'profile_id': profile_id,
        'repo_url': 'https://github.com/facebook/rocksdb',
        'duration_weeks': 4,
        'use_ai': True
    }
)

plan = response.json()

# Step 3: Use in Frontend
# The 'plan' object can be directly used by the frontend
weeks = plan['plan']['weeks']
```

### Testing

Run the test script:

```bash
python3 examples/test_study_plan_generator.py
```

This will:
1. Upload Elon Musk's sample resume
2. Generate a personalized plan for RocksDB
3. Display the plan structure
4. Save the full plan to `examples/output/study_plan_{profile_id}.json`

## Frontend Integration

### Using the Generated Plan

The generated plan can be directly consumed by the frontend:

```typescript
// Fetch the study plan
const response = await fetch('/api/generateStudyPlan', {
  method: 'POST',
  body: formData
});

const result = await response.json();
const weeks: WeekContent[] = result.plan.weeks;

// Use with existing components
<WeekSelector weeks={weeks} />
<WeekContentArea currentWeek={weeks[0]} />
```

### Storage

Plans are stored in:
```
data/study_plans/
└── {profile_id}_{repo_name}_{timestamp}.json
```

Each file contains:
- Metadata (profile_id, repo_url, generated_at)
- Complete week-by-week plan
- Ready for frontend consumption

## Customization

### Adjust Week Count

```python
# Generate 8-week plan
result = await generator.generate_study_plan(
    profile_id="abc123",
    repo_url="https://github.com/facebook/rocksdb",
    duration_weeks=8  # Extended plan
)
```

### Modify AI Prompt

Edit `services/study_plan_generator.py`:

```python
async def generate_plan_with_grok(self, profile, codebase, duration_weeks):
    # Customize the prompt to change generation behavior
    prompt = f"""Generate a {duration_weeks}-week plan with focus on:
    - Hands-on coding (70%)
    - Theory and concepts (30%)
    ...
    """
```

### Extend Fallback Templates

```python
def generate_fallback_plan(self, profile, codebase, duration_weeks):
    # Add custom week templates
    weeks.append({
        "weekId": 5,
        "title": "Advanced Performance Tuning",
        ...
    })
```

## Best Practices

### 1. Profile Quality
- Ensure resume analysis is complete before generating plans
- Review knowledge gaps for accuracy
- Update profiles when candidates provide more information

### 2. Codebase Analysis
- Keep codebase analyses up to date
- Trigger manual analysis before generating plans if repo has changed
- Ensure analyses contain rich chapter content

### 3. Performance
- Cache generated plans
- Reuse plans for similar profiles
- Generate plans asynchronously for long-running tasks

### 4. Monitoring
- Track plan generation success rates
- Monitor AI API usage
- Collect feedback on plan quality

## Troubleshooting

### "Profile not found"
```bash
# Verify profile exists
curl http://localhost:8080/api/getProfile/{profile_id}

# Re-analyze resume if needed
curl -X POST http://localhost:8080/api/analyzeResume \
  -F "resume=@resume.pdf"
```

### "No codebase analysis found"
```bash
# Check available analyses
curl http://localhost:8080/api/codebases

# Trigger manual analysis
curl -X POST http://localhost:8080/api/codebases/trigger
```

### AI Generation Fails
- Falls back to template generation automatically
- Check Grok API key configuration
- Review API logs for specific errors

## Future Enhancements

- [ ] Progress tracking integration
- [ ] Adaptive plan adjustments based on completion
- [ ] Mentor feedback incorporation
- [ ] Multi-repository plans
- [ ] Team-specific customizations
- [ ] Learning resource recommendations
- [ ] Skill assessment integration

## Related Documentation

- [Resume API Documentation](./RESUME_API.md)
- [Codebase Analysis](./PERIODIC_ANALYSIS.md)
- [Product Features](./PRODUCT_FEATURES.md)
- [API Reference](./API_REFERENCE.md)
