"""
Tutorial Generation Service
============================

Purpose:
    Generates tutorial content from codebase analysis using the Grok Code API. Creates
    summaries, identifies abstractions, generates tutorial chapters, and builds
    knowledge graphs.

Key Responsibilities:
    - Generate high-level codebase summaries using Grok API
    - Identify design patterns and architectural abstractions
    - Generate structured tutorial chapters
    - Build knowledge graphs from code structure
    - Parse and structure Grok API responses

Main Methods:
    - generate_summary(): Creates comprehensive codebase summary
    - identify_abstractions(): Identifies design patterns and abstractions
    - generate_chapters(): Breaks codebase into tutorial chapters
    - build_knowledge_graph(): Constructs graph from code structure (no API call)
    - _select_key_files(): Selects important files for API context
    - _organize_files_by_topic(): Groups files by logical categories
    - _parse_abstractions(): Parses JSON response from Grok API
    - _parse_chapters(): Parses chapter data from Grok API

Grok API Integration:
    Uses different prompts for different tasks:
        - "summarize": High-level overview
        - "identify_abstractions": Pattern identification
        - "generate_chapters": Tutorial chapter generation

Output:
    - Summary: Text summary of the codebase
    - Abstractions: List of identified patterns
    - Chapters: List of tutorial chapters with content
    - Knowledge Graph: Graph structure with nodes and edges

Dependencies:
    - utils.grok_client: Grok API client wrapper
    - models.schemas: Data models for chapters, abstractions, knowledge graphs
"""
import json
from typing import Dict, List, Any
from utils.grok_client import GrokClient
from models.schemas import Chapter, Abstraction, KnowledgeGraph, KnowledgeGraphNode, KnowledgeGraphEdge


