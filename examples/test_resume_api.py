#!/usr/bin/env python3
"""
Test script for the Resume Analysis API
Creates a sample PDF resume and tests the API endpoints
"""

import requests
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from pathlib import Path

def create_sample_resume(filename="test_resume.pdf"):
    """Create a sample PDF resume for testing"""
    
    # Create PDF
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Add content
    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "JANE DOE")
    
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "Software Engineer | jane.doe@email.com | (555) 123-4567")
    
    y -= 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "EDUCATION")
    
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "Bachelor of Science in Computer Science")
    y -= 15
    c.drawString(50, y, "Stanford University, 2019")
    y -= 15
    c.drawString(50, y, "GPA: 3.8/4.0")
    
    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "EXPERIENCE")
    
    y -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Senior Software Engineer - Tech Corp")
    y -= 15
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(50, y, "January 2021 - Present")
    y -= 15
    c.setFont("Helvetica", 9)
    c.drawString(70, y, "• Designed and implemented microservices architecture using Python and Flask")
    y -= 12
    c.drawString(70, y, "• Built RESTful APIs serving 1M+ requests/day")
    y -= 12
    c.drawString(70, y, "• Improved system performance by 40% through optimization")
    y -= 12
    c.drawString(70, y, "• Led team of 3 engineers on cloud migration to AWS")
    
    y -= 25
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Software Engineer - StartupXYZ")
    y -= 15
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(50, y, "June 2019 - December 2020")
    y -= 15
    c.setFont("Helvetica", 9)
    c.drawString(70, y, "• Developed full-stack web applications using React and Node.js")
    y -= 12
    c.drawString(70, y, "• Implemented CI/CD pipelines with GitHub Actions")
    y -= 12
    c.drawString(70, y, "• Worked with PostgreSQL and MongoDB databases")
    
    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "TECHNICAL SKILLS")
    
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "Languages: Python, JavaScript, Java, SQL, Go")
    y -= 15
    c.drawString(50, y, "Frameworks: Flask, Django, React, Node.js, Spring Boot")
    y -= 15
    c.drawString(50, y, "Tools & Technologies: Docker, Kubernetes, AWS, Git, Jenkins")
    y -= 15
    c.drawString(50, y, "Databases: PostgreSQL, MongoDB, Redis, MySQL")
    
    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "PROJECTS")
    
    y -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Distributed Task Queue System")
    y -= 15
    c.setFont("Helvetica", 9)
    c.drawString(70, y, "• Built scalable task processing system handling 100K+ tasks/hour")
    y -= 12
    c.drawString(70, y, "• Technologies: Python, Redis, RabbitMQ, Docker")
    
    c.save()
    print(f"✅ Created sample resume: {filename}")
    return filename


def test_analyze_resume(api_url="http://localhost:8080"):
    """Test the resume analysis endpoint"""
    print("\n🧪 Testing Resume Analysis API...\n")
    
    # Create sample resume
    resume_file = create_sample_resume()
    
    # Test upload and analysis
    print("📤 Uploading resume...")
    
    try:
        with open(resume_file, 'rb') as f:
            files = {'resume': f}
            data = {'candidate_email': 'jane.doe@example.com'}
            
            response = requests.post(
                f"{api_url}/api/analyzeResume",
                files=files,
                data=data
            )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Resume analyzed successfully!\n")
            
            print(f"Profile ID: {result['profile_id']}")
            print(f"Message: {result['message']}\n")
            
            analysis = result['analysis']
            
            if 'warning' in analysis:
                print(f"⚠️  {analysis['warning']}\n")
            
            print("📊 Analysis Results:")
            print(f"  Name: {analysis.get('candidate_name', 'N/A')}")
            print(f"  Experience: {analysis.get('experience_years', 'N/A')} years")
            
            if 'technical_skills' in analysis:
                print("\n  Technical Skills:")
                skills = analysis['technical_skills']
                print(f"    Languages: {', '.join(skills.get('languages', []))}")
                print(f"    Frameworks: {', '.join(skills.get('frameworks', []))[:80]}...")
                print(f"    Tools: {', '.join(skills.get('tools', []))[:80]}...")
            
            if 'strengths' in analysis:
                print("\n  Strengths:")
                for strength in analysis['strengths'][:3]:
                    print(f"    • {strength}")
            
            if 'recommended_learning_path' in analysis:
                print("\n  Recommended Learning:")
                for item in analysis['recommended_learning_path'][:3]:
                    print(f"    • {item}")
            
            # Test retrieve profile
            profile_id = result['profile_id']
            print(f"\n🔍 Retrieving profile {profile_id}...")
            
            profile_response = requests.get(f"{api_url}/api/getProfile/{profile_id}")
            
            if profile_response.status_code == 200:
                profile = profile_response.json()
                print("✅ Profile retrieved successfully!")
                print(f"  Uploaded at: {profile['uploaded_at']}")
                print(f"  Resume filename: {profile['resume_filename']}")
            else:
                print(f"❌ Failed to retrieve profile: {profile_response.status_code}")
            
            # Save full analysis to file
            output_file = f"analysis_{profile_id}.json"
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\n💾 Full analysis saved to: {output_file}")
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.json())
    
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure the server is running:")
        print("   python -m src.app")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        # Cleanup
        if Path(resume_file).exists():
            print(f"\n🗑️  Cleaned up test file: {resume_file}")
            Path(resume_file).unlink()


if __name__ == "__main__":
    test_analyze_resume()
