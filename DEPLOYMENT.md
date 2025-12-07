# Google Cloud Run Deployment Guide

This guide walks you through deploying the Onboarding-x-Grok Flask API to Google Cloud Run.

## Prerequisites

1. **Google Cloud Account**: Create one at [cloud.google.com](https://cloud.google.com)
2. **Billing Enabled**: Cloud Run requires a billing account
3. **gcloud CLI**: Install from [cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)

## Step 1: Install and Configure gcloud CLI

### Install gcloud (if not already installed)

**macOS** (using Homebrew):
```bash
brew install google-cloud-sdk
```

**Alternative** (official installer):
```bash
# Download and install
curl https://sdk.cloud.google.com | bash

# Restart shell
exec -l $SHELL

# Initialize
gcloud init
```

### Login to Google Cloud
```bash
gcloud auth login
```

This will open your browser to authenticate.

## Step 2: Create and Configure a Google Cloud Project

### Create a new project (or use existing)
```bash
# Create new project
gcloud projects create onboarding-wiki-project --name="Onboarding Wiki"

# List all projects to see your project
gcloud projects list
```

### Set the active project
```bash
# Replace with your actual project ID
gcloud config set project onboarding-wiki-project
```

### Set the region
```bash
gcloud config set run/region us-central1
```

Common regions:
- `us-central1` (Iowa, USA)
- `us-east1` (South Carolina, USA)
- `us-west1` (Oregon, USA)
- `europe-west1` (Belgium)
- `asia-east1` (Taiwan)

## Step 3: Enable Required APIs

```bash
# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Enable Cloud Build API (for building containers)
gcloud services enable cloudbuild.googleapis.com

# Enable Artifact Registry (optional, for storing images)
gcloud services enable artifactregistry.googleapis.com
```

This may take a few minutes.

## Step 4: Deploy to Cloud Run

### Option A: Direct Deployment (Recommended)

From the project root directory:

```bash
gcloud run deploy onboarding-wiki-api \
  --source . \
  --allow-unauthenticated \
  --region us-central1 \
  --platform managed
```

**What this does:**
- Builds a Docker image from the Dockerfile
- Pushes it to Google Container Registry
- Deploys to Cloud Run
- Makes the service publicly accessible
- Prints the service URL when complete

**Build time**: 2-5 minutes (first deployment)

### Option B: Manual Build and Deploy

If you want more control:

```bash
# Build the container image
gcloud builds submit --tag gcr.io/onboarding-wiki-project/wiki-api

# Deploy to Cloud Run
gcloud run deploy onboarding-wiki-api \
  --image gcr.io/onboarding-wiki-project/wiki-api \
  --allow-unauthenticated \
  --region us-central1 \
  --platform managed
```

## Step 5: Get Your Service URL

```bash
gcloud run services describe onboarding-wiki-api \
  --region us-central1 \
  --format 'value(status.url)'
```

This will output something like:
```
https://onboarding-wiki-api-abc123-uc.a.run.app
```

## Step 6: Test Your Deployed API

```bash
# Store the URL
SERVICE_URL=$(gcloud run services describe onboarding-wiki-api --region us-central1 --format 'value(status.url)')

# Test health endpoint
curl "$SERVICE_URL/"

# Test the main API
curl "$SERVICE_URL/api/getCodeBaseSummary?codebase_url=https://github.com/facebook/rocksdb"
```

## Managing Your Deployment

### View Logs
```bash
# Stream logs in real-time
gcloud run logs tail onboarding-wiki-api --region us-central1

# View recent logs
gcloud run logs read onboarding-wiki-api --region us-central1 --limit 50
```

### Update Deployment

After making code changes:

```bash
gcloud run deploy onboarding-wiki-api --source .
```

Or using the manual approach:
```bash
gcloud builds submit --tag gcr.io/onboarding-wiki-project/wiki-api
gcloud run deploy onboarding-wiki-api --image gcr.io/onboarding-wiki-project/wiki-api
```

### View Service Details
```bash
gcloud run services describe onboarding-wiki-api --region us-central1
```

### List All Services
```bash
gcloud run services list
```

### Delete Service
```bash
gcloud run services delete onboarding-wiki-api --region us-central1
```

## Advanced Configuration

### Set Environment Variables
```bash
gcloud run deploy onboarding-wiki-api \
  --source . \
  --set-env-vars "ENVIRONMENT=production,LOG_LEVEL=info"
```

### Configure Memory and CPU
```bash
gcloud run deploy onboarding-wiki-api \
  --source . \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10
```

### Set Timeout
```bash
gcloud run deploy onboarding-wiki-api \
  --source . \
  --timeout 300
```

### Enable Authentication
```bash
# Deploy with authentication required
gcloud run deploy onboarding-wiki-api \
  --source . \
  --no-allow-unauthenticated

# Grant access to specific users/service accounts
gcloud run services add-iam-policy-binding onboarding-wiki-api \
  --region us-central1 \
  --member="user:your-email@example.com" \
  --role="roles/run.invoker"
```

## Cost Management

Cloud Run pricing (as of 2024):
- **Free tier**: 2 million requests/month, 360,000 GB-seconds/month
- **Pay-as-you-go**: ~$0.40 per million requests
- **No traffic = minimal costs** (only pay for requests)

### Monitor Costs
```bash
# View billing information
gcloud billing accounts list

# Set budget alerts in Cloud Console
# console.cloud.google.com/billing/budgets
```

## Troubleshooting

### Build Fails
```bash
# Check Cloud Build logs
gcloud builds list --limit 5
gcloud builds log <BUILD_ID>
```

### Service Won't Start
```bash
# Check logs for errors
gcloud run logs read onboarding-wiki-api --region us-central1 --limit 100
```

### Permission Errors
```bash
# Ensure you're authenticated
gcloud auth list

# Ensure correct project is set
gcloud config get-value project

# Check IAM permissions
gcloud projects get-iam-policy onboarding-wiki-project
```

### Connection Issues
```bash
# Test if service is accessible
curl -v $(gcloud run services describe onboarding-wiki-api --region us-central1 --format 'value(status.url)')
```

## Security Best Practices

1. **Use Secrets Manager** for sensitive data:
   ```bash
   # Create a secret
   echo -n "my-secret-value" | gcloud secrets create db-password --data-file=-
   
   # Grant access to Cloud Run
   gcloud secrets add-iam-policy-binding db-password \
     --member="serviceAccount:YOUR-PROJECT-NUMBER-compute@developer.gserviceaccount.com" \
     --role="roles/secretmanager.secretAccessor"
   ```

2. **Enable HTTPS only** (enabled by default)

3. **Use VPC Connector** for private database access

4. **Implement API authentication** (see app.py for examples)

## Next Steps

- [ ] Set up continuous deployment with GitHub Actions
- [ ] Configure custom domain
- [ ] Add Cloud SQL or Firestore for data persistence
- [ ] Set up monitoring and alerting
- [ ] Implement caching with Cloud Memorystore

## Resources

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud Run Pricing](https://cloud.google.com/run/pricing)
- [Flask on Cloud Run Tutorial](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service)
- [Best Practices for Cloud Run](https://cloud.google.com/run/docs/tips)
