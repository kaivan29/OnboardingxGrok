"""
Chat API endpoint for codebase Q&A
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from utils.grok_client import GrokClient
from pathlib import Path
import json

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat_with_codebase(request: ChatRequest):
    """
    Chat endpoint for asking questions about the codebase.
    Uses Grok API with codebase context to provide intelligent answers.
    """
    try:
        # Initialize Grok client
        grok_client = GrokClient()
        
        # Load the most recent codebase analysis for context
        data_dir = Path("data/codebase_analyses")
        context = ""
        
        if data_dir.exists():
            analysis_files = sorted(data_dir.glob("*.json"), reverse=True)
            if analysis_files:
                with open(analysis_files[0], 'r') as f:
                    codebase_data = json.load(f)
                    
                    # Build context from codebase summary
                    summary = codebase_data.get('summary', {})
                    context = f"""
Codebase Context:
- Repository: {codebase_data.get('repo_url', 'Unknown')}
- Technologies: {', '.join(summary.get('technologies', []))}
- Key Components: {', '.join(summary.get('key_components', []))}
- Difficulty Level: {summary.get('difficulty_level', 'Unknown')}

The user is asking questions about this codebase. Provide detailed, helpful answers based on the context.
"""
        
        # Build conversation history
        messages = []
        for msg in request.history[-5:]:  # Keep last 5 messages for context
            messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Add current question with context
        messages.append({
            "role": "user",
            "content": f"{context}\n\nQuestion: {request.message}"
        })
        
        # Call Grok API
        response = await grok_client.chat_completion(messages)
        
        # Close client
        await grok_client.close()
        
        return ChatResponse(response=response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")
