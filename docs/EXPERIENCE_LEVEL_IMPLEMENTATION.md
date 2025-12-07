# Experience-Level Based Onboarding Implementation Summary

## Overview

We have successfully implemented an experience-level-based onboarding system that tailors codebase analysis and study plans to individual new hires based on their background.

## What Was Implemented

### 1. Analysis Prompt Templates

Created two comprehensive prompt templates for LLM-based codebase analysis:

#### **Junior Engineer Prompt** (`data/analysis_prompts/junior_engineer_prompt.md`)
- **Target**: 0-3 years of experience
- **Focus**: 
  - Fundamental concepts and domain knowledge
  - Essential code entry points
  - Safe, hands-on learning tasks
  - Progressive learning path
- **Output Structure**:
  1. Required domain knowledge
  2. Must-study code paths
  3. Ramp-up tasks (3-5 items)
  4. First 2 weeks schedule

#### **Senior Engineer Prompt** (`data/analysis_prompts/senior_engineer_prompt.md`)
- **Target**: 3+ years of experience  
- **Focus**:
  - Architecture-level concepts
  - Critical code ownership areas
  - High-impact engineering tasks
  - Cross-module understanding
- **Output Structure**:
  1. Critical architecture concepts
  2. High-priority code areas to master
  3. High-impact ramp-up tasks (3-6 items)
  4. First 4-6 weeks roadmap

### 2. Configuration System

#### **`config_prompts.py`**
Central configuration for prompt management:
- `PROMPT_TEMPLATES`: Maps experience levels to prompt files
- `get_prompt_template(level)`: Loads the appropriate prompt
- `get_all_prompt_templates()`: Retrieves all available prompts
- `determine_experience_level(profile)`: Automatically detects experience level from resume
  - Heuristic: 3+ years → senior, < 3 years → junior

#### **`config_repos.py`** (Updated)
Added configuration for multi-level analysis:
```python
ANALYSIS_CONFIG = {
    "generate_for_levels": ["junior", "senior"],
    # ... other settings
}
```

### 3. Enhanced Codebase Scheduler

**File**: `services/codebase_scheduler.py`

#### Changes:
- **Multi-level Analysis**: Now generates separate analyses for each experience level
- **Prompt Integration**: Uses configured prompts to guide LLM analysis
- **Structured Storage**: Stores analyses in a new format supporting multiple levels

#### New Storage Format:
```json
{
  "repo_url": "https://github.com/facebook/rocksdb",
  "analyzed_at": "2025-12-07T04:30:00Z",
  "analysis_id": "facebook_rocksdb_20251207_043000",
  "metadata": {
    "repo_name": "facebook_rocksdb",
    "analysis_version": "2.0",
    "includes_prompts": true,
    "experience_levels": ["junior", "senior"]
  },
  "analyses": {
    "junior": {
      "summary": {...},
      "chapters": [...],
      "knowledge_graph": {...}
    },
    "senior": {
      "summary": {...},
      "chapters": [...],
      "knowledge_graph": {...}
    }
  },
  // Backward compatibility: root-level fields use junior analysis
  "summary": {...},
  "chapters": [...],
  "knowledge_graph": {...}
}
```

### 4. Smart Study Plan Generator

**File**: `services/study_plan_generator.py`

#### Enhanced Logic:
1. **Automatic Experience Detection**:
   ```python
   experience_level = determine_experience_level(profile)
   # Returns "junior" or "senior" based on years of experience
   ```

2. **Level-Specific Analysis Selection**:
   - Checks if codebase has multi-level analyses
   - Selects the appropriate analysis based on detected experience level
   - Falls back to default analysis for backward compatibility

3. **Metadata Tracking**:
   - Study plans now include `experience_level` field
   - Tracks which analysis was used

### 5. Updated .gitignore

Modified to allow version control of prompt templates:
```gitignore
data/
!data/.gitkeep
!data/analysis_prompts/
```

### 6. Comprehensive Documentation

Created `data/analysis_prompts/README.md`:
- Complete guide to the prompts system
- Configuration instructions
- Customization guidelines
- Testing procedures
- Best practices

Updated main `README.md`:
- Added feature description
- Updated project structure
- Documented new configuration files

## How It Works End-to-End

### 1. Resume Upload
```
User uploads resume → Resume analyzed by Grok
→ Experience determined (junior/senior)
→ Profile stored with metadata
```

### 2. Periodic Codebase Analysis
```
Scheduler runs daily →
For each configured repo:
  - Load junior prompt template
  - Analyze codebase with junior focus
  - Store junior analysis
  
  - Load senior prompt template
  - Analyze codebase with senior focus
  - Store senior analysis
  
→ Save combined analysis with both levels
```

