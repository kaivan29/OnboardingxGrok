# Onboarding-x-Grok

Product Use case: Building the brain/knowledge graph for team specific codebase, provide intelligent onboarding experience for new hires:
- Analyze resume to understand the candidate's background and experience
- Analyze codebase to understand the codebase structure and dependencies
- Generate personalized learning plan for new hires
- Provide intelligent onboarding experience for new hires:
  - Generate 4 week learning plan for new hires
    -- Generate Weekly reading material for new hires, reading material is a AI generated WIKI of the codebase
    -- Generate weekly coding tasks for new hires, the coding task should related to codebase
    -- Generate weekly quiz for new hires, the quiz should related to codebase/reading material
 


## 📦 Technology Stack

- **Backend**: FastAPI 0.104.1 for API,
- **AI**: Grok-3 (X.AI): analyze resume, grok code api for codebase analysis, generate learning plan, generate weekly reading material, generate weekly coding tasks, generate weekly quiz
- **Deployment**: Google Cloud Run
- **Frontend**: Next.js (in `client/` directory)

<img width="1388" height="801" alt="Screenshot 2026-06-24 at 1 34 48 PM" src="https://github.com/user-attachments/assets/33fb1f3e-da62-4484-9f19-b9fb5fc6b712" />

