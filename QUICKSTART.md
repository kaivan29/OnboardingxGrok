# Quick Start Guide

Get the Onboarding Wiki API running in 5 minutes!

## Local Development

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Server
```bash
python app.py
```

Server starts at `http://localhost:8080`

### 3. Test It
```bash
# Health check
curl http://localhost:8080/

# Get wiki for RocksDB
curl "http://localhost:8080/api/getCodeBaseSummary?codebase_url=https://github.com/facebook/rocksdb"
```

---

## Deploy to Google Cloud (5 minutes)

### One-Time Setup
```bash
# Install gcloud CLI (macOS)
brew install google-cloud-sdk

# Login
gcloud auth login

# Create/set project
gcloud config set project YOUR_PROJECT_ID
gcloud config set run/region us-central1

# Enable APIs
gcloud services enable run.googleapis.com cloudbuild.googleapis.com
```

### Deploy
```bash
gcloud run deploy onboarding-wiki-api \
  --source . \
  --allow-unauthenticated
```

Wait 2-5 minutes. You'll get a URL like:
```
https://onboarding-wiki-api-xyz-uc.a.run.app
```

### Test Deployment
```bash
SERVICE_URL=$(gcloud run services describe onboarding-wiki-api --region us-central1 --format 'value(status.url)')

curl "$SERVICE_URL/api/getCodeBaseSummary?codebase_url=https://github.com/facebook/rocksdb"
```

---

## API Usage

### Endpoint
```
GET /api/getCodeBaseSummary?codebase_url={repo_url}
```

### Example Requests

**cURL:**
```bash
curl "http://localhost:8080/api/getCodeBaseSummary?codebase_url=https://github.com/facebook/rocksdb"
```

**JavaScript:**
```javascript
const response = await fetch(
  'http://localhost:8080/api/getCodeBaseSummary?codebase_url=https://github.com/facebook/rocksdb'
);
const { wiki } = await response.json();
```

**Python:**
```python
import requests

response = requests.get(
    'http://localhost:8080/api/getCodeBaseSummary',
    params={'codebase_url': 'https://github.com/facebook/rocksdb'}
)
wiki = response.json()['wiki']
```

### Response Schema

See [SCHEMA.md](SCHEMA.md) for complete documentation.

The API returns a comprehensive wiki with:
- Repository metadata
- Architecture diagrams (components, edges)
- Workflows (write/read/compaction)
- Module catalog
- Operational metrics & runbooks
- Getting started guide
- FAQs

---

## What's Next?

1. **Read the docs:**
   - [README.md](README.md) - Full documentation
   - [SCHEMA.md](SCHEMA.md) - API schema & TypeScript types
   - [DEPLOYMENT.md](DEPLOYMENT.md) - Detailed Cloud Run guide

2. **Build a frontend:**
   - Use the schema to create a wiki viewer
   - Try frameworks: Docusaurus, VitePress, or custom React
   - Visualize architecture with D3.js or Mermaid

3. **Add real data:**
   - Replace `PREPROCESSED_WIKIS` dictionary in `app.py`
   - Integrate with Cloud Firestore or Cloud SQL
   - Build a GitHub analyzer to generate wikis

4. **Production features:**
   - Add authentication
   - Implement caching
   - Set up monitoring
   - Create admin endpoints

---

## Troubleshooting

### Port already in use
```bash
# Kill process on port 8080
lsof -ti:8080 | xargs kill -9

# Or use a different port
PORT=8000 python app.py
```

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Cloud Run deployment fails
```bash
# Check build logs
gcloud builds list --limit 5
gcloud builds log <BUILD_ID>

# Check service logs
gcloud run logs tail onboarding-wiki-api --region us-central1
```

---

## File Structure

```
Onboarding-x-Grok/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container config
├── README.md             # Full documentation
├── SCHEMA.md             # API schema reference
├── DEPLOYMENT.md         # Cloud Run deployment guide
├── QUICKSTART.md         # This file
├── .gitignore           # Git ignore rules
└── .gcloudignore        # Cloud deployment ignore rules
```

---

## Support

- **Documentation:** See README.md for detailed info
- **Schema:** Check SCHEMA.md for frontend integration
- **Deployment:** Read DEPLOYMENT.md for Cloud Run guide

Happy coding! 🚀
