# Onboarding-x-Grok

A unified FastAPI platform for personalized engineer onboarding, combining AI-powered resume analysis with codebase documentation generation.

## 🚀 Features

### 1. Resume Analysis (AI-Powered)
- Upload PDF resumes for analysis
- Extract technical skills, experience, and education
- Get personalized learning recommendations
- Identify knowledge gaps and strengths
- Powered by Grok AI (grok-3 model)

### 2. Codebase Analysis & Tutorial Generation
- Analyze GitHub repositories
- Generate comprehensive code documentation
- Create knowledge graphs and visualizations
- Build structured tutorials for new hires
- **NEW**: Experience-level-based analysis (junior vs senior)
  - Automatically detects new hire's experience level from resume
  - Generates tailored content using configurable LLM prompts
  - Separate analyses for junior (0-3 years) and senior (3+ years) engineers

### 3. Profile Management
- Store and retrieve candidate profiles
- Track onboarding progress
- Match candidates with codebase requirements

## 📦 Technology Stack

- **Backend**: FastAPI 0.104.1
- **Server**: Uvicorn (async ASGI)
- **AI**: Grok-3 (X.AI)
- **PDF Processing**: PyPDF2
- **Visualization**: NetworkX, Matplotlib, Graphviz
- **Deployment**: Google Cloud Run
- **Frontend**: Next.js (in `client/` directory)

## 🏃 Quick Start

### Prerequisites

- Python 3.9+
- Google Cloud CLI (for deployment)
- Grok API key from https://console.x.ai/

### Local Development

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up environment (optional - has defaults)
echo "XAI_API_KEY=your_grok_key" > .env

# 3. Run the server
python3 main.py

# Server starts at http://localhost:8080
```

### Test the API

```bash
# Health check
curl http://localhost:8080/

# Analyze a resume
curl -X POST http://localhost:8080/api/analyzeResume \
  -F "resume=@examples/elon_musk_junior_backend_resume_one_page.pdf" \
  -F "candidate_email=test@example.com"

# Get profile
curl http://localhost:8080/api/getProfile/{profile_id}
```

### Interactive API Documentation

Visit http://localhost:8080/docs for Swagger UI documentation.

## 🌐 Production Deployment

### Deploy to Google Cloud Run

```bash
# Quick deploy
./deploy.sh

# Manual deploy
gcloud run deploy onboarding-wiki-api \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

### Live Production API

**URL**: `https://onboarding-wiki-api-197454585336.us-central1.run.app`

**Endpoints**:
- `GET /` - API information
- `GET /docs` - Interactive documentation  
- `POST /api/analyzeResume` - Analyze resume PDF
- `GET /api/getProfile/{id}` - Retrieve profile
- `POST /api/analyze` - Analyze codebase
- `GET /health` - Health check

## 📁 Project Structure

```
Onboarding-x-Grok/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration (API keys, models)
├── config_repos.py        # Codebase analysis configuration
├── config_prompts.py      # Analysis prompts configuration
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── deploy.sh             # Deployment script
│
├── api/                   # API route handlers
│   └── routes.py         # Codebase analysis endpoints
│
├── models/                # Pydantic data models
│   └── schemas.py        # Request/response schemas
│
├── services/              # Business logic
│   ├── codebase_analyzer.py
│   ├── codebase_scheduler.py  # Periodic analysis jobs
│   ├── study_plan_generator.py
│   ├── tutorial_generator.py
│   └── visualization_generator.py
│
├── utils/                 # Utility functions
│   └── grok_client.py    # Grok API wrapper
│
├── examples/              # Test data and demos
│   ├── demo_elon_resume.py
│   ├── test_resume_api.py
│   └── elon_musk_junior_backend_resume_one_page.pdf
│
├── docs/                  # Documentation
│   ├── API_REFERENCE.md
│   ├── DEPLOYMENT.md
│   ├── GROK_SETUP.md
│   ├── RESUME_API.md
│   └── ...
│
├── client/                # Next.js frontend (separate)
│
└── data/                  # Runtime data storage (gitignored)
    ├── analysis_prompts/  # LLM prompts for codebase analysis
    │   ├── README.md      # Prompts documentation
    │   ├── junior_engineer_prompt.md
    │   └── senior_engineer_prompt.md
    ├── resumes/          # Uploaded PDFs
    ├── analyzed_profiles/ # Resume analysis results
    ├── codebase_analyses/ # Stored codebase analyses
    └── study_plans/      # Generated study plans
```

## 📚 API Documentation

### Resume Analysis

**Endpoint**: `POST /api/analyzeResume`

**Request**:
```bash
curl -X POST http://localhost:8080/api/analyzeResume \
  -F "resume=@path/to/resume.pdf" \
  -F "candidate_email=candidate@example.com"
```