### 3. Study Plan Generation
```
Request: /api/generateStudyPlan
→ Load user profile
→ Determine experience level from profile
→ Load latest codebase analysis
→ Select appropriate level-specific analysis
→ Generate personalized study plan
→ Save and return plan
```

## Testing the Implementation

### 1. Test Manual Analysis Trigger
```bash
# Trigger analysis job
curl -X POST http://localhost:8080/api/codebases/trigger

# View generated analyses
curl http://localhost:8080/api/codebases
```

### 2. Test Resume Analysis with Study Plan
```bash
# Upload resume (auto-generates plan)
curl -X POST http://localhost:8080/api/analyzeResume \
  -F "resume=@elon_musk_junior_backend_resume_one_page.pdf" \
  -F "repo_url=https://github.com/facebook/rocksdb" \
  -F "generate_plan=true"
```

### 3. Verify Experience Level Detection
```bash
# Get profile to see detected level
curl http://localhost:8080/api/getProfile/{profile_id}

# Get study plan to see which analysis was used
curl http://localhost:8080/api/getStudyPlan/{profile_id}
```

## Key Benefits

### 1. **Personalization at Scale**
- Each new hire receives content tailored to their experience level
- No manual configuration needed - automatic detection

### 2. **Configurable and Extensible**
- Easy to add new experience levels (intern, mid-level, staff, etc.)
- Prompts can be updated without code changes
- Template-based approach allows rapid iteration

### 3. **Backward Compatible**
- Existing endpoints continue to work
- Old analyses without multi-level support still function
- Gradual migration path

### 4. **Separation of Concerns**
- Prompts managed separately from code
- Configuration centralized
- Easy to test and modify

## Future Enhancements

### Short Term
- [ ] Add more experience levels (intern, mid-level, staff, principal)
- [ ] Implement prompt versioning
- [ ] Add prompt validation

### Medium Term
- [ ] Domain-specific prompts (ML engineer, backend, frontend, etc.)
- [ ] Prompt A/B testing
- [ ] Learning outcome tracking

### Long Term
- [ ] Dynamic prompt generation based on team needs
- [ ] Machine learning to optimize prompts
- [ ] Cross-team knowledge sharing

## File Changes Summary

### New Files Created
1. `data/analysis_prompts/junior_engineer_prompt.md` - Junior prompt template
2. `data/analysis_prompts/senior_engineer_prompt.md` - Senior prompt template
3. `data/analysis_prompts/README.md` - Prompts documentation
4. `config_prompts.py` - Prompts configuration module
5. `docs/EXPERIENCE_LEVEL_IMPLEMENTATION.md` - This file

### Modified Files
1. `.gitignore` - Allow prompts directory
2. `config_repos.py` - Added `generate_for_levels` config
3. `services/codebase_scheduler.py` - Multi-level analysis support
4. `services/study_plan_generator.py` - Level-specific analysis selection
5. `README.md` - Updated documentation

## Configuration Reference

### Adding a New Experience Level

1. **Create Prompt Template**:
   ```bash
   # Create new prompt file
   touch data/analysis_prompts/mid_level_prompt.md
   ```

2. **Update config_prompts.py**:
   ```python
   PROMPT_TEMPLATES = {
       "junior": "junior_engineer_prompt.md",
       "mid": "mid_level_prompt.md",
       "senior": "senior_engineer_prompt.md"
   }
   ```

3. **Update Experience Detection Logic**:
   ```python
   def determine_experience_level(profile_data: dict) -> str:
       years = profile_data.get("analysis", {}).get("experience_years", 0)
       if years < 2:
           return "junior"
       elif years < 5:
           return "mid"
       else:
           return "senior"
   ```

4. **Update config_repos.py**:
   ```python
   ANALYSIS_CONFIG = {
       "generate_for_levels": ["junior", "mid", "senior"],
   }
   ```

## Monitoring and Observability

The system includes logging for key operations:

```python
# In codebase_scheduler.py
logger.info(f"Analysis stored: {storage_path}")
logger.info(f"  - Generated analyses for: {', '.join(experience_levels)}")

# In study_plan_generator.py
print(f"📊 Determined experience level: {experience_level}")
print(f"✅ Using {experience_level}-specific codebase analysis")
```

## Conclusion

This implementation provides a robust, scalable foundation for personalized onboarding. By leveraging configurable LLM prompts and automatic experience detection, we can ensure each new hire receives content optimized for their skill level and learning needs.

The system is production-ready and can be extended to support additional experience levels, domains, and customization as requirements evolve.
