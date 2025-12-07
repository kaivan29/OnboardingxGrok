# Instructions: Get Your Grok API Key

## Step 1: Get API Key from X.AI

1. Visit: https://console.x.ai/
2. Sign in with your X (Twitter) account
3. Navigate to API Keys section
4. Click "Create New API Key"
5. Copy the key (starts with "xai-...")

## Step 2: Configure the Key

**Option A: Create .env file (Recommended)**
```bash
echo "GROK_API_KEY=xai-your_actual_key_here" > .env
```

**Option B: Set environment variable**
```bash
export GROK_API_KEY=xai-your_actual_key_here
```

## Step 3: Restart the Server

```bash
# Stop current server (Ctrl+C in terminal or:)
lsof -ti:8080 | xargs kill -9

# Start with new config
python3 -m src.app
```

## Step 4: Test with Real Analysis

```bash
curl -X POST http://localhost:8080/api/analyzeResume \
  -F "resume=@elon_musk_junior_backend_resume_one_page.pdf" \
  -F "candidate_email=elon@example.com" | python3 -m json.tool
```

The response will now contain actual AI analysis instead of mock data!

## What You'll Get

With Grok API enabled, the analysis will be based on the actual resume content:
- Real name: "Elon Musk"
- Actual education: "University of Pennsylvania - BA Physics & BS Economics (1997)"
- Real experience: Full-stack developer background, Zip2, X.com
- True technical skills: JavaScript, TypeScript, Python, Go
- Personalized recommendations based on stated objective (backend infrastructure)
- Knowledge gaps identified from resume (e.g., limited distributed systems experience)
- Learning path tailored to help transition to backend role

## Costs

Grok API pricing:
- Check current rates at: https://x.ai/pricing
- Typical: ~$5-10 per million tokens
- Each resume analysis: ~$0.01-0.05 (rough estimate)

## Alternative: Continue with Mock Data

The system works perfectly for testing without Grok:
- Frontend development ✅
- API integration testing ✅
- Deployment testing ✅
- Demo purposes ✅

You can add Grok later when ready for production!
