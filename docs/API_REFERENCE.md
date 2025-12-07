# Complete API Reference

## Base URL

**Local Development:**
```
http://localhost:8080
```

**Production (Google Cloud Run):**
```
https://onboarding-wiki-api-197454585336.us-central1.run.app
```

---

## Endpoints

### 1. Health Check

**GET** `/`

Simple health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

---

### 2. Get Codebase Wiki Summary

**GET** `/api/getCodeBaseSummary`

Retrieve comprehensive wiki documentation for a GitHub repository.

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `codebase_url` | string | Yes | Canonical GitHub repository URL |

**Example Request:**
```bash
curl "http://localhost:8080/api/getCodeBaseSummary?codebase_url=https://github.com/facebook/rocksdb"
```

**Success Response (200):**
```json
{
  "wiki": {
    "meta": {...},
    "summary": {...},
    "architecture": {...},
    "workflows": [...],
    "modules": [...],
    "operational_readiness": {...},
    "getting_started": {...},
    "faq": [...]
  }
}
```

**Error Responses:**
- `400 Bad Request`: Missing `codebase_url` parameter
  ```json
  {"error": "missing codebase_url"}
  ```
- `404 Not Found`: Codebase not indexed
  ```json
  {"error": "codebase not indexed"}
  ```

**Available Repositories (Prototype):**
- `https://github.com/facebook/rocksdb`

---

### 3. Analyze Resume

**POST** `/api/analyzeResume`

Upload and analyze a candidate's resume using Grok AI.

**Content-Type:** `multipart/form-data`

**Form Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `resume` | file | Yes | PDF file of candidate's resume (max 10MB) |
| `candidate_email` | string | No | Email for profile identification |

**Example Requests:**

**cURL:**
```bash
curl -X POST http://localhost:8080/api/analyzeResume \
  -F "resume=@/path/to/resume.pdf" \
  -F "candidate_email=candidate@example.com"
```

**Python:**
```python
import requests

files = {'resume': open('resume.pdf', 'rb')}
data = {'candidate_email': 'candidate@example.com'}

response = requests.post(
    'http://localhost:8080/api/analyzeResume',
    files=files,
    data=data
)
```

**JavaScript:**
```javascript
const formData = new FormData();
formData.append('resume', fileInput.files[0]);
formData.append('candidate_email', 'candidate@example.com');

const response = await fetch('/api/analyzeResume', {
  method: 'POST',
  body: formData
});
```

**Success Response (200):**
```json
{
  "success": true,
  "profile_id": "a1b2c3d4e5f6",
  "message": "Resume analyzed successfully",
  "analysis": {
    "candidate_name": "John Doe",
    "experience_years": 5,
    "education": [
      {
        "degree": "Bachelor of Science in Computer Science",
        "institution": "Stanford University",
        "graduation_year": 2018
      }
    ],
    "technical_skills": {
      "languages": ["Python", "JavaScript", "Java"],
      "frameworks": ["React", "Flask", "Django"],
      "tools": ["Git", "Docker", "AWS"],
      "databases": ["PostgreSQL", "MongoDB"]
    },
    "experience_summary": [
      {
        "role": "Senior Software Engineer",
        "company": "Tech Corp",
        "duration": "2020 - Present",
        "technologies": ["Python", "AWS"],
        "key_achievements": [
          "Built microservices architecture"
        ]
      }
    ],
    "strengths": [
      "Strong backend development",
      "Cloud platform experience"
    ],
    "knowledge_gaps": [
      "Limited ML experience"
    ],
    "recommended_learning_path": [
      "Study distributed systems",
      "Learn Kubernetes"
    ]
  }
}
```

**Error Responses:**
- `400 Bad Request`:
  ```json
  {
    "error": "No resume file provided"
  }
  ```
  Possible error messages:
  - `"No resume file provided"` - Missing file
  - `"No file selected"` - Empty filename
  - `"Only PDF files are allowed"` - Invalid file type
  - `"File size exceeds maximum 10MB"` - File too large
  - `"Could not extract sufficient text from PDF"` - PDF parsing failed

- `500 Internal Server Error`:
  ```json
  {
    "error": "Internal server error: <details>"
  }
  ```

---

### 4. Get Candidate Profile

**GET** `/api/getProfile/{profile_id}`

Retrieve a previously analyzed candidate profile.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `profile_id` | string | Yes | Unique profile identifier from analyzeResume response |

**Example Request:**
```bash
curl "http://localhost:8080/api/getProfile/a1b2c3d4e5f6"
```

**Success Response (200):**
```json
{
  "profile_id": "a1b2c3d4e5f6",
  "candidate_email": "candidate@example.com",
  "uploaded_at": "2024-12-07T00:00:00.000000",
  "resume_filename": "john_doe_resume.pdf",
  "analysis": {
    // Same structure as analyzeResume response
  }
}
```

