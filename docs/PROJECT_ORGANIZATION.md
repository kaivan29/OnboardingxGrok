# 📁 Project Organization - Best Practices

## Directory Structure

The project follows Python Flask best practices with clear separation of concerns:

```
Onboarding-x-Grok/
│
├── 📦 src/                          # Application Source Code
│   ├── __init__.py                 # Python package initialization
│   └── app.py                      # Main Flask application with all endpoints
│
├── 📚 docs/                         # Documentation
│   ├── API_REFERENCE.md            # Complete API documentation
│   ├── DEPLOYMENT.md               # Google Cloud Run deployment guide
│   ├── GROK_SETUP.md               # Grok API configuration instructions
│   ├── IMPLEMENTATION_SUMMARY.md   # Technical implementation details
│   ├── QUICKSTART.md               # 5-minute quick start guide
│   ├── RESUME_API.md               # Resume analysis API documentation
│   └── SCHEMA.md                   # CodeBaseSummary schema reference
│
├── 🧪 examples/                     # Examples and Test Data
│   ├── README.md                   # Examples documentation
│   ├── demo_elon_resume.py         # Working demo with sample resume
│   ├── test_resume_api.py          # Test script with synthetic data
│   └── elon_musk_junior_backend_resume_one_page.pdf  # Sample resume
│
├── 💾 data/                         # Runtime Data (Git Ignored)
│   ├── .gitkeep                    # Preserve directory in git
│   ├── resumes/                    # Uploaded PDF files
│   │   └── .gitkeep
│   └── analyzed_profiles/          # Analysis results (JSON)
│       └── .gitkeep
│
├── 🚀 Deployment Files
│   ├── deploy.sh                   # Automated deployment script
│   ├── Dockerfile                  # Container configuration
│   └── .gcloudignore              # Files to exclude from deployment
│
├── ⚙️ Configuration
│   ├── requirements.txt            # Python dependencies
│   ├── .env.example               # Environment template
│   ├── .gitignore                 # Git ignore rules
│   └── README.md                  # Main project documentation
│
└── 📄 Root Files
    └── (deployment and config files only)
```

## Design Principles

### 1. **Clear Separation of Concerns**
- **Source**: All application code in `src/`
- **Documentation**: All docs in `docs/`
- **Examples**: Demos and test data in `examples/`
- **Data**: Runtime data in `data/` (gitignored)

### 2. **Self-Documenting Structure**
Each directory has a clear purpose:
- `src/` → "Where is the code?"
- `docs/` → "How do I use this?"
- `examples/` → "Show me how it works"
- `data/` → "Where does it store things?"

### 3. **Deployment Ready**
- Clean root directory
- Docker configuration at root
- Deployment scripts easily accessible
- Cloud-specific configs (`.gcloudignore`)

### 4. **Developer Friendly**
- Examples are runnable
- Docs are comprehensive
- Test data included
- Clear paths in code

## File Organization Rules

### ✅ DO

**Root Directory:**
- Keep deployment files (`Dockerfile`, `deploy.sh`)
- Keep configuration (`requirements.txt`, `.env.example`)
- Keep documentation (`README.md`)
- Keep version control (`.gitignore`, `.gcloudignore`)

**src/ Directory:**
- Application code only
- Business logic
- API endpoints
- Helper functions

**docs/ Directory:**
- All markdown documentation
- API references
- Guides and tutorials
- Implementation notes

**examples/ Directory:**
- Demo scripts
- Test data
- Sample code
- Integration examples

**data/ Directory:**
- Runtime generated files
- Uploaded files
- Temporary storage
- Cache files

### ❌ DON'T

- Don't put code in root directory
- Don't mix examples with source code
- Don't commit data files
- Don't put docs in root (except README)
- Don't scatter test files everywhere

## Python Import Best Practices

### Running the Application

```bash
# ✅ Correct: Run as module
python3 -m src.app

# ❌ Incorrect: Direct execution
python3 src/app.py
```

### Running Examples

```bash
# ✅ From project root
python3 examples/demo_elon_resume.py

# ✅ From examples directory
cd examples && python3 demo_elon_resume.py
```

### Imports in Code

