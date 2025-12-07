#!/usr/bin/env python3
"""
Demo script for testing resume analysis with Elon Musk's resume
"""

import requests
import json
import os

# Get the path to the resume file
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESUME_FILE = os.path.join(SCRIPT_DIR, "elon_musk_junior_backend_resume_one_page.pdf")
# API URL - update if running on different host/port
API_URL = os.environ.get("API_URL", "http://localhost:8080")

def test_elon_resume():
    print("🚀 Testing Resume Analysis API with Elon Musk's Resume\n")
    print("="*60)
    
    # Step 1: Upload and analyze
    print("\n📤 Step 1: Uploading resume...")
    print(f"   File: {RESUME_FILE}")
    
    with open(RESUME_FILE, 'rb') as f:
        files = {'resume': f}
        data = {'candidate_email': 'elon@example.com'}
        
        response = requests.post(
            f"{API_URL}/api/analyzeResume",
            files=files,
            data=data
        )
    
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        print(response.json())
        return
    
    result = response.json()
    print("✅ Resume analyzed successfully!\n")
    
    # Display results
    profile_id = result['profile_id']
    analysis = result['analysis']
    
    print(f"📋 Profile ID: {profile_id}\n")
    
    if 'warning' in analysis:
        print(f"⚠️  Note: {analysis['warning']}")
        print("   To get real AI analysis, set up Grok API key")
        print("   See GROK_SETUP.md for instructions\n")
    
    print("="*60)
    print("📊 CANDIDATE ANALYSIS")
    print("="*60)
    
    print(f"\n👤 Name: {analysis.get('candidate_name', 'N/A')}")
    print(f"💼 Experience: {analysis.get('experience_years', 'N/A')} years")
    
    # Technical Skills
    if 'technical_skills' in analysis:
        print("\n🛠️  TECHNICAL SKILLS:")
        skills = analysis['technical_skills']
        print(f"   Languages: {', '.join(skills.get('languages', []))}")
        print(f"   Frameworks: {', '.join(skills.get('frameworks', []))}")
        print(f"   Tools: {', '.join(skills.get('tools', []))}")
        print(f"   Databases: {', '.join(skills.get('databases', []))}")
    
    # Education
    if 'education' in analysis:
        print("\n🎓 EDUCATION:")
        for edu in analysis['education']:
            print(f"   {edu.get('degree', 'N/A')}")
            print(f"   {edu.get('institution', 'N/A')} ({edu.get('graduation_year', 'N/A')})")
    
    # Experience
    if 'experience_summary' in analysis:
        print("\n💼 EXPERIENCE:")
        for exp in analysis['experience_summary']:
            print(f"   {exp.get('role', 'N/A')} at {exp.get('company', 'N/A')}")
            print(f"   Duration: {exp.get('duration', 'N/A')}")
            if 'key_achievements' in exp:
                print("   Achievements:")
                for achievement in exp['key_achievements']:
                    print(f"     • {achievement}")
    
    # Strengths
    if 'strengths' in analysis:
        print("\n💪 STRENGTHS:")
        for strength in analysis['strengths']:
            print(f"   • {strength}")
    
    # Knowledge Gaps
    if 'knowledge_gaps' in analysis:
        print("\n📈 AREAS FOR GROWTH:")
        for gap in analysis['knowledge_gaps']:
            print(f"   • {gap}")
    
    # Learning Path
    if 'recommended_learning_path' in analysis:
        print("\n🎯 RECOMMENDED LEARNING PATH:")
        for i, item in enumerate(analysis['recommended_learning_path'], 1):
            print(f"   {i}. {item}")
    
    print("\n" + "="*60)
    
    # Step 2: Retrieve profile
    print("\n🔍 Step 2: Testing profile retrieval...\n")
    
    profile_response = requests.get(f"{API_URL}/api/getProfile/{profile_id}")
    
    if profile_response.status_code == 200:
        profile = profile_response.json()
        print("✅ Profile retrieved successfully!")
        print(f"   Profile ID: {profile['profile_id']}")
        print(f"   Email: {profile['candidate_email']}")
        print(f"   Upload Time: {profile['uploaded_at']}")
        print(f"   Filename: {profile['resume_filename']}")
        
        # Show where files are stored
        print(f"\n📁 Files stored:")
        print(f"   Resume: data/resumes/{profile_id}_{profile['resume_filename']}")
        print(f"   Analysis: data/analyzed_profiles/{profile_id}.json")
    else:
        print(f"❌ Failed to retrieve profile: {profile_response.status_code}")
    
    print("\n" + "="*60)
    print("\n✨ Test Complete!")
    print("\nNext Steps:")
    print("1. Set up Grok API key for real AI analysis (see GROK_SETUP.md)")
    print("2. Build frontend to display this analysis")
    print("3. Combine with codebase wiki for personalized onboarding")
    print("4. Create learning path generator endpoint")
    print("\n🚀 Your personalized onboarding system is ready!")

if __name__ == "__main__":
    try:
        test_elon_resume()
    except FileNotFoundError:
        print(f"❌ Error: Could not find {RESUME_FILE}")
        print("   Make sure the file is in the current directory")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API")
        print("   Make sure the server is running: python3 -m src.app")
    except Exception as e:
        print(f"❌ Error: {e}")
