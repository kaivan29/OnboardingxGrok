"""
Analysis Prompts Configuration
===============================

Purpose:
    Maps experience levels to analysis prompt templates for codebase analysis.
    These prompts are used by the LLM to generate tailored onboarding plans.

Configuration:
    - junior: Beginner-friendly onboarding focused on fundamentals
    - senior: Advanced onboarding focused on architecture and ownership
"""

from pathlib import Path
from typing import Dict, Optional

# Prompt templates directory
PROMPTS_DIR = Path(__file__).parent / "data" / "analysis_prompts"

# Experience level to prompt file mapping
PROMPT_TEMPLATES = {
    "junior": "junior_engineer_prompt.md",
    "senior": "senior_engineer_prompt.md"
}


def get_prompt_template(experience_level: str) -> Optional[str]:
    """
    Load the appropriate prompt template based on experience level.
    
    Args:
        experience_level: Either "junior" or "senior"
        
    Returns:
        Prompt template text, or None if not found
    """
    template_file = PROMPT_TEMPLATES.get(experience_level.lower())
    
    if not template_file:
        # Default to junior if invalid level
        template_file = PROMPT_TEMPLATES["junior"]
    
    prompt_path = PROMPTS_DIR / template_file
    
    if not prompt_path.exists():
        return None
    
    with open(prompt_path, 'r') as f:
        return f.read()


def get_all_prompt_templates() -> Dict[str, str]:
    """
    Load all available prompt templates.
    
    Returns:
        Dictionary mapping experience level to prompt template text
    """
    templates = {}
    
    for level, filename in PROMPT_TEMPLATES.items():
        prompt_path = PROMPTS_DIR / filename
        if prompt_path.exists():
            with open(prompt_path, 'r') as f:
                templates[level] = f.read()
    
    return templates


def determine_experience_level(profile_data: dict) -> str:
    """
    Determine experience level from analyzed profile.
    
    Args:
        profile_data: Analyzed resume profile data
        
    Returns:
        "junior" or "senior"
    """
    analysis = profile_data.get("analysis", {})
    
    # Extract years of experience
    years = analysis.get("experience_years", 0)
    
    # Simple heuristic: 3+ years = senior, otherwise junior
    # You can customize this logic based on your needs
    if isinstance(years, (int, float)) and years >= 3:
        return "senior"
    elif isinstance(years, str):
        # Try to parse string like "5 years"
        try:
            num = float(''.join(filter(str.isdigit, years)))
            if num >= 3:
                return "senior"
        except:
            pass
    
    return "junior"