**Response**:
```json
{
  "success": true,
  "profile_id": "abc123",
  "message": "Resume analyzed successfully",
  "analysis": {
    "candidate_name": "John Doe",
    "experience_years": 5,
    "education": [...],
    "technical_skills": {
      "languages": ["Python", "JavaScript"],
      "frameworks": ["React", "FastAPI"],
      "tools": ["Docker", "AWS"],
      "databases": ["PostgreSQL"]
    },
    "strengths": [...],
    "knowledge_gaps": [...],
    "recommended_learning_path": [...]
  }
}
```

### Get Profile

**Endpoint**: `GET /api/getProfile/{profile_id}`

Returns the complete stored profile including upload metadata and analysis.

### Codebase Analysis

**Endpoint**: `POST /api/analyze`

**Request**:
```json
{
  "repo_url": "https://github.com/user/repo",
  "include": ["*.py", "*.js"],
  "exclude": ["**/node_modules/**"]
}
```

Generates comprehensive codebase documentation with:
- Code summary
- Chapter-wise tutorials
- Knowledge graph
- Dependency visualizations
- Architecture diagrams

## 🔑 Configuration

### Environment Variables

Create a `.env` file (optional - has defaults):

```bash
# Grok API Configuration
XAI_API_KEY=xai-your-key-here
XAI_MODEL=grok-3
XAI_BASE_URL=https://api.x.ai/v1

# Optional
GITHUB_TOKEN=your_github_token  # For private repos
PORT=8080
```

Current defaults in `config.py`:
- Model: `grok-3`
- API key: Pre-configured (ask teammate for current key)

## 🧪 Testing

### Run Example Scripts

```bash
# Test with Elon Musk's sample resume
python3 examples/demo_elon_resume.py

# Create and test with synthetic resume
python3 examples/test_resume_api.py
```

### Test Production API

```bash
# Test resume analysis
curl -X POST "https://onboarding-wiki-api-197454585336.us-central1.run.app/api/analyzeResume" \
  -F "resume=@examples/elon_musk_junior_backend_resume_one_page.pdf" \
  -F "candidate_email=test@example.com"
```

## 🎯 Use Cases

### 1. New Hire Onboarding
- Upload new hire's resume
- Get skills analysis
- Match with codebase requirements
- Generate personalized learning plan

### 2. Codebase Documentation
- Analyze company repositories
- Generate wiki-style documentation
- Create visual architecture diagrams
- Build knowledge graphs

### 3. Team Onboarding
- Analyze entire team's skills
- Identify knowledge gaps
- Plan training programs
- Track progress

## 📊 Cost & Performance

### API Response Times
- Health check: ~50ms
- Resume analysis: ~3-5 seconds (Grok processing)
- Profile retrieval: ~100ms
- Codebase analysis: Varies by repo size

### Grok API Costs
- Resume analysis: ~$0.01-0.05 per resume
- Model: grok-3
- Pricing: https://x.ai/pricing

## 🔒 Security Considerations

### Current Implementation
- ✅ File type validation (PDF only)
- ✅ File size limits (10MB)
- ✅ Secure filename handling
- ✅ CORS enabled

### Production Recommendations
- [ ] Add authentication/authorization
- [ ] Implement rate limiting
- [ ] Add virus scanning for uploads
- [ ] Encrypt stored profiles
- [ ] GDPR compliance (data deletion, export)
- [ ] Audit logging

## 🚧 Roadmap

### Near Term
- [ ] Database integration (replace file storage)
- [ ] Batch resume processing
- [ ] Resume comparison features
- [ ] Advanced search and filtering

### Future Features
- [ ] Personalized onboarding plan generator
- [ ] Learning progress tracking
- [ ] Integration with HR systems
- [ ] Team analytics dashboard
- [ ] Slack/Teams integration
- [ ] Video resume analysis

## 📖 Additional Documentation

- [Complete API Reference](docs/API_REFERENCE.md)
- [Grok Setup Guide](docs/GROK_SETUP.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Resume API Details](docs/RESUME_API.md)
- [FastAPI Migration Notes](FASTAPI_MIGRATION_SUCCESS.md)
- [Codebase Summary Schema](CODEBASE_SUMMARY.md)

## 🤝 Contributing

### Development Workflow

1. Make changes locally
2. Test with `python3 main.py`
3. Test all endpoints
4. Deploy with `./deploy.sh`
5. Verify production deployment

### Code Organization

- Put new API endpoints in `api/routes.py`
- Add business logic to `services/`
- Define data models in `models/schemas.py`
- Update documentation in `docs/`

## 📝 License

This project is for internal use.

## 🙏 Acknowledgments

- Grok AI by X.AI for resume analysis
- FastAPI for the modern Python framework
- Google Cloud Run for serverless deployment

## 📞 Support

- **API Docs**: https://onboarding-wiki-api-197454585336.us-central1.run.app/docs
- **Cloud Console**: https://console.cloud.google.com/run/detail/us-central1/onboarding-wiki-api
- **Logs**: https://console.cloud.google.com/run/detail/us-central1/onboarding-wiki-api/logs

---

**Status**: ✅ Production Ready

**Last Updated**: December 2024

**Version**: 2.0.0 (FastAPI)