```python
# ✅ In src/app.py - absolute imports
from datetime import datetime
from flask import Flask

# ❌ Avoid relative imports in main modules
from ..utils import helper  # Don't do this in app.py
```

## Data Management

### Git Ignore Strategy

**Ignored (in .gitignore):**
- `data/` - All uploaded and generated data
- `.env` - Environment secrets
- `__pycache__/` - Python bytecode
- `*.pyc` - Compiled Python
- `test_resume.pdf` - Test artifacts
- `analysis_*.json` - Generated analyses

**Tracked (with .gitkeep):**
- `data/.gitkeep` - Preserves directory structure
- `data/resumes/.gitkeep`
- `data/analyzed_profiles/.gitkeep`

This ensures:
- Directory structure is maintained
- No sensitive data is committed
- Clean repository

## Deployment Considerations

### What Gets Deployed

The `.gcloudignore` excludes:
- Git files (`.git`, `.gitignore`)
- Documentation (`*.md` except README)
- Development files (`node_modules`, `.next`)
- Python cache (`__pycache__`, `*.pyc`)
- Environment files (`.env`)
- Virtual environments (`venv/`, `.venv/`)

This keeps deployments:
- Small and fast
- Secure (no secrets)
- Clean (no dev artifacts)

## Testing Organization

### Current Structure
- Examples include test data
- Demo scripts double as integration tests
- Unit tests would go in `tests/` (future)

### Future: tests/ Directory

When adding proper testing:
```
tests/
├── __init__.py
├── test_api.py           # API endpoint tests
├── test_resume.py        # Resume analysis tests
└── fixtures/             # Test data
    └── sample_resume.pdf
```

## Documentation Organization

### docs/ Structure

**Purpose-Based Organization:**
- `API_REFERENCE.md` - For API consumers
- `DEPLOYMENT.md` - For DevOps/deployment
- `QUICKSTART.md` - For new users
- `RESUME_API.md` - Feature-specific (resume)
- `SCHEMA.md` - Feature-specific (codebase wiki)
- `GROK_SETUP.md` - Configuration guide
- `IMPLEMENTATION_SUMMARY.md` - For developers

This allows users to find what they need quickly.

## Examples Organization

### Best Practices for examples/

1. **Self-Contained**: Each example should work independently
2. **Documented**: README.md explains each script
3. **Realistic**: Use real-world scenarios
4. **Runnable**: Include all necessary test data
5. **Clear Paths**: Use `os.path` for file locations

### Example Script Template

```python
#!/usr/bin/env python3
"""
Brief description of what this example demonstrates
"""
import os

# Get script directory for relative paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_FILE = os.path.join(SCRIPT_DIR, "test_data.pdf")

# Use environment variable for flexibility
API_URL = os.environ.get("API_URL", "http://localhost:8080")

# Rest of script...
```

## Benefits of This Organization

1. **Scalability**: Easy to add new features
2. **Maintainability**: Clear where everything belongs
3. **Collaboration**: New developers find things quickly
4. **Professional**: Follows industry standards
5. **Deployment**: Clean separation of dev/prod
6. **Documentation**: Everything is documented
7. **Testing**: Examples serve as integration tests

## Migration Notes

### What Was Moved

- `demo_elon_resume.py` → `examples/`
- `test_resume_api.py` → `examples/`
- `elon_musk_junior_backend_resume_one_page.pdf` → `examples/`
- `GROK_SETUP.md` → `docs/`

### What Stayed

- `deploy.sh` → Root (deployment tool)
- `Dockerfile` → Root (deployment config)
- `requirements.txt` → Root (package config)
- `.env.example` → Root (config template)
- `README.md` → Root (main documentation)

### Scripts Updated

- `examples/demo_elon_resume.py` → Updated paths to use `SCRIPT_DIR`
- `README.md` → Updated project structure diagram

## Summary

This organization follows these key principles:
1. **Separation of concerns** - Each directory has one purpose
2. **Standard conventions** - Follows Python/Flask norms
3. **Developer friendly** - Easy to navigate and understand
4. **Production ready** - Clean deployment structure
5. **Well documented** - Every directory explained

The result is a professional, maintainable codebase that scales well.
