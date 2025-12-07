# Grokboard

Backend API service for generating codebase tutorials using Grok Code API. This service analyzes codebases (GitHub repositories or local directories) and generates structured tutorial content including summaries, chapters, knowledge graphs, and visualizations.

## Features

- **Codebase Analysis**: Analyze GitHub repositories or local codebase directories
- **Tutorial Generation**: Generate structured tutorial content using Grok Code API
- **Knowledge Graphs**: Build and visualize relationships between code components
- **Abstraction Identification**: Identify design patterns and architectural components
- **Visualizations**: Generate dependency graphs, structure trees, and knowledge graphs

## Setup

### Prerequisites

- Python 3.10+
- Grok API key from [xAI](https://x.ai/api/)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd OnboardingxGrok
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Copy `.env.sample` to `.env` (if available) or create a `.env` file
   - Add your Grok API key:
   ```
   XAI_API_KEY=your_grok_api_key_here
   XAI_MODEL=grok-code-fast-1
   XAI_BASE_URL=https://api.x.ai/v1
   ```
   - Optionally add GitHub token for private repos:
   ```
   GITHUB_TOKEN=your_github_token_here
   ```

## Usage

### Running the API Server

Start the FastAPI server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
- API documentation: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

### API Endpoints

#### POST `/api/analyze`

Analyze a codebase and generate tutorial content.

**Request Body:**
```json
{
  "repo_url": "https://github.com/username/repo",
  "include": ["*.py", "*.js"],
  "exclude": ["tests/*", "node_modules/*"],
  "max_size": 100000,
  "max_abstractions": 10
}
```

Or for local directories:
```json
{
  "local_path": "/path/to/codebase",
  "include": ["*.py"],
  "exclude": ["tests/*"],
  "max_size": 100000
}
```

**Response:**
```json
{
  "summary": "High-level overview of the codebase...",
  "chapters": [
    {
      "title": "Core Components",
      "content": "Detailed explanation...",
      "files": ["src/core.py"],
      "order": 1
    }
  ],
  "knowledge_graph": {
    "nodes": [...],
    "edges": [...]
  },
  "abstractions": [
    {
      "name": "Design Pattern",
      "description": "...",
      "pattern_type": "design_pattern",
      "files": ["src/pattern.py"]
    }
  ],
  "visualizations": {
    "dependency_graph": {...},
    "knowledge_graph": {...},
    "structure_tree": {...}
  }
}
```

#### GET `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

## Project Structure

```
.
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── api/
│   └── routes.py         # API endpoint definitions
├── services/
│   ├── codebase_analyzer.py      # Codebase crawling and parsing
│   ├── tutorial_generator.py     # Grok API integration for content generation
│   └── visualization_generator.py # Graph and diagram generation
├── utils/
│   └── grok_client.py    # Grok API client wrapper
└── models/
    └── schemas.py        # Request/response models
```

## Configuration

Environment variables (set in `.env` file):

- `XAI_API_KEY` (required): Grok API key
- `XAI_MODEL` (optional): Model name (default: `grok-code-fast-1`)
- `XAI_BASE_URL` (optional): API base URL (default: `https://api.x.ai/v1`)
- `GITHUB_TOKEN` (optional): GitHub token for private repos or rate limits
- `DEFAULT_MAX_FILE_SIZE` (optional): Default max file size in bytes (default: 100000)

## Development

The backend is designed to work with a frontend application. The API returns structured JSON that can be consumed by any frontend framework.

### Example Frontend Integration

```javascript
const response = await fetch('http://localhost:8000/api/analyze', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    repo_url: 'https://github.com/username/repo',
    include: ['*.py'],
    exclude: ['tests/*']
  })
});

const tutorial = await response.json();
console.log(tutorial.summary);
console.log(tutorial.chapters);
```

## License

MIT
