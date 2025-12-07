"""
Codebase Analysis Scheduler
============================

Purpose:
    Runs periodic background jobs to analyze configured codebases and store
    the results for later use in personalized onboarding plans.

Key Responsibilities:
    - Schedule daily analysis jobs
    - Analyze configured repositories
    - Store analysis results in JSON files
    - Manage analysis lifecycle

Design:
    - Uses APScheduler for job scheduling
    - Analyses stored in data/codebase_analyses/
    - Mock data used until real analysis is implemented
    - Results include: summary, chapters, knowledge graph

Storage Format:
    data/codebase_analyses/
    └── {repo_name}_{timestamp}.json
        ├── repo_url
        ├── analyzed_at
        ├── summary
        ├── chapters
        ├── knowledge_graph
        └── metadata
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

# Storage configuration
STORAGE_DIR = Path("data/codebase_analyses")
STORAGE_DIR.mkdir(parents=True, exist_ok=True)


class CodebaseAnalysisScheduler:
    """Manages periodic codebase analysis jobs."""
    
    def __init__(self):
        """Initialize the scheduler."""
        self.storage_dir = STORAGE_DIR
    
    async def analyze_and_store(self, repo_url: str, config: Dict[str, Any] = None) -> str:
        """
        Analyze a repository and store the results.
        
        Args:
            repo_url: GitHub repository URL
            config: Analysis configuration (include/exclude patterns, etc.)
            
        Returns:
            Analysis ID (filename)
        """
        logger.info(f"Starting analysis for: {repo_url}")
        
        # Generate unique ID for this analysis
        timestamp = datetime.now()
        repo_name = self._extract_repo_name(repo_url)
        analysis_id = f"{repo_name}_{timestamp.strftime('%Y%m%d_%H%M%S')}"
        
        # For now, use mock data
        # TODO: Replace with real analysis by calling services.codebase_analyzer
        analysis_result = self._create_mock_analysis(repo_url, repo_name, timestamp)
        
        # Store the analysis
        storage_path = self.storage_dir / f"{analysis_id}.json"
        with open(storage_path, 'w') as f:
            json.dump(analysis_result, f, indent=2)
        
        logger.info(f"Analysis stored: {storage_path}")
        
        return analysis_id
    
    def get_analysis(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a stored analysis by ID.
        
        Args:
            analysis_id: Analysis identifier
            
        Returns:
            Analysis data or None if not found
        """
        storage_path = self.storage_dir / f"{analysis_id}.json"
        
        if not storage_path.exists():
            return None
        
        with open(storage_path, 'r') as f:
            return json.load(f)
    
    def get_latest_analysis(self, repo_url: str) -> Optional[Dict[str, Any]]:
        """
        Get the most recent analysis for a repository.
        
        Args:
            repo_url: Repository URL
            
        Returns:
            Latest analysis data or None
        """
        repo_name = self._extract_repo_name(repo_url)
        
        # Find all analyses for this repo
        analyses = sorted(
            [f for f in self.storage_dir.glob(f"{repo_name}_*.json")],
            reverse=True
        )
        
        if not analyses:
            return None
        
        with open(analyses[0], 'r') as f:
            return json.load(f)
    
    def list_all_analyses(self) -> list:
        """
        List all stored codebase analyses.
        
        Returns:
            List of analysis metadata
        """
        analyses = []
        
        for analysis_file in self.storage_dir.glob("*.json"):
            try:
                with open(analysis_file, 'r') as f:
                    data = json.load(f)
                    analyses.append({
                        "analysis_id": analysis_file.stem,
                        "repo_url": data.get("repo_url"),
                        "repo_name": data.get("metadata", {}).get("repo_name"),
                        "analyzed_at": data.get("analyzed_at"),
                        "chapters_count": len(data.get("chapters", [])),
                    })
            except Exception as e:
                logger.error(f"Error reading {analysis_file}: {e}")
        
        return sorted(analyses, key=lambda x: x["analyzed_at"], reverse=True)
    
    def _extract_repo_name(self, repo_url: str) -> str:
        """Extract repository name from URL."""
        # github.com/owner/repo -> owner_repo
        parts = repo_url.rstrip('/').split('/')
        if len(parts) >= 2:
            return f"{parts[-2]}_{parts[-1]}".replace('.git', '')
        return hashlib.md5(repo_url.encode()).hexdigest()[:12]
    
    def _create_mock_analysis(
        self,
        repo_url: str,
        repo_name: str,
        timestamp: datetime
    ) -> Dict[str, Any]:
        """
        Create mock analysis data for testing.
        
        TODO: Replace with real analysis from services.codebase_analyzer
        """
        return {
            "repo_url": repo_url,
            "analyzed_at": timestamp.isoformat(),
            "summary": {
                "overview": f"Mock analysis for {repo_name}",
                "purpose": "This is a placeholder analysis used for testing the periodic job system",
                "key_components": [
                    "Main application logic",
                    "API endpoints",
                    "Data models",
                    "Utility functions"
                ],
                "technologies": ["Python", "FastAPI", "SQLAlchemy"],
                "difficulty_level": "intermediate"
            },
            "chapters": [
                {
                    "title": "Getting Started",
                    "order": 1,
                    "content": f"Introduction to {repo_name} codebase",
                    "sections": [
                        {
                            "heading": "Setup",
                            "content": "How to set up the development environment"
                        },
                        {
                            "heading": "Architecture Overview",
                            "content": "High-level architecture and design patterns"
                        }
                    ]
                },
                {
                    "title": "Core Concepts",
                    "order": 2,
                    "content": "Understanding the fundamental concepts",
                    "sections": [
                        {
                            "heading": "Data Models",
                            "content": "Core data structures and their relationships"
                        },
                        {
                            "heading": "Business Logic",
                            "content": "Main application logic and workflows"
                        }
                    ]
                },
                {
                    "title": "API Reference",
                    "order": 3,
                    "content": "Complete API documentation",
                    "sections": [
                        {
                            "heading": "Endpoints",
                            "content": "List of all API endpoints and their usage"
                        }
                    ]
                }
            ],
            "knowledge_graph": {
                "nodes": [
                    {
                        "id": "main_app",
                        "label": "Main Application",
                        "type": "module"
                    },
                    {
                        "id": "api_routes",
                        "label": "API Routes",
                        "type": "module"
                    },
                    {
                        "id": "models",
                        "label": "Data Models",
                        "type": "module"
                    }
                ],
                "edges": [
                    {
                        "source": "main_app",
                        "target": "api_routes",
                        "relationship": "imports"
                    },
                    {
                        "source": "api_routes",
                        "target": "models",
                        "relationship": "uses"
                    }
                ]
            },
            "metadata": {
                "repo_name": repo_name,
                "analysis_version": "1.0",
                "is_mock": True,
                "files_analyzed": 42,
                "total_lines": 15000
            }
        }


# Global scheduler instance
scheduler_instance = CodebaseAnalysisScheduler()


async def scheduled_analysis_job():
    """
    Job function that runs periodically to analyze configured repositories.
    
    This is called by the scheduler and analyzes all repos in config_repos.ANALYSIS_REPOS.
    """
    try:
        from config_repos import ANALYSIS_REPOS, ANALYSIS_CONFIG
        
        logger.info("Starting scheduled codebase analysis job")
        
        for repo_url in ANALYSIS_REPOS:
            try:
                analysis_id = await scheduler_instance.analyze_and_store(
                    repo_url=repo_url,
                    config=ANALYSIS_CONFIG
                )
                logger.info(f"Completed analysis: {analysis_id}")
            except Exception as e:
                logger.error(f"Error analyzing {repo_url}: {e}")
        
        logger.info("Scheduled analysis job completed")
        
    except Exception as e:
        logger.error(f"Error in scheduled_analysis_job: {e}")
