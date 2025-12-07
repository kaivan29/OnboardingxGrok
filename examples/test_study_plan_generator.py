#!/usr/bin/env python3
"""
Demo script for testing the study plan generation feature

This script demonstrates the complete flow:
1. Analyze a resume
2. Generate a personalized study plan based on the resume and a codebase
3. Display the generated plan

Usage:
    python3 examples/test_study_plan_generator.py
"""

import requests
import json
import os
from pathlib import Path

# Get paths
SCRIPT_DIR = Path(__file__).parent
RESUME_FILE = SCRIPT_DIR / "elon_musk_junior_backend_resume_one_page.pdf"
API_URL = os.environ.get("API_URL", "http://localhost:8080")

# RocksDB repository
REPO_URL = "https://github.com/facebook/rocksdb"


def test_study_plan_generation():
    """Test the complete study plan generation workflow."""
    print("🎓 Testing Study Plan Generation")
    print("=" * 60)
    
    # Step 1: Upload and analyze resume
    print("\n📤 Step 1: Uploading resume for analysis...")
    print(f"   File: {RESUME_FILE}")
    
    if not RESUME_FILE.exists():
        print(f"❌ Error: Resume file not found: {RESUME_FILE}")
        return
    
    with open(RESUME_FILE, 'rb') as f:
        files = {'resume': f}
        data = {'candidate_email': 'elon@example.com'}
        
        response = requests.post(
            f"{API_URL}/api/analyzeResume",
            files=files,
            data=data
        )
    
    if response.status_code != 200:
        print(f"❌ Error analyzing resume: {response.status_code}")
        print(response.json())
        return
    
    result = response.json()
    profile_id = result['profile_id']
    analysis = result['analysis']
    
    print(f"✅ Resume analyzed successfully!")
    print(f"   Profile ID: {profile_id}")
    print(f"   Candidate: {analysis.get('candidate_name', 'N/A')}")
    print(f"   Experience: {analysis.get('experience_years', 'N/A')} years")
    
    if 'knowledge_gaps' in analysis:
        print(f"\n📊 Identified Knowledge Gaps:")
        for gap in analysis['knowledge_gaps'][:3]:
            print(f"   • {gap}")
    
    # Step 2: Generate study plan
    print(f"\n🎯 Step 2: Generating personalized study plan...")
    print(f"   Repository: {REPO_URL}")
    print(f"   Duration: 4 weeks")
    
    plan_response = requests.post(
        f"{API_URL}/api/generateStudyPlan",
        data={
            'profile_id': profile_id,
            'repo_url': REPO_URL,
            'duration_weeks': 4,
            'use_ai': True  # Set to False for fallback plan
        }
    )
    
    if plan_response.status_code != 200:
        print(f"❌ Error generating plan: {plan_response.status_code}")
        print(plan_response.json())
        return
    
    plan_result = plan_response.json()
    print("✅ Study plan generated successfully!")
    print(f"   Plan ID: {plan_result.get('plan_id', 'N/A')}")
    
    # Step 3: Display the plan
    print("\n" + "=" * 60)
    print("📚 PERSONALIZED STUDY PLAN")
    print("=" * 60)
    
    plan = plan_result['plan']
    weeks = plan.get('weeks', [])
    
    for week in weeks:
        print(f"\n{'─' * 60}")
        print(f"Week {week['weekId']}: {week['title']}")
        print(f"Status: {week['status']}")
        print(f"{'─' * 60}")
        
        # Show overview (first 200 chars)
        overview = week.get('overview', '').replace('\n', ' ')
        if len(overview) > 200:
            overview = overview[:200] + "..."
        print(f"\nOverview: {overview}")
        
        # Show chapters
        print(f"\n📖 Chapters ({len(week.get('chapters', []))}):")
        for chapter in week.get('chapters', []):
            print(f"   • {chapter['title']}")
            if chapter.get('subItems'):
                print(f"     Sub-sections: {len(chapter['subItems'])}")
        
        # Show tasks
        print(f"\n✓ Tasks ({len(week.get('tasks', []))}):")
        for task in week.get('tasks', []):
            print(f"   • {task['title']}")
            print(f"     {task['description'][:80]}...")
            print(f"     Progress: {task['progress']}%")
    
    # Save full plan to file
    output_dir = Path("examples/output")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"study_plan_{profile_id}.json"
    
    with open(output_file, 'w') as f:
        json.dump(plan_result, f, indent=2)
    
    print("\n" + "=" * 60)
    print("✨ Complete!")
    print(f"\n📁 Full plan saved to: {output_file}")
    print("\n🎉 Next Steps:")
    print("1. Review the generated plan in the JSON file")
    print("2. The plan matches the format expected by client/lib/data/week-content.ts")
    print("3. Frontend can now render this personalized plan!")
    print("4. Integrate with your onboarding dashboard")


if __name__ == "__main__":
    try:
        test_study_plan_generation()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API")
        print("   Make sure the server is running: python3 main.py")
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
