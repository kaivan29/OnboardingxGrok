"""
Grok API Client Wrapper
=========================

Purpose:
    Provides a Python client for interacting with the Grok Code API (xAI). Handles
    authentication, request formatting, and response parsing for code analysis tasks.

Key Responsibilities:
    - Authenticate with Grok API using API key
    - Send chat completion requests
    - Format codebase analysis prompts
    - Handle API responses and errors
    - Manage HTTP client lifecycle

Main Methods:
    - chat_completion(): Generic chat completion API call
    - analyze_codebase(): Specialized method for codebase analysis
        - Supports different tasks: "analyze", "summarize", "identify_abstractions", "generate_chapters"
    - close(): Cleanup HTTP client

Configuration:
    - API Key: From Config.XAI_API_KEY
    - Model: Config.XAI_MODEL (default: grok-code-fast-1)
    - Base URL: Config.XAI_BASE_URL (default: https://api.x.ai/v1)
    - Timeout: 300 seconds (5 minutes) for large codebases

Task Types:
    The analyze_codebase() method uses different prompts for different tasks:
        - "analyze": General codebase analysis
        - "summarize": High-level summary generation
        - "identify_abstractions": Pattern and abstraction identification
        - "generate_chapters": Tutorial chapter generation

Context Management:
    - Automatically selects key files to stay within API context limits
    - Truncates file contents if needed (max ~200k characters)
    - Limits each file to 5000 characters in context

Error Handling:
    - Raises exceptions for HTTP errors
    - Handles API response format variations
    - Provides clear error messages

Dependencies:
    - httpx: Async HTTP client
    - config: Configuration settings
"""
import httpx
import json
from typing import Optional, Dict, Any, AsyncIterator
from config import Config


class GrokClient:
    """Client for interacting with Grok Code API."""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, model: Optional[str] = None):
        """Initialize Grok API client."""
        self.api_key = api_key or Config.XAI_API_KEY
        self.base_url = base_url or Config.XAI_BASE_URL
        self.model = model or Config.XAI_MODEL
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            timeout=300.0  # 5 minutes for large code analysis
        )
    
    async def chat_completion(
        self,
        messages: list,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Send a chat completion request to Grok API.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response
            
        Returns:
            API response dictionary
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
        
        if stream:
            payload["stream"] = True
        
        try:
            response = await self.client.post("/chat/completions", json=payload)
            response.raise_for_status()
            
            if stream:
                return response  # Return response object for streaming
            else:
                return response.json()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Grok API error: {e.response.text}") from e
        except Exception as e:
            raise Exception(f"Failed to call Grok API: {str(e)}") from e
    
    async def analyze_codebase(
        self,
        codebase_summary: str,
        files_content: Dict[str, str],
        task: str = "analyze"
    ) -> str:
        """
        Analyze a codebase using Grok API.
        
        Args:
            codebase_summary: Summary of the codebase structure
            files_content: Dictionary mapping file paths to their content
            task: Task type ('analyze', 'summarize', 'identify_abstractions', 'generate_chapters')
            
        Returns:
            Analysis result as string
        """
        # Build context from codebase
        context = f"Codebase Summary:\n{codebase_summary}\n\n"
        context += "Key Files:\n"
        
        # Include file contents (truncate if too long)
        total_chars = len(context)
        max_context = 200000  # Leave room for prompt and response
        
        for file_path, content in files_content.items():
            file_entry = f"\n--- {file_path} ---\n{content[:5000]}\n"  # Limit each file to 5k chars
            if total_chars + len(file_entry) > max_context:
                break
            context += file_entry
            total_chars += len(file_entry)
        
        # Create task-specific prompts
        prompts = {
            "analyze": """Analyze this codebase and provide a comprehensive overview including:
1. Main purpose and functionality
2. Architecture and design patterns
3. Key components and their relationships
4. Entry points and main workflows""",
            
            "summarize": """Provide a concise, high-level summary of this codebase that explains:
1. What the project does
2. Main technologies and frameworks used
3. Overall architecture
4. Key features and capabilities""",
            
            "identify_abstractions": """Identify the core abstractions, design patterns, and architectural components in this codebase.
For each abstraction, provide:
- Name and type (design pattern, architecture pattern, abstraction)
- Description of what it is and how it's used
- Files/modules where it appears
- Examples of usage

Format as JSON with this structure:
{
  "abstractions": [
    {
      "name": "Pattern Name",
      "description": "Description",
      "pattern_type": "design_pattern|architecture|abstraction",
      "files": ["file1.py", "file2.py"],
      "examples": ["code snippet 1", "code snippet 2"]
    }
  ]
}""",
            
            "generate_chapters": """Break down this codebase into logical tutorial chapters.
Each chapter should cover a cohesive topic (e.g., "Core Components", "Data Models", "API Endpoints").
For each chapter, provide:
- Title
- Detailed content explaining the concepts
- List of relevant files
- Order/number

Format as JSON with this structure:
{
  "chapters": [
    {
      "title": "Chapter Title",
      "content": "Detailed explanation...",
      "files": ["file1.py", "file2.py"],
      "order": 1,
      "sections": [
        {"title": "Section 1", "content": "..."}
      ]
    }
  ]
}"""
        }
        
        prompt = prompts.get(task, prompts["analyze"])
        
        messages = [
            {
                "role": "system",
                "content": "You are an expert software engineer and technical writer. Analyze codebases and create clear, educational content."
            },
            {
                "role": "user",
                "content": f"{prompt}\n\n{context}"
            }
        ]
        
        response = await self.chat_completion(messages, temperature=0.3, max_tokens=8000)
        
        if "choices" in response and len(response["choices"]) > 0:
            return response["choices"][0]["message"]["content"]
        else:
            raise Exception("Unexpected response format from Grok API")
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

