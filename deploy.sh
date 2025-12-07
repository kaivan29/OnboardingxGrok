#!/bin/bash

# Deployment script for Google Cloud Run
# Makes the API accessible from anywhere (any browser)

echo "🚀 Deploying Onboarding Wiki API to Google Cloud Run..."

# Deploy the service
gcloud run deploy onboarding-wiki-api \
  --source . \
  --allow-unauthenticated \
  --region us-central1 \
  --platform managed \
  --timeout 60 \
  --memory 512Mi

# Get and display the service URL
echo ""
echo "✅ Deployment complete!"
echo ""
echo "📍 Your API URL:"
SERVICE_URL=$(gcloud run services describe onboarding-wiki-api --region us-central1 --format 'value(status.url)')
echo "$SERVICE_URL"
echo ""
echo "🧪 Test your API:"
echo "curl \"$SERVICE_URL/\""
echo "curl \"$SERVICE_URL/api/getCodeBaseSummary?codebase_url=https://github.com/facebook/rocksdb\""
