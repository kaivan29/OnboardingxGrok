# Resume Analysis API

## New Endpoint: `/api/analyzeResume`

Upload a resume PDF to analyze the candidate's technical background and experience using Grok AI.

### Setup

1. **Get a Grok API Key:**
   - Visit [https://console.x.ai/](https://console.x.ai/)
   - Create an account and generate an API key

2. **Configure the API Key:**
   ```bash
   # Create a .env file in the project root
   echo "GROK_API_KEY=your_api_key_here" > .env
   ```

   Or set as environment variable:
   ```bash
   export GROK_API_KEY=your_grok_api_key
   ```

### API Endpoint

**POST** `/api/analyzeResume`

**Content-Type:** `multipart/form-data`

**Parameters:**
- `resume` (file, required) - PDF file of the candidate's resume
- `candidate_email` (string, optional) - Email address for identification

**Response:**
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
      "languages": ["Python", "JavaScript", "Java", "Go"],
      "frameworks": ["React", "Flask", "Spring Boot", "Node.js"],
      "tools": ["Git", "Docker", "Kubernetes", "AWS"],
      "databases": ["PostgreSQL", "MongoDB", "Redis"]
    },
    "experience_summary": [
      {
        "role": "Senior Software Engineer",
        "company": "Tech Corp",
        "duration": "2020 - Present",
        "technologies": ["Python", "AWS", "PostgreSQL"],
        "key_achievements": [
          "Designed and implemented microservices architecture",
          "Improved system performance by 40%",
          "Led team of 5 engineers"
        ]
      }
    ],
    "strengths": [
      "Strong backend development skills",
      "Extensive experience with cloud platforms",
      "Proven track record in system design"
    ],
    "knowledge_gaps": [
      "Limited experience with machine learning",
      "Could deepen knowledge in distributed systems"
    ],
    "recommended_learning_path": [
      "Study distributed systems architecture",
      "Learn about ML operations and deployment",
      "Deep dive into advanced database optimization"
    ]
  }
}
```

###Retrieve Profile

**GET** `/api/getProfile/{profile_id}`

Retrieve a previously analyzed resume profile.

**Response:**
```json
{
  "profile_id": "a1b2c3d4e5f6",
  "candidate_email": "john@example.com",
  "uploaded_at": "2024-12-07T00:00:00",
  "resume_filename": "john_doe_resume.pdf",
  "analysis": {
    // Same structure as above
  }
}
```

## Usage Examples

### cURL Example

```bash
# Analyze a resume
curl -X POST http://localhost:8080/api/analyzeResume \
  -F "resume=@/path/to/resume.pdf" \
  -F "candidate_email=candidate@example.com"

# Retrieve profile
curl http://localhost:8080/api/getProfile/a1b2c3d4e5f6
```

### Python Example

```python
import requests

# Upload and analyze resume
files = {'resume': open('resume.pdf', 'rb')}
data = {'candidate_email': 'candidate@example.com'}

response = requests.post(
    'http://localhost:8080/api/analyzeResume',
    files=files,
    data=data
)

result = response.json()
print(f"Profile ID: {result['profile_id']}")
print(f"Analysis: {result['analysis']}")

# Retrieve profile later
profile_id = result['profile_id']
profile = requests.get(f'http://localhost:8080/api/getProfile/{profile_id}')
print(profile.json())
```

### JavaScript/Fetch Example

```javascript
// Upload resume
const formData = new FormData();
formData.append('resume', fileInput.files[0]);
formData.append('candidate_email', 'candidate@example.com');

const response = await fetch('http://localhost:8080/api/analyzeResume', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log('Profile ID:', result.profile_id);
console.log('Analysis:', result.analysis);

// Retrieve profile
const profileResponse = await fetch(
  `http://localhost:8080/api/getProfile/${result.profile_id}`
);
const profile = await profileResponse.json();
```

## Testing Without Grok API Key

The API will work without a Grok API key and return mock data for testing purposes. You'll see a warning in the response:

```json
{
  "analysis": {
    "warning": "Grok API key not configured - using mock data",
    ...
  }
}
```

## File Storage

### Uploaded Resumes
Stored in: `data/resumes/`
Format: `{profile_id}_{original_filename}.pdf`

### Analyzed Profiles
Stored in: `data/analyzed_profiles/`
Format: `{profile_id}.json`

Example profile JSON:
```json
{
  "profile_id": "a1b2c3d4e5f6",
  "candidate_email": "john@example.com",
  "uploaded_at": "2024-12-07T00:00:00.000000",
  "resume_filename": "john_doe_resume.pdf",
  "analysis": {
    // Analysis results
  }
}
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "No resume file provided"
}
```

Possible errors:
- `"No resume file provided"` - Missing file in request
- `"No file selected"` - Empty filename
- `"Only PDF files are allowed"` - Invalid file type
- `"File size exceeds maximum 10MB"` - File too large
- `"Could not extract sufficient text from PDF"` - PDF parsing failed

### 404 Not Found
```json
{
  "error": "Profile not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error: <details>"
}
```

## Integration with Feature 2: Personalized Onboarding

This API provides the foundation for personalized onboarding:

1. **New hire uploads resume** → API analyzes background
2. **Analysis identifies:**
   - Current knowledge level
   - Technical strengths
   - Knowledge gaps
   - Recommended learning path

3. **Next steps:**
   - Combine with codebase summary from `getCodeBaseSummary`
   - Match candidate's background with project requirements
   - Generate personalized weekly ramp-up plan
   - Provide targeted learning resources

## Roadmap

- [ ] Add support for DOCX resumes
- [ ] Implement batch processing
- [ ] Add profile comparison features
- [ ] Create learning path generator based on codebase and profile
- [ ] Build admin dashboard for HR/managers
- [ ] Add analytics and insights

## Security Considerations

For production:
1. Add authentication/authorization
2. Sanitize file uploads
3. Implement rate limiting
4. Add virus scanning for uploaded files
5. Encrypt stored profiles
6. Add GDPR compliance features (data deletion, export)
