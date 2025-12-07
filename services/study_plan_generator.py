"""
Study Plan Generator Service
=============================

Purpose:
    Generate personalized weekly study plans that match the frontend week-content.ts format.
    Combines user profile (from resume analysis) with codebase analysis to create
    customized onboarding content.

Author: System
Date: 2025-12-07
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

# Try to import Grok client
try:
    from utils.grok_client import GrokClient
    GROK_AVAILABLE = True
except ImportError:
    GROK_AVAILABLE = False


class StudyPlanGenerator:
    """Generate personalized study plans based on user profile and codebase analysis."""
    
    def __init__(self):
        """Initialize the study plan generator."""
        self.data_dir = Path("data")
        self.profiles_dir = self.data_dir / "analyzed_profiles"
        self.codebase_dir = self.data_dir / "codebase_analyses"
        self.plans_dir = self.data_dir / "study_plans"
        
        # Ensure directories exist
        self.plans_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize Grok client if available
        if GROK_AVAILABLE:
            try:
                self.grok_client = GrokClient()
            except Exception:
                self.grok_client = None
        else:
            self.grok_client = None
    
    def get_profile(self, profile_id: str) -> Optional[Dict]:
        """Load user profile from analyzed profiles."""
        profile_file = self.profiles_dir / f"{profile_id}.json"
        
        if not profile_file.exists():
            return None
        
        try:
            with open(profile_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading profile: {e}")
            return None
    
    def get_latest_codebase_analysis(self, repo_url: str) -> Optional[Dict]:
        """Get the latest analysis for a specific repository."""
        # Extract repo name from URL
        repo_name = repo_url.rstrip('/').split('/')[-2] + '_' + repo_url.rstrip('/').split('/')[-1]
        repo_name = repo_name.replace('-', '_').replace('.', '_')
        
        # Find all analyses for this repo
        pattern = f"{repo_name}_*.json"
        analyses = sorted(self.codebase_dir.glob(pattern), reverse=True)
        
        if not analyses:
            return None
        
        # Return the most recent
        try:
            with open(analyses[0], 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading codebase analysis: {e}")
            return None
    
    async def generate_plan_with_grok(
        self,
        profile: Dict,
        codebase: Dict,
        duration_weeks: int = 4
    ) -> Dict:
        """Use Grok to generate a personalized study plan."""
        
        if not self.grok_client:
            raise ValueError("Grok client not available. Cannot generate AI-powered plan.")
        
        # Build the prompt
        prompt = f"""Generate a personalized {duration_weeks}-week onboarding study plan for a new software engineer.

The plan should match this JSON structure EXACTLY:

{{
  "weeks": [
    {{
      "weekId": 1,
      "title": "Week Title",
      "status": "start",  // one of: "completed", "continue", "start", "locked"
      "overview": "# Overview\\n\\nMarkdown content for week overview...\\n\\n## Key takeaways\\n\\n- Point 1\\n- Point 2",
      "chapters": [
        {{
          "id": "chapter-slug",
          "title": "Chapter Title",
          "content": "# Chapter Title\\n\\nMarkdown content...\\n\\n## Section\\n\\nMore content...",
          "subItems": [
            {{ "id": "section-slug", "title": "Section Title" }}
          ]
        }}
      ],
      "tasks": [
        {{
          "id": "task-1-1",
          "title": "Task Title",
          "description": "Detailed task description",
          "assignedBy": "Mentor Name",
          "timeAgo": "2 hrs ago",
          "progress": 0  // 0-100
        }}
      ]
    }}
  ]
}}

CANDIDATE PROFILE:
Name: {profile['analysis'].get('candidate_name', 'Unknown')}
Experience: {profile['analysis'].get('experience_years', 0)} years
Technical Skills: {json.dumps(profile['analysis'].get('technical_skills', {}))}
Strengths: {json.dumps(profile['analysis'].get('strengths', []))}
Knowledge Gaps: {json.dumps(profile['analysis'].get('knowledge_gaps', []))}
Recommended Learning Path: {json.dumps(profile['analysis'].get('recommended_learning_path', []))}