**Error Responses:**
- `404 Not Found`:
  ```json
  {
    "error": "Profile not found"
  }
  ```

- `500 Internal Server Error`:
  ```json
  {
    "error": "Failed to load profile: <details>"
  }
  ```

---

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Grok API Key (optional for testing)
GROK_API_KEY=your_grok_api_key_here

# Server Port (auto-set by Cloud Run)
PORT=8080
```

### Getting a Grok API Key

1. Visit [https://console.x.ai/](https://console.x.ai/)
2. Create an account
3. Generate an API key
4. Add to `.env` file

**Note:** The API works without a Grok key (uses mock data) for development.

---

## Rate Limits & Constraints

**File Upload Limits:**
- Maximum file size: 10MB
- Allowed formats: PDF only
- Maximum concurrent uploads: No limit (currently)

**API Rate Limits:**
- None (currently)
- Production should implement rate limiting

---

## Complete Workflow Example

### Onboarding a New Engineer

```python
import requests

API_URL = "http://localhost:8080"

# Step 1: Analyze the candidate's resume
with open('candidate_resume.pdf', 'rb') as f:
    files = {'resume': f}
    data = {'candidate_email': 'newengineer@company.com'}
    
    response = requests.post(f"{API_URL}/api/analyzeResume", files=files, data=data)
    profile = response.json()

profile_id = profile['profile_id']
analysis = profile['analysis']

print(f"Candidate: {analysis['candidate_name']}")
print(f"Experience: {analysis['experience_years']} years")
print(f"Skills: {analysis['technical_skills']['languages']}")

# Step 2: Get the codebase wiki for the project they'll work on
wiki_response = requests.get(
    f"{API_URL}/api/getCodeBaseSummary",
    params={'codebase_url': 'https://github.com/facebook/rocksdb'}
)
wiki = wiki_response.json()['wiki']

# Step 3: Match candidate background with codebase
print("\nCodebase:", wiki['meta']['name'])
print("Languages:", wiki['meta']['language'])

# Step 4: Create personalized onboarding plan
# (Future implementation - combine profile + wiki)
strengths = set(analysis['technical_skills']['languages'])
project_langs = set(wiki['meta']['language'])

needs_to_learn = project_langs - strengths
print(f"\nCandidate should learn: {needs_to_learn}")

# Step 5: Retrieve profile later if needed
stored_profile = requests.get(f"{API_URL}/api/getProfile/{profile_id}")
print(f"\nProfile retrieved: {stored_profile.json()['uploaded_at']}")
```

---

## Authentication

**Current Status:** None (open API)

**Production Recommendations:**
- Implement API key authentication
- Add OAuth 2.0 for user-based access
- Use JWT tokens for session management
- Restrict resume upload to authenticated users
- Add role-based access control (RBAC)

---

## CORS

Cross-Origin Resource Sharing (CORS) is **enabled** for all origins.

This allows frontend applications hosted on different domains to call the API.

---

## Error Handling

All endpoints follow this error response format:

```json
{
  "error": "Human-readable error message"
}
```

HTTP Status Codes:
- `200 OK` - Success
- `400 Bad Request` - Invalid input
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Testing

### Health Check
```bash
curl http://localhost:8080/
```

### Get Wiki
```bash
curl "http://localhost:8080/api/getCodeBaseSummary?codebase_url=https://github.com/facebook/rocksdb" | python3 -m json.tool
```

### Analyze Resume
```bash
curl -X POST http://localhost:8080/api/analyzeResume \
  -F "resume=@resume.pdf" \
  -F "candidate_email=test@example.com"
```

### Get Profile
```bash
curl http://localhost:8080/api/getProfile/YOUR_PROFILE_ID
```

---

## Documentation Links

- [Full README](../README.md)
- [Deployment Guide](DEPLOYMENT.md)
- [Quick Start](QUICKSTART.md)
- [Resume API Details](RESUME_API.md)
- [CodeBaseSummary Schema](SCHEMA.md)
- [Implementation Summary](IMPLEMENTATION_SUMMARY.md)

---

## Support

For issues or questions:
1. Check the documentation in the `docs/` folder
2. Review the implementation in `src/app.py`
3. Test with the provided examples

---

## Changelog

### v1.1.0 (Latest)
- Added `/api/analyzeResume` endpoint
- Added `/api/getProfile/{profile_id}` endpoint
- Integrated Grok AI for resume analysis
- Added PDF processing capabilities
- Implemented file storage for profiles

### v1.0.0
- Initial release
- `/api/getCodeBaseSummary` endpoint
- Flask backend with CORS
- Google Cloud Run deployment
