"""
Codebase Analysis Scheduler
============================

Purpose:
    Runs periodic background jobs to analyze configured codebases using Grok AI
    and stores the results for use in personalized onboarding plans.

Key Responsibilities:
    - Schedule daily analysis jobs
    - Analyze configured repositories with Grok API
    - Store analysis results in JSON files
    - Manage analysis lifecycle

Design:
    - Uses APScheduler for job scheduling
    - Analyses stored in data/codebase_analyses/
    - Uses Grok AI (grok-3 model) for comprehensive curriculum generation
    - Results include: summary, 4-week curriculum, chapters, knowledge graph

Storage Format:
    data/codebase_analyses/
    └── {repo_name}_{timestamp}.json
        ├── repo_url
        ├── analyzed_at
        ├── summary
        ├── curriculum (Grok-generated 4-week plan)
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
        Analyze a repository using Grok API and store the results.
        Generates a comprehensive 4-week onboarding curriculum.
        
        Args:
            repo_url: GitHub repository URL
            config: Analysis configuration (include/exclude patterns, experience levels, etc.)
            
        Returns:
            Analysis ID (filename)
        """
        logger.info(f"Starting Grok AI analysis for: {repo_url}")
        
        # Generate unique ID for this analysis
        timestamp = datetime.now()
        repo_name = self._extract_repo_name(repo_url)
        analysis_id = f"{repo_name}_{timestamp.strftime('%Y%m%d_%H%M%S')}"
        
        # Initialize Grok client
        try:
            from openai import OpenAI
            from config import Config
            
            grok_client = OpenAI(
                api_key=Config.XAI_API_KEY,
                base_url=Config.XAI_BASE_URL
            )
        except Exception as e:
            logger.error(f"Failed to initialize Grok client: {e}")
            raise ValueError(f"Grok API not available: {e}")
        
        # Clone and analyze repository
        try:
            # NOTE: Currently uses hardcoded repo structure info from _get_codebase_info()
            # Future enhancement: Clone repo and analyze actual file structure dynamically
            
            codebase_info = self._get_codebase_info(repo_url, repo_name)
            
        except Exception as e:
            logger.error(f"Failed to fetch codebase info: {e}")
            raise ValueError(f"Could not analyze codebase: {e}")
        
        # Build the comprehensive Staff Engineer prompt
        staff_engineer_prompt = f"""You are a Staff Engineer responsible for onboarding new hires.  
Analyze the provided codebase and generate a complete 4-week onboarding curriculum.

Your output should include:  
- Weekly reading materials (derived strictly from the codebase and its architecture)  
- Weekly quizzes to validate understanding  
- Weekly coding tasks that increase in scope and complexity  

The generated plan must be customized to this specific codebase, not generic.

---

# Repository Information
Repository: {repo_url}
Name: {repo_name}

# Codebase Structure
{codebase_info}

---

# 1. Identify and extract essential knowledge
From the codebase, identify:
- Core architectural components
- Key modules and important abstractions
- Critical data flows and invariants
- Tools, libraries, and frameworks in use
- Any implicit knowledge required to understand the system

Use this to drive the onboarding curriculum.

---

# 2. Construct a 4-week ramp-up plan
The plan should progressively deepen understanding:

### Week 1 — Foundations
Goal: Understand top-level architecture & main flows.
Include:
- Reading: foundational files, entry points, configs, read/write path basics  
- Quiz: high-level architecture, module purpose, basic terminology  
- Coding Task: safe, small changes (tests, documentation, simple bug fix)

### Week 2 — Core Components and Data Flow
Goal: Understand critical components and their relationships.
Include:
- Reading: deeper modules (state machines, storage, networking, compaction, scheduler, etc.)  
- Quiz: reasoning about data transformations or call paths  
- Coding Task: implement a small feature or improve observability

### Week 3 — Advanced Internals and Performance
Goal: Explore deeper subsystems, performance implications, threading.
Include:
- Reading: hotspots, concurrency code, pipelines, IO layers  
- Quiz: identify race conditions, performance bottlenecks, invariants  
- Coding Task: write benchmark, refactor small module, optimize a path

### Week 4 — Ownership & Real Contribution
Goal: Be ready to own part of the system.
Include:
- Reading: complex flows, failure recovery, edge cases, test infra  
- Quiz: design reasoning, how to extend a subsystem safely  
- Coding Task: propose and implement a meaningful improvement or fix

---

# 3. Design reading materials
For each week list:
- Exact file paths from the codebase
- Key functions/classes to study  
- Why these files matter  
- What concepts they teach  
Reference the actual repository structure.

---

# 4. Create weekly quizzes
Each quiz should include:
- Concept questions  
- Code comprehension questions (e.g., "What happens when X is called?")  
- Performance/correctness reasoning  
Quizzes must align with the reading and tasks for that week.

---

# 5. Create weekly coding tasks
Each task must:
- Point to specific modules and functions  
- Explain the value of the task  
- Describe expected learning outcomes  
- Include hints on how to approach the implementation  
Tasks must scale in difficulty week-by-week.

Types of coding tasks to include:
- Week 1: tests, logging, safe refactors  
- Week 2: small features or integration points  
- Week 3: profiling or performance investigation  
- Week 4: real contribution or architectural improvement proposal

---

# 6. Output Format
Respond in valid JSON format with the following structure:

{{
  "summary": {{
    "overview": "Brief overview of the codebase and onboarding approach",
    "purpose": "What this codebase does",
    "key_components": ["Component 1", "Component 2", ...],
    "technologies": ["Tech 1", "Tech 2", ...],
    "difficulty_level": "intermediate|advanced"
  }},
  "weeks": [
    {{
      "week_number": 1,
      "title": "Week 1: Foundations",
      "goal": "Understand top-level architecture & main flows",
      "reading_materials": [
        {{
          "file_path": "path/to/file.cpp",
          "key_functions": ["function1", "function2"],
          "why_it_matters": "Explanation",
          "concepts_taught": ["concept1", "concept2"]
        }}
      ],
      "quiz": [
        {{
          "question": "Question text",
          "type": "concept|code_comprehension|performance",
          "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
          "correct_answer": "A",
          "explanation": "Why this is correct"
        }}
      ],
      "coding_tasks": [
        {{
          "title": "Task title",
          "description": "Detailed description",
          "target_modules": ["module1.cpp", "module2.h"],
          "learning_outcomes": ["outcome1", "outcome2"],
          "hints": ["hint1", "hint2"],
          "difficulty": "easy|medium|hard"
        }}
      ]
    }}
  ]
}}

Return ONLY valid JSON, no markdown code blocks, no additional text.

---

# 7. Tone & Style
- Clear, actionable, specific  
- Should feel like a structured corporate onboarding curriculum  
- Avoid generic or boilerplate suggestions  
- Base 100% of content on codebase analysis"""

        # Call Grok API
        logger.info("Calling Grok API for codebase analysis...")
        try:
            response = grok_client.chat.completions.create(
                model=Config.XAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert Staff Engineer who creates comprehensive, codebase-specific onboarding curricula. You analyze codebases deeply and create actionable 4-week ramp-up plans. You return only valid JSON."
                    },
                    {
                        "role": "user",
                        "content": staff_engineer_prompt
                    }
                ],
                temperature=0.3,
                max_tokens=16000  # Need more tokens for comprehensive curriculum
            )
            
            # Extract and parse JSON
            content = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if content.startswith("```json"):
                content = content[7:-3].strip()
            elif content.startswith("```"):
                content = content[3:-3].strip()
            
            curriculum_data = json.loads(content)
            logger.info("Successfully generated curriculum with Grok AI")
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Grok response as JSON: {e}")
            logger.error(f"Response content: {content[:500]}...")
            raise ValueError(f"Grok returned invalid JSON: {e}")
        except Exception as e:
            logger.error(f"Failed to call Grok API: {e}")
            raise ValueError(f"Grok API call failed: {e}")
        
        # Transform the curriculum data into our storage format
        chapters = []
        for week_data in curriculum_data.get("weeks", []):
            for idx, reading in enumerate(week_data.get("reading_materials", [])):
                chapters.append({
                    "title": f"Week {week_data['week_number']}: {reading.get('file_path', 'Unknown')}",
                    "order": (week_data['week_number'] - 1) * 10 + idx + 1,
                    "content": f"# {reading.get('file_path', 'File')}\n\n{reading.get('why_it_matters', '')}\n\n## Concepts\n" + "\n".join([f"- {c}" for c in reading.get('concepts_taught', [])]),
                    "sections": [
                        {
                            "heading": func,
                            "content": f"Study the {func} function"
                        } for func in reading.get('key_functions', [])[:3]
                    ],
                    "week_number": week_data['week_number'],
                    "reading_material": reading,
                    "quiz": week_data.get('quiz', []),
                    "coding_tasks": week_data.get('coding_tasks', [])
                })
        
        # Build the complete analysis result
        analysis_result = {
            "repo_url": repo_url,
            "analyzed_at": timestamp.isoformat(),
            "analysis_id": analysis_id,
            "generated_with": "grok_staff_engineer_prompt",
            "metadata": {
                "repo_name": repo_name,
                "analysis_version": "3.0",  # Updated version for Grok-generated content
                "is_ai_generated": True,
                "model": Config.XAI_MODEL,
                "prompt_type": "staff_engineer_curriculum"
            },
            "summary": curriculum_data.get("summary", {}),
            "curriculum": curriculum_data,  # Store the full curriculum data
            "chapters": chapters,
            "knowledge_graph": {
                "nodes": [],  # Can be enhanced later
                "edges": []
            }
        }
        
        # Store the analysis
        storage_path = self.storage_dir / f"{analysis_id}.json"
        with open(storage_path, 'w') as f:
            json.dump(analysis_result, f, indent=2)
        
        logger.info(f"✅ AI-generated curriculum stored: {storage_path}")
        logger.info(f"  - {len(curriculum_data.get('weeks', []))} weeks")
        logger.info(f"  - {len(chapters)} chapters")
        
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
    
    
    def _get_codebase_info(self, repo_url: str, repo_name: str) -> str:
        """
        Generate codebase structure information for Grok analysis.
        
        Returns hardcoded structure for known repos (RocksDB) or generic template.
        Future enhancement: Clone and analyze repos dynamically.
        """
        # Hardcoded info for RocksDB (can be extended for other repos)
        if "rocksdb" in repo_url.lower():
            return """
## RocksDB Codebase Structure

### Core Architecture
- **db/**: Core database implementation
  - db_impl.cc/h: Main DB implementation
  - version_set.cc/h: Version management and MVCC
  - write_batch.cc/h: Batched write operations
  - memtable.cc/h: In-memory write buffer

- **table/**: SSTable (Sorted String Table) implementation
  - block_based/: Block-based table format
  - table_builder.cc: Table creation logic
  - table_reader.cc: Table reading logic

- **util/**: Utility functions and helpers
  - coding.cc/h: Encoding/decoding utilities
  - crc32c.cc: Checksums
  - thread_local.cc: Thread-local storage

- **include/rocksdb/**: Public API headers
  - db.h: Main database interface
  - options.h: Configuration options
  - iterator.h: Iterator interface

### Key Concepts
- LSM-Tree (Log-Structured Merge-Tree) architecture
- Memtable → Immutable Memtable → SSTable flush pipeline
- Compaction strategies (leveled, universal, FIFO)
- Write-Ahead Log (WAL) for durability
- Block cache for read performance
- Bloom filters for efficient lookups

### Critical Flows
1. **Write Path**: Client → WriteBatch → Memtable → WAL → Flush → SSTable
2. **Read Path**: Client → Memtable check → Block cache → SSTable lookup
3. **Compaction**: Background threads merge and compact SSTables

### Technologies
- C++17
- Threading: std::thread, mutexes, condition variables
- I/O: POSIX file APIs, mmap
- Compression: Snappy, LZ4, Zstandard
- Testing: Google Test framework
"""
        else:
            # Generic structure for unknown repos
            return f"""
## {repo_name} Codebase

### General Structure
- Source files in standard directories
- Configuration and build files
- Tests and documentation
- README and contributing guides

### Recommended Approach
1. Start with README.md and documentation
2. Identify entry points and main modules
3. Trace through core workflows
4. Study tests to understand behavior
"""
    
    def _extract_repo_name(self, repo_url: str) -> str:
        """Extract repository name from URL."""
        # github.com/owner/repo -> owner_repo
        parts = repo_url.rstrip('/').split('/')
        if len(parts) >= 2:
            return f"{parts[-2]}_{parts[-1]}".replace('.git', '')
        return hashlib.md5(repo_url.encode()).hexdigest()[:12]
    


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