CODEBASE INFORMATION:
Repository: {codebase.get('repo_url', 'Unknown')}
Overview: {codebase['summary'].get('overview', 'N/A')}
Purpose: {codebase['summary'].get('purpose', 'N/A')}
Key Components: {json.dumps(codebase['summary'].get('key_components', []))}
Technologies: {json.dumps(codebase['summary'].get('technologies', []))}
Difficulty Level: {codebase['summary'].get('difficulty_level', 'intermediate')}

Chapters Available in Codebase:
{json.dumps([ch['title'] for ch in codebase.get('chapters', [])], indent=2)}

REQUIREMENTS:
1. Create a {duration_weeks}-week plan that addresses the candidate's knowledge gaps
2. Week 1 should have status "start", later weeks should be "locked" or "continue" based on progression
3. Each week should have 2-4 chapters with detailed markdown content
4. Each chapter should have subItems that match the headings in the content
5. Include 2-3 practical tasks per week that relate to the codebase
6. Use the codebase chapters as source material for learning
7. Tasks should be specific and actionable
8. Overview should explain the week's focus and key takeaways
9. Content should be in markdown format with proper headings
10. First week should focus on gaps, later weeks on deeper codebase concepts

Return ONLY valid JSON, no additional text."""

        # Call Grok API
        try:
            response = await self.grok_client.client.chat.completions.create(
                model=self.grok_client.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert technical onboarding specialist who creates personalized learning plans for software engineers. You return only valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.4,
                max_tokens=8000
            )
            
            # Extract and parse JSON
            content = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if content.startswith("```json"):
                content = content[7:-3].strip()
            elif content.startswith("```"):
                content = content[3:-3].strip()
            
            plan = json.loads(content)
            return plan
            
        except Exception as e:
            raise ValueError(f"Failed to generate plan with Grok: {str(e)}")
    
    def generate_fallback_plan(
        self,
        profile: Dict,
        codebase: Dict,
        duration_weeks: int = 4
    ) -> Dict:
        """Generate a basic plan without AI (fallback)."""
        
        # Extract key information
        candidate_name = profile['analysis'].get('candidate_name', 'New Hire')
        gaps = profile['analysis'].get('knowledge_gaps', [])
        strengths = profile['analysis'].get('strengths', [])
        codebase_chapters = codebase.get('chapters', [])
        technologies = codebase['summary'].get('technologies', [])
        
        weeks = []
        
        # Week 1: Foundations & Setup
        weeks.append({
            "weekId": 1,
            "title": "Foundations & Setup",
            "status": "start",
            "overview": f"""# Overview

Welcome to your personalized onboarding plan, {candidate_name}! This week focuses on getting you set up and reviewing fundamental concepts.

Based on your resume analysis, we've identified some areas to strengthen before diving deep into the codebase.

## Key takeaways

- Set up your development environment
- Review foundational concepts
- Get familiar with the codebase structure
- Complete your first code review""",
            "chapters": [
                {
                    "id": "environment-setup",
                    "title": "Environment Setup",
                    "content": """# Environment Setup

Setting up your development environment is the first critical step in your onboarding journey.

## Prerequisites

Before you begin, ensure you have the necessary tools installed on your system.

## Installation Steps

Follow these steps to get your environment ready for development.

### Step 1: Clone the Repository

Clone the repository to your local machine and navigate to the project directory.

### Step 2: Install Dependencies

Install all required dependencies using your package manager.

### Step 3: Verify Installation

Run the tests to ensure everything is working correctly.""",
                    "subItems": [
                        {"id": "prerequisites", "title": "Prerequisites"},
                        {"id": "installation-steps", "title": "Installation Steps"},
                        {"id": "verify-installation", "title": "Verify Installation"}
                    ]
                },
                {
                    "id": "codebase-overview",
                    "title": "Codebase Overview",
                    "content": f"""# Codebase Overview

Understanding the structure and architecture of the codebase is essential for effective contribution.

## Project Structure

