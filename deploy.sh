#!/bin/bash

# Deployment script for Google Cloud Run
# Makes the API accessible from anywhere (any browser)

echo "🚀 Deploying Onboarding Wiki API to Google Cloud Run..."

# Load environment variables from .env file
if [ -f .env ]; then
    echo "📝 Loading environment variables from .env..."
    export $(cat .env | grep -E "^(XAI_API_KEY|XAI_BASE_URL|XAI_MODEL)=" | xargs)
else
    echo "⚠️  Warning: .env file not found. Make sure API keys are configured."
fi

# Check if XAI_API_KEY is set
if [ -z "$XAI_API_KEY" ]; then
    echo "❌ Error: XAI_API_KEY is not set. Please configure it in .env file."
    exit 1
fi

echo "✅ API Key configured"

# Deploy the service with environment variables
gcloud run deploy onboarding-wiki-api \
  --source . \
  --allow-unauthenticated \
  --region us-central1 \
  --platform managed \
  --timeout 60 \
  --memory 512Mi \
  --set-env-vars XAI_API_KEY=$XAI_API_KEY,XAI_BASE_URL=${XAI_BASE_URL:-https://api.x.ai/v1},XAI_MODEL=${XAI_MODEL:-grok-3}

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
