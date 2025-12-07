#!/bin/bash

# Deployment script for Next.js Frontend to Google Cloud Run
# Requires BACKEND_URL environment variable to be set

echo "🚀 Deploying Onboarding Wiki Frontend to Google Cloud Run..."

# Check if BACKEND_URL is provided
if [ -z "$1" ]; then
    echo "❌ Error: Backend URL is required"
    echo "Usage: ./deploy-frontend.sh <BACKEND_URL>"
    echo "Example: ./deploy-frontend.sh https://onboarding-wiki-api-xxxxx.run.app"
    exit 1
fi

BACKEND_URL=$1

echo "📍 Using Backend URL: $BACKEND_URL"
echo ""

# Deploy the frontend service
cd client
gcloud run deploy onboarding-wiki-frontend \
  --source . \
  --allow-unauthenticated \
  --region us-central1 \
  --platform managed \
  --timeout 60 \
  --memory 512Mi \
  --set-env-vars NEXT_PUBLIC_API_URL=$BACKEND_URL

cd ..

# Get and display the service URL
echo ""
echo "✅ Frontend deployment complete!"
echo ""
echo "📍 Your Frontend URL:"
FRONTEND_URL=$(gcloud run services describe onboarding-wiki-frontend --region us-central1 --format 'value(status.url)')
echo "$FRONTEND_URL"
echo ""
echo "🌐 Open in browser:"
echo "$FRONTEND_URL"