This project uses {', '.join(technologies)} and follows industry best practices.

## Key Components

The codebase is organized into several major components:

{chr(10).join([f'- {comp}' for comp in codebase['summary'].get('key_components', [])])}

## How to Navigate

Start by exploring the main directories and familiarizing yourself with the project layout.""",
                    "subItems": [
                        {"id": "project-structure", "title": "Project Structure"},
                        {"id": "key-components", "title": "Key Components"},
                        {"id": "how-to-navigate", "title": "How to Navigate"}
                    ]
                }
            ],
            "tasks": [
                {
                    "id": "task-1-1",
                    "title": "Complete Environment Setup",
                    "description": "Set up your local development environment following the setup guide. Verify that you can run the project locally and all tests pass.",
                    "assignedBy": "Onboarding Team",
                    "timeAgo": "1 hr ago",
                    "progress": 0
                },
                {
                    "id": "task-1-2",
                    "title": "Explore Codebase Structure",
                    "description": "Navigate through the codebase and document the main directories and their purposes. Create a personal reference guide.",
                    "assignedBy": "Onboarding Team",
                    "timeAgo": "1 hr ago",
                    "progress": 0
                }
            ]
        })
        
        # Week 2: Core Concepts
        week2_chapters = []
        for i, chapter in enumerate(codebase_chapters[:2]):
            week2_chapters.append({
                "id": chapter['title'].lower().replace(' ', '-'),
                "title": chapter['title'],
                "content": chapter.get('content', f"# {chapter['title']}\n\nLearn about {chapter['title']} in this chapter."),
                "subItems": [
                    {"id": section['heading'].lower().replace(' ', '-'), "title": section['heading']}
                    for section in chapter.get('sections', [])
                ]
            })
        
        if not week2_chapters:
            week2_chapters = [{
                "id": "core-concepts",
                "title": "Core Concepts",
                "content": "# Core Concepts\n\nDeep dive into the fundamental concepts of this codebase.",
                "subItems": []
            }]
        
        weeks.append({
            "weekId": 2,
            "title": "Core Concepts",
            "status": "locked",
            "overview": """# Overview

This week focuses on understanding the core concepts and patterns used in the codebase.

## Key takeaways

- Understand the architecture patterns
- Learn the data flow
- Study the key algorithms
- Practice code review""",
            "chapters": week2_chapters,
            "tasks": [
                {
                    "id": "task-2-1",
                    "title": "Study Core Architecture",
                    "description": "Review the core architecture documentation and diagram the main data flow. Present your understanding to your mentor.",
                    "assignedBy": "Technical Lead",
                    "timeAgo": "1 day ago",
                    "progress": 0
                },
                {
                    "id": "task-2-2",
                    "title": "Fix a Starter Bug",
                    "description": "Pick a 'good first issue' from the issue tracker and submit a pull request. This will help you understand the contribution workflow.",
                    "assignedBy": "Technical Lead",
                    "timeAgo": "1 day ago",
                    "progress": 0
                }
            ]
        })
        
        # Week 3: Advanced Topics
        week3_chapters = []
        for i, chapter in enumerate(codebase_chapters[2:4]):
            week3_chapters.append({
                "id": chapter['title'].lower().replace(' ', '-'),
                "title": chapter['title'],
                "content": chapter.get('content', f"# {chapter['title']}\n\nAdvanced concepts in {chapter['title']}."),
                "subItems": [
                    {"id": section['heading'].lower().replace(' ', '-'), "title": section['heading']}
                    for section in chapter.get('sections', [])
                ]
            })
        
        if not week3_chapters:
            week3_chapters = [{
                "id": "advanced-topics",
                "title": "Advanced Topics",
                "content": "# Advanced Topics\n\nExplore advanced concepts and best practices.",
                "subItems": []
            }]
        
        weeks.append({
            "weekId": 3,
            "title": "Advanced Topics",
            "status": "locked",
            "overview": f"""# Overview

This week addresses your identified knowledge gaps and dives into advanced topics.

## Areas of Focus