class TutorialGenerator:
    """Service for generating tutorial content using Grok API."""
    
    def __init__(self, grok_client: GrokClient):
        """Initialize tutorial generator."""
        self.grok_client = grok_client
    
    async def generate_summary(
        self,
        codebase_summary: str,
        file_contents: Dict[str, str]
    ) -> str:
        """Generate high-level summary of the codebase."""
        # Select key files for context
        key_files = self._select_key_files(file_contents)
        
        result = await self.grok_client.analyze_codebase(
            codebase_summary=codebase_summary,
            files_content=key_files,
            task="summarize"
        )
        
        return result
    
    async def identify_abstractions(
        self,
        codebase_summary: str,
        file_contents: Dict[str, str],
        max_abstractions: int = 10
    ) -> List[Abstraction]:
        """Identify code abstractions and patterns."""
        # Select representative files
        key_files = self._select_key_files(file_contents, max_files=20)
        
        prompt_context = f"Identify up to {max_abstractions} core abstractions."
        
        result = await self.grok_client.analyze_codebase(
            codebase_summary=codebase_summary + "\n\n" + prompt_context,
            files_content=key_files,
            task="identify_abstractions"
        )
        
        # Parse JSON response
        abstractions = self._parse_abstractions(result)
        
        return abstractions[:max_abstractions]
    
    async def generate_chapters(
        self,
        codebase_summary: str,
        file_contents: Dict[str, str],
        structure: Dict[str, Any]
    ) -> List[Chapter]:
        """Generate tutorial chapters from codebase."""
        # Organize files by logical grouping
        organized_files = self._organize_files_by_topic(file_contents, structure)
        
        # Select key files for each topic
        key_files = {}
        for topic, files in organized_files.items():
            for file_path in list(files)[:5]:  # Max 5 files per topic
                if file_path in file_contents:
                    key_files[file_path] = file_contents[file_path]
        
        result = await self.grok_client.analyze_codebase(
            codebase_summary=codebase_summary,
            files_content=key_files,
            task="generate_chapters"
        )
        
        # Parse JSON response
        chapters = self._parse_chapters(result, file_contents)
        
        return chapters
    
    def build_knowledge_graph(
        self,
        structure: Dict[str, Any],
        dependencies: Dict[str, List[str]]
    ) -> KnowledgeGraph:
        """Build knowledge graph from code structure."""
        nodes = []
        edges = []
        node_ids = set()
        
        # Add file/module nodes
        for file_path, module_info in structure.get("modules", {}).items():
            node_id = f"file:{file_path}"
            if node_id not in node_ids:
                nodes.append(KnowledgeGraphNode(
                    id=node_id,
                    label=file_path.split("/")[-1],
                    type="file",
                    file_path=file_path,
                    metadata={"path": file_path}
                ))
                node_ids.add(node_id)
        
        # Add class nodes and edges
        for class_key, class_info in structure.get("classes", {}).items():
            file_path, class_name = class_key.split("::")
            node_id = f"class:{class_key}"
            
            if node_id not in node_ids:
                nodes.append(KnowledgeGraphNode(
                    id=node_id,
                    label=class_name,
                    type="class",
                    file_path=file_path,
                    metadata={
                        "methods": class_info.get("methods", []),
                        "bases": class_info.get("bases", [])
                    }
                ))
                node_ids.add(node_id)
            
            # Edge: file contains class
            file_node_id = f"file:{file_path}"
            if file_node_id in node_ids:
                edges.append(KnowledgeGraphEdge(
                    source=file_node_id,
                    target=node_id,
                    relationship="contains"
                ))
            
            # Edge: class inherits from base
            for base in class_info.get("bases", []):
                base_node_id = f"class:{file_path}::{base}"
                if base_node_id in node_ids:
                    edges.append(KnowledgeGraphEdge(
                        source=node_id,
                        target=base_node_id,
                        relationship="inherits"
                    ))
        
        # Add function nodes and edges
        for func_key, func_info in structure.get("functions", {}).items():
            file_path, func_name = func_key.split("::")
            node_id = f"function:{func_key}"
            
            if node_id not in node_ids:
                nodes.append(KnowledgeGraphNode(
                    id=node_id,
                    label=func_name,
                    type="function",
                    file_path=file_path,
                    metadata={"args": func_info.get("args", [])}
                ))
                node_ids.add(node_id)
            
            # Edge: file contains function
            file_node_id = f"file:{file_path}"
            if file_node_id in node_ids:
                edges.append(KnowledgeGraphEdge(
                    source=file_node_id,
                    target=node_id,
                    relationship="contains"
                ))
        
        # Add dependency edges
        for file_path, deps in dependencies.items():
            file_node_id = f"file:{file_path}"
            if file_node_id not in node_ids:
                continue
            
            for dep in deps:
                # Try to find matching file node
                for other_file, _ in structure.get("modules", {}).items():
                    if dep in other_file or other_file.endswith(f"/{dep}.py"):
                        dep_node_id = f"file:{other_file}"
                        if dep_node_id in node_ids:
                            edges.append(KnowledgeGraphEdge(
                                source=file_node_id,
                                target=dep_node_id,
                                relationship="imports"
                            ))
                        break
        
        return KnowledgeGraph(nodes=nodes, edges=edges)
    
    def _select_key_files(
        self,
        file_contents: Dict[str, str],
        max_files: int = 15
    ) -> Dict[str, str]:
        """Select key files for analysis."""
        # Prioritize files by:
        # 1. Main/entry point files (main.py, index.js, app.py, etc.)
        # 2. Core module files
        # 3. Largest files (more content)
        
        priority_names = ["main", "index", "app", "core", "init", "__main__"]
        
        def file_priority(file_path: str) -> tuple:
            filename = file_path.lower().split("/")[-1]
            # Check if it's a priority file
            for i, name in enumerate(priority_names):
                if name in filename:
                    return (0, i, -len(file_contents[file_path]))
            # Otherwise prioritize by size
            return (1, 0, -len(file_contents[file_path]))
        
        sorted_files = sorted(file_contents.keys(), key=file_priority)
        return {f: file_contents[f] for f in sorted_files[:max_files]}
    
    def _organize_files_by_topic(
        self,
        file_contents: Dict[str, str],
        structure: Dict[str, Any]
    ) -> Dict[str, set]:
        """Organize files by logical topic/category."""
        topics = {
            "Core": set(),
            "API": set(),
            "Models": set(),
            "Utils": set(),
            "Config": set(),
            "Tests": set(),
            "Other": set()
        }
        
        for file_path in file_contents.keys():
            file_lower = file_path.lower()
            
            if any(x in file_lower for x in ["test", "spec", "__test__"]):
                topics["Tests"].add(file_path)
            elif any(x in file_lower for x in ["api", "route", "endpoint", "controller"]):
                topics["API"].add(file_path)
            elif any(x in file_lower for x in ["model", "schema", "entity", "data"]):
                topics["Models"].add(file_path)
            elif any(x in file_lower for x in ["util", "helper", "tool", "common"]):
                topics["Utils"].add(file_path)
            elif any(x in file_lower for x in ["config", "setting", "env"]):
                topics["Config"].add(file_path)
            elif any(x in file_lower for x in ["main", "app", "core", "init"]):
                topics["Core"].add(file_path)
            else:
                topics["Other"].add(file_path)
        
        # Remove empty topics
        return {k: v for k, v in topics.items() if v}
    
    def _parse_abstractions(self, result: str) -> List[Abstraction]:
        """Parse abstractions from Grok API response."""
        abstractions = []
        
        # Try to extract JSON from response
        json_match = None
        if "```json" in result:
            json_start = result.find("```json") + 7
            json_end = result.find("```", json_start)
            if json_end > json_start:
                json_match = result[json_start:json_end].strip()
        elif "{" in result:
            # Try to find JSON object
            json_start = result.find("{")
            json_end = result.rfind("}") + 1
            if json_end > json_start:
                json_match = result[json_start:json_end]
        
        if json_match:
            try:
                data = json.loads(json_match)
                for abs_data in data.get("abstractions", []):
                    abstractions.append(Abstraction(
                        name=abs_data.get("name", "Unknown"),
                        description=abs_data.get("description", ""),
                        pattern_type=abs_data.get("pattern_type", "abstraction"),
                        files=abs_data.get("files", []),
                        examples=abs_data.get("examples", [])
                    ))
            except json.JSONDecodeError:
                # Fallback: create abstraction from text
                pass
        
        # Fallback: create a single abstraction from the text
        if not abstractions:
            abstractions.append(Abstraction(
                name="Codebase Patterns",
                description=result[:500],
                pattern_type="abstraction",
                files=[],
                examples=[]
            ))
        
        return abstractions
    
    def _parse_chapters(self, result: str, file_contents: Dict[str, str]) -> List[Chapter]:
        """Parse chapters from Grok API response."""
        chapters = []
        
        # Try to extract JSON from response
        json_match = None
        if "```json" in result:
            json_start = result.find("```json") + 7
            json_end = result.find("```", json_start)
            if json_end > json_start:
                json_match = result[json_start:json_end].strip()
        elif "{" in result:
            json_start = result.find("{")
            json_end = result.rfind("}") + 1
            if json_end > json_start:
                json_match = result[json_start:json_end]
        
        if json_match:
            try:
                data = json.loads(json_match)
                for i, chapter_data in enumerate(data.get("chapters", [])):
                    # Match files mentioned in chapter to actual files
                    mentioned_files = []
                    chapter_text = chapter_data.get("content", "").lower()
                    for file_path in file_contents.keys():
                        if any(part in chapter_text for part in file_path.lower().split("/")):
                            mentioned_files.append(file_path)
                    
                    chapters.append(Chapter(
                        title=chapter_data.get("title", f"Chapter {i+1}"),
                        content=chapter_data.get("content", ""),
                        files=chapter_data.get("files", mentioned_files[:5]),
                        order=chapter_data.get("order", i+1),
                        sections=chapter_data.get("sections", [])
                    ))
            except json.JSONDecodeError:
                pass
        
        # Fallback: create a single chapter
        if not chapters:
            chapters.append(Chapter(
                title="Overview",
                content=result,
                files=list(file_contents.keys())[:5],
                order=1,
                sections=None
            ))
        
        # Sort by order
        chapters.sort(key=lambda x: x.order)
        
        return chapters

