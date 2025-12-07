#!/bin/bash

# Master deployment script for full-stack application
# Deploys both backend and frontend to Google Cloud Run

echo "🚀 Starting full-stack deployment to Google Cloud Run..."
echo "=================================================="
echo ""

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
echo ""

# Step 1: Deploy Backend
echo "📦 Step 1/2: Deploying Backend (FastAPI)..."
echo ""

gcloud run deploy onboarding-wiki-api \
  --source . \
  --allow-unauthenticated \
  --region us-central1 \
  --platform managed \
  --timeout 60 \
  --memory 512Mi \
  --set-env-vars XAI_API_KEY=$XAI_API_KEY,XAI_BASE_URL=${XAI_BASE_URL:-https://api.x.ai/v1},XAI_MODEL=${XAI_MODEL:-grok-3}

# Capture backend URL
BACKEND_URL=$(gcloud run services describe onboarding-wiki-api --region us-central1 --format 'value(status.url)')

if [ -z "$BACKEND_URL" ]; then
    echo "❌ Error: Backend deployment failed or URL not found"
    exit 1
fi

echo ""
echo "✅ Backend deployed successfully!"
echo "📍 Backend URL: $BACKEND_URL"
echo ""
echo "=================================================="
echo ""

# Step 2: Deploy Frontend with backend URL
echo "📦 Step 2/2: Deploying Frontend (Next.js)..."
echo ""

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

# Capture frontend URL
FRONTEND_URL=$(gcloud run services describe onboarding-wiki-frontend --region us-central1 --format 'value(status.url)')

if [ -z "$FRONTEND_URL" ]; then
    echo "❌ Error: Frontend deployment failed or URL not found"
    exit 1
fi

echo ""
echo "✅ Frontend deployed successfully!"
echo "📍 Frontend URL: $FRONTEND_URL"
echo ""
echo "=================================================="
echo ""
echo "🎉 Deployment Complete!"
echo ""
echo "Your application is now live:"
echo "  Backend:  $BACKEND_URL"
echo "  Frontend: $FRONTEND_URL"
echo ""
echo "🧪 Quick tests:"
echo "  Backend health: curl \"$BACKEND_URL/health\""
echo "  Frontend: open $FRONTEND_URL"
echo ""