Based on your profile, we're focusing on:
{chr(10).join([f'- {gap}' for gap in gaps[:3]]) if gaps else '- Advanced architecture patterns'}

## Key takeaways

- Master advanced concepts
- Apply patterns to real problems
- Build confidence with complex features""",
            "chapters": week3_chapters,
            "tasks": [
                {
                    "id": "task-3-1",
                    "title": "Implement a Feature",
                    "description": "Implement a small feature end-to-end. This should include writing tests, documentation, and getting code review approval.",
                    "assignedBy": "Tech Lead",
                    "timeAgo": "3 days ago",
                    "progress": 0
                }
            ]
        })
        
        # Week 4: Summary & Next Steps
        weeks.append({
            "weekId": 4,
            "title": "Summary & Next Steps",
            "status": "locked",
            "overview": """# Overview

Congratulations on reaching the final week! This week focuses on consolidating your learning and planning your continued growth.

## Key takeaways

- Review all concepts learned
- Identify areas for continued growth
- Set goals for the coming months
- Celebrate your progress!""",
            "chapters": [
                {
                    "id": "onboarding-review",
                    "title": "Onboarding Review",
                    "content": """# Onboarding Review

Let's reflect on your journey over the past few weeks.

## What You've Accomplished

Review all the skills and knowledge you've gained during your onboarding.

## Feedback Session

Schedule a feedback session with your mentor to discuss your progress.

## Next Steps

Set concrete goals for your first 90 days and beyond.""",
                    "subItems": [
                        {"id": "accomplishments", "title": "What You've Accomplished"},
                        {"id": "feedback-session", "title": "Feedback Session"},
                        {"id": "next-steps", "title": "Next Steps"}
                    ]
                }
            ],
            "tasks": [
                {
                    "id": "task-4-1",
                    "title": "Complete Onboarding Survey",
                    "description": "Provide feedback on your onboarding experience to help us improve the process for future hires.",
                    "assignedBy": "People Ops",
                    "timeAgo": "1 week ago",
                    "progress": 0
                }
            ]
        })
        
        return {"weeks": weeks}
    
    async def generate_study_plan(
        self,
        profile_id: str,
        repo_url: str,
        duration_weeks: int = 4,
        use_ai: bool = True
    ) -> Dict:
        """
        Generate a personalized study plan.
        
        Args:
            profile_id: User profile ID from resume analysis
            repo_url: Repository URL for the codebase
            duration_weeks: Number of weeks for the plan (default 4)
            use_ai: Whether to use AI generation (requires Grok API)
        
        Returns:
            Dictionary with study plan in week-content.ts format
        """
        # Load profile
        profile = self.get_profile(profile_id)
        if not profile:
            raise ValueError(f"Profile not found: {profile_id}")
        
        # Load codebase analysis
        codebase = self.get_latest_codebase_analysis(repo_url)
        if not codebase:
            raise ValueError(f"No codebase analysis found for: {repo_url}")
        
        # Generate plan
        if use_ai and self.grok_client:
            try:
                plan = await self.generate_plan_with_grok(profile, codebase, duration_weeks)
            except Exception as e:
                print(f"AI generation failed, using fallback: {e}")
                plan = self.generate_fallback_plan(profile, codebase, duration_weeks)
        else:
            plan = self.generate_fallback_plan(profile, codebase, duration_weeks)
        
        # Add metadata
        result = {
            "success": True,
            "profile_id": profile_id,
            "repo_url": repo_url,
            "generated_at": datetime.now().isoformat(),
            "duration_weeks": duration_weeks,
            "plan": plan
        }
        
        # Save the plan
        plan_id = f"{profile_id}_{repo_url.split('/')[-1]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        plan_file = self.plans_dir / f"{plan_id}.json"
        
        with open(plan_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        result["plan_id"] = plan_id
        return result


# Global instance
_generator_instance = None

def get_generator() -> StudyPlanGenerator:
    """Get or create the global generator instance."""
    global _generator_instance
    if _generator_instance is None:
        _generator_instance = StudyPlanGenerator()
    return _generator_instance
