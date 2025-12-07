# Examples

This directory contains example scripts and test data for the Onboarding-x-Grok API.

## Files

### Demo Scripts

**`demo_elon_resume.py`**
- Demonstrates the complete resume analysis workflow
- Uses the included Elon Musk sample resume
- Shows formatted output of the analysis
- Tests both upload and retrieval endpoints

**Usage:**
```bash
# Run from project root
python3 examples/demo_elon_resume.py

# Or from examples directory
cd examples
python3 demo_elon_resume.py
```

**`test_resume_api.py`**
- Creates a sample PDF resume programmatically
- Tests the API with synthetic data
- Useful for automated testing

**Requirements:**
```bash
pip install reportlab  # Only needed for test_resume_api.py
```

**Usage:**
```bash
python3 examples/test_resume_api.py
```

### Test Data

**`elon_musk_junior_backend_resume_one_page.pdf`**
- Sample resume for testing
- Junior backend engineer profile
- Demonstrates transition from full-stack to backend infrastructure

## Running Examples

### Prerequisites

1. **Start the API server:**
   ```bash
   # From project root
   python3 -m src.app
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install reportlab  # Optional, for test_resume_api.py
   ```

### Example Workflow

```bash
# 1. Start server (in one terminal)
python3 -m src.app

# 2. Run demo (in another terminal)
python3 examples/demo_elon_resume.py
```

### Expected Output

The demo will:
1. Upload the resume PDF
2. Display the analysis results (skills, experience, recommendations)
3. Retrieve the stored profile
4. Show file storage locations

## Customization

### Use a Different Resume

Edit `demo_elon_resume.py`:
```python
RESUME_FILE = os.path.join(SCRIPT_DIR, "your_resume.pdf")
```

### Change API URL

Set environment variable:
```bash
export API_URL=https://your-deployment-url.com
python3 examples/demo_elon_resume.py
```

## Integration Testing

These examples can be used for:
- **Development**: Test API changes
- **Demos**: Show potential users how the API works
- **CI/CD**: Automated testing pipeline
- **Documentation**: Living examples of API usage

## Adding New Examples

When adding new examples:
1. Place the script in this directory
2. Add documentation to this README
3. Include any required test data
4. Make paths relative to `SCRIPT_DIR`

Example template:
```python
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_FILE = os.path.join(SCRIPT_DIR, "test_data.pdf")
API_URL = os.environ.get("API_URL", "http://localhost:8080")
```

## Troubleshooting

**"Connection refused"**
- Make sure the API server is running: `python3 -m src.app`

**"File not found"**
- Run scripts from project root: `python3 examples/demo_elon_resume.py`
- Or cd into examples first: `cd examples && python3 demo_elon_resume.py`

**"Grok API key not configured"**
- This is normal! The API works with mock data for testing
- See [docs/GROK_SETUP.md](../docs/GROK_SETUP.md) to enable real AI analysis

## See Also

- [API Reference](../docs/API_REFERENCE.md)
- [Resume API Documentation](../docs/RESUME_API.md)
- [Quick Start Guide](../docs/QUICKSTART.md)
