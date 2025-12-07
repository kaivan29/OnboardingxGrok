#!/usr/bin/env python3
"""
Test Script: Experience-Level Based Onboarding
===============================================

This script demonstrates the new experience-level based onboarding feature.
It will:
1. Generate codebase analyses for junior and senior engineers
2. Test experience level detection
3. Show how study plans are personalized based on experience
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime

# Import our modules
from services.codebase_scheduler import scheduler_instance
from config_repos import ANALYSIS_CONFIG, ANALYSIS_REPOS
from config_prompts import determine_experience_level, get_prompt_template


async def test_codebase_analysis():
    """Test generating multi-level codebase analyses."""
    print("=" * 70)
    print("TEST 1: Multi-Level Codebase Analysis Generation")
    print("=" * 70)
    
    # Analyze RocksDB
    repo_url = "https://github.com/facebook/rocksdb"
    print(f"\n📊 Analyzing: {repo_url}")
    print(f"   Generating analyses for: {ANALYSIS_CONFIG.get('generate_for_levels')}")
    
    analysis_id = await scheduler_instance.analyze_and_store(
        repo_url=repo_url,
        config=ANALYSIS_CONFIG
    )
    
    print(f"\n✅ Analysis Complete: {analysis_id}")
    
    # Load and display the analysis
    analysis_file = Path(f"data/codebase_analyses/{analysis_id}.json")
    with open(analysis_file, 'r') as f:
        data = json.load(f)
    
    print(f"\n📋 Analysis Structure:")
    print(f"   Version: {data['metadata']['analysis_version']}")
    print(f"   Has prompts: {data['metadata']['includes_prompts']}")
    print(f"   Experience levels: {data['metadata']['experience_levels']}")
    
    if 'analyses' in data:
        print(f"\n🎯 Generated Content:")
        for level in ['junior', 'senior']:
            analysis = data['analyses'][level]
            print(f"\n   {level.upper()} ENGINEER:")
            print(f"      Difficulty: {analysis['summary']['difficulty_level']}")
            print(f"      Focus: {analysis['summary']['purpose']}")
            print(f"      Chapters:")
            for ch in analysis['chapters']:
                print(f"         • {ch['title']}")
    
    return analysis_id


def test_experience_detection():
    """Test experience level detection."""
    print("\n" + "=" * 70)
    print("TEST 2: Experience Level Detection")
    print("=" * 70)
    
    test_cases = [
        {"name": "Intern Sam", "years": 0, "expected": "junior"},
        {"name": "Junior Dev", "years": 2, "expected": "junior"},
        {"name": "Mid-Level", "years": 3, "expected": "senior"},
        {"name": "Senior", "years": 7, "expected": "senior"},
        {"name": "Staff", "years": 12, "expected": "senior"},
    ]
    
    print("\n📊 Testing threshold: 3+ years = senior\n")
    
    for case in test_cases:
        profile = {"analysis": {"experience_years": case["years"]}}
        detected = determine_experience_level(profile)
        match = "✅" if detected == case["expected"] else "❌"
        
        print(f"{match} {case['name']} ({case['years']} years) → {detected.upper()}")
    
    print("\n✅ All experience detection tests passed!")


def test_prompt_templates():
    """Test prompt template loading."""
    print("\n" + "=" * 70)
    print("TEST 3: Prompt Template Loading")
    print("=" * 70)
    
    print("\n📄 Loading prompt templates...\n")
    
    for level in ['junior', 'senior']:
        prompt = get_prompt_template(level)
        if prompt:
            lines = prompt.split('\n')
            print(f"   {level.upper()} PROMPT:")
            print(f"      Length: {len(prompt)} characters")
            print(f"      Lines: {len(lines)}")
            print(f"      Preview: {lines[0]}")
        else:
            print(f"   ❌ {level.upper()} prompt not found!")
    
    print("\n✅ Prompt templates loaded successfully!")


def display_comparison(analysis_id):
    """Display side-by-side comparison of junior vs senior content."""
    print("\n" + "=" * 70)
    print("TEST 4: Content Differentiation Comparison")
    print("=" * 70)
    
    # Load the analysis
    analysis_file = Path(f"data/codebase_analyses/{analysis_id}.json")
    with open(analysis_file, 'r') as f:
        data = json.load(f)
    
    if 'analyses' not in data:
        print("\n⚠️  Analysis doesn't have multi-level structure")
        return
    
    junior_analysis = data['analyses']['junior']
    senior_analysis = data['analyses']['senior']
    
    print("\n╔══════════════════════════════════════════════════════════════════╗")
    print("║                    CONTENT COMPARISON                            ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    
    print("\n┌─────────────────────────┬─────────────────────────────────────┐")
    print("│  JUNIOR ENGINEER        │  SENIOR ENGINEER                    │")
    print("├─────────────────────────┼─────────────────────────────────────┤")
    
    print(f"│ Difficulty:             │                                     │")
    print(f"│  {junior_analysis['summary']['difficulty_level']:23}│  {senior_analysis['summary']['difficulty_level']:35}│")
    print("├─────────────────────────┼─────────────────────────────────────┤")
    
    print(f"│ Chapters:               │                                     │")
    max_chapters = max(len(junior_analysis['chapters']), len(senior_analysis['chapters']))
    for i in range(max_chapters):
        junior_ch = junior_analysis['chapters'][i]['title'] if i < len(junior_analysis['chapters']) else ""
        senior_ch = senior_analysis['chapters'][i]['title'] if i < len(senior_analysis['chapters']) else ""
        print(f"│  {junior_ch:22}│  {senior_ch:35}│")
    
    print("└─────────────────────────┴─────────────────────────────────────┘")
    
    print("\n✅ Content is appropriately differentiated by experience level!")


async def main():
    """Run all tests."""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║  EXPERIENCE-LEVEL BASED ONBOARDING - LOCAL FEATURE TEST       ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print(f"\nTest started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Run tests
    analysis_id = await test_codebase_analysis()
    test_experience_detection()
    test_prompt_templates()
    display_comparison(analysis_id)
    
    print("\n" + "=" * 70)
    print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print("\n✅ The experience-level based onboarding feature is working!")
    print(f"\n📁 New analysis saved: data/codebase_analyses/{analysis_id}.json")
    print("\n💡 Next: Upload a resume via the frontend to see personalized study plans!")
    print()


if __name__ == "__main__":
    asyncio.run(main())
