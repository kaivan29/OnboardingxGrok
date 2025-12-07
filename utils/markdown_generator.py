"""
Markdown Documentation Generator
=================================

Purpose:
    Converts analysis results into markdown documentation files. Generates the main
    output.md file with summary and visualizations, and individual chapter markdown files.

Key Responsibilities:
    - Generate output.md with complete analysis report
    - Generate individual .md files for each tutorial chapter
    - Format markdown with proper headers, sections, and code blocks
    - Include visualization references (SVG images)
    - Structure content for readability

Main Methods:
    - generate_output_md(): Creates main output.md file
        - Includes summary, structure, abstractions, knowledge graph info
        - Adds visualization sections with explanations
        - Includes analysis metadata
    - generate_chapter_md(): Creates individual chapter markdown files
        - Formats chapter title and content
        - Lists related files
        - Includes sections if available

Output Files:
    - output.md: Main report with all analysis results
    - chapter_XX_title.md: Individual chapter files (one per chapter)

Markdown Structure:
    - Uses standard markdown headers (#, ##, ###)
    - Includes code blocks for examples
    - References SVG visualizations with ![alt](path)
    - Formats lists and metadata tables

File Naming:
    - Chapter files: chapter_XX_sanitized_title.md
    - Sanitizes filenames (removes special characters, limits length)

Dependencies:
    - models.schemas: Data models for chapters, abstractions, knowledge graphs
    - pathlib: File path handling
"""
import base64
from pathlib import Path
from typing import Dict, List, Any
from models.schemas import Chapter, Abstraction, KnowledgeGraph, Visualization


class MarkdownGenerator:
    """Generate markdown documentation from analysis results."""
    
    def __init__(self, output_dir: Path):
        """Initialize markdown generator."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_output_md(
        self,
        summary: str,
        structure_summary: str,
        abstractions: List[Abstraction],
        knowledge_graph: KnowledgeGraph,
        visualizations: Dict[str, Visualization],
        metadata: Dict[str, Any]
    ) -> Path:
        """Generate the main output.md file with summary and visualizations."""
        content = []
        
        # Title
        content.append("# Codebase Analysis Report\n")
        content.append(f"*Generated on: {metadata.get('generated_at', 'N/A')}*\n")
        
        # Summary section
        content.append("## Summary\n")
        content.append(summary)
        content.append("\n")
        
        # Structure Overview
        content.append("## Codebase Structure\n")
        content.append("```")
        content.append(structure_summary)
        content.append("```")
        content.append("\n")
        
        # Abstractions section
        if abstractions:
            content.append("## Key Abstractions and Patterns\n")
            for abs in abstractions:
                content.append(f"### {abs.name} ({abs.pattern_type})")
                content.append(f"\n{abs.description}\n")
                if abs.files:
                    content.append("**Related Files:**")
                    for file in abs.files:
                        content.append(f"- `{file}`")
                    content.append("")
                if abs.examples:
                    content.append("**Examples:**")
                    for example in abs.examples:
                        content.append(f"```python\n{example}\n```")
                    content.append("")
        
        # Knowledge Graph section
        content.append("## Knowledge Graph\n")
        content.append(f"The knowledge graph contains **{len(knowledge_graph.nodes)} nodes** and **{len(knowledge_graph.edges)} edges**, ")
        content.append("representing the relationships between modules, classes, functions, and files in the codebase.\n")
        content.append("\n**Node Types:**")
        node_types = {}
        for node in knowledge_graph.nodes:
            node_types[node.type] = node_types.get(node.type, 0) + 1
        for node_type, count in node_types.items():
            content.append(f"- {node_type}: {count}")
        content.append("\n**Relationship Types:**")
        edge_types = {}
        for edge in knowledge_graph.edges:
            edge_types[edge.relationship] = edge_types.get(edge.relationship, 0) + 1
        for rel_type, count in edge_types.items():
            content.append(f"- {rel_type}: {count}")
        content.append("\n")
        
        # Visualizations section
        content.append("## Visualizations\n")
        
        # Dependency Graph
        if "dependency_graph" in visualizations:
            content.append("### Dependency Graph\n")
            content.append("The dependency graph shows how different modules and files depend on each other. ")
            content.append("Arrows indicate import relationships, helping you understand the module hierarchy and dependencies.\n")
            content.append(f"\n![Dependency Graph](dependency_graph.svg)\n")
            content.append("\n")
        
        # Knowledge Graph Visualization
        if "knowledge_graph" in visualizations:
            content.append("### Knowledge Graph Visualization\n")
            content.append("This visualization represents the complete knowledge graph of the codebase, showing all components ")
            content.append("(files, classes, functions) and their relationships. Different colors represent different types of components.\n")
            content.append(f"\n![Knowledge Graph](knowledge_graph.svg)\n")
            content.append("\n")
        
        # Structure Tree
        if "structure_tree" in visualizations:
            content.append("### Code Structure Tree\n")
            content.append("The structure tree provides a hierarchical view of the codebase organization, showing how files contain ")
            content.append("classes and functions, and how classes contain methods. This helps understand the overall architecture.\n")
            content.append(f"\n![Structure Tree](structure_tree.svg)\n")
            content.append("\n")
        
        # Metadata
        content.append("## Analysis Metadata\n")
        content.append(f"- **Files Analyzed:** {metadata.get('files_analyzed', 'N/A')}")
        content.append(f"- **Model Used:** {metadata.get('model_used', 'N/A')}")
        if 'root_path' in metadata:
            content.append(f"- **Root Path:** `{metadata['root_path']}`")
        content.append("\n")
        
        # Write to file
        output_file = self.output_dir / "output.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(content))
        
        return output_file
    
    def generate_chapter_md(self, chapter: Chapter, chapter_num: int) -> Path:
        """Generate a markdown file for a single chapter."""
        content = []
        
        # Title - remove "Chapter X:" prefix if it exists in the title
        title = chapter.title
        if title.startswith(f"Chapter {chapter_num}:"):
            title = title.replace(f"Chapter {chapter_num}:", "").strip()
        elif title.startswith("Chapter "):
            # Remove any "Chapter X:" prefix
            import re
            title = re.sub(r'^Chapter \d+:\s*', '', title).strip()
        
        content.append(f"# Chapter {chapter_num}: {title}\n")
        
        # Content
        content.append(chapter.content)
        content.append("\n")
        
        # Related Files
        if chapter.files:
            content.append("## Related Files\n")
            for file_path in chapter.files:
                content.append(f"- `{file_path}`")
            content.append("\n")
        
        # Sections (if any)
        if chapter.sections:
            content.append("## Sections\n")
            for section in chapter.sections:
                if isinstance(section, dict):
                    section_title = section.get("title", "Untitled Section")
                    section_content = section.get("content", "")
                    content.append(f"### {section_title}\n")
                    content.append(section_content)
                    content.append("\n")
        
        # Write to file
        filename = f"chapter_{chapter_num:02d}_{chapter.title.lower().replace(' ', '_').replace(':', '')}.md"
        # Clean filename
        filename = "".join(c for c in filename if c.isalnum() or c in ('_', '-', '.'))[:100]
        output_file = self.output_dir / filename
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(content))
        
        return output_file

