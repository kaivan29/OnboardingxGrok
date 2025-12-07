"""
Codebase Analysis Service
==========================

Purpose:
    Analyzes codebases by crawling files, parsing code structure, and extracting
    information about classes, functions, imports, and dependencies. Supports both
    GitHub repositories (via cloning) and local directories.

Key Responsibilities:
    - Clone GitHub repositories or read local directories
    - Filter files based on include/exclude patterns
    - Parse Python files using AST (Abstract Syntax Tree)
    - Parse JavaScript/TypeScript files using regex patterns
    - Extract code structure (classes, functions, imports)
    - Build dependency graphs from import statements
    - Generate structure summaries

Main Methods:
    - analyze(): Main entry point - analyzes codebase and returns structure
    - _clone_repository(): Clones GitHub repo to temporary directory
    - _collect_files(): Collects files matching patterns
    - _read_files(): Reads file contents
    - _parse_code_structure(): Parses code to extract structure
    - _build_dependency_graph(): Builds dependency relationships
    - _generate_structure_summary(): Creates text summary

Output:
    Returns dictionary with:
        - files: List of analyzed file paths
        - file_contents: Dictionary mapping file paths to content
        - structure: Parsed structure (modules, classes, functions, imports)
        - dependencies: Dependency graph (file -> imported modules)
        - summary: Text summary of codebase structure
        - root_path: Root path of the codebase

Dependencies:
    - gitpython: For cloning GitHub repositories
    - ast: Python's built-in AST parser
"""
import os
import re
import ast
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
from git import Repo
from config import Config


class CodebaseAnalyzer:
    """Service for analyzing codebase structure and extracting information."""
    
    def __init__(self, max_file_size: int = 100000):
        """Initialize the codebase analyzer."""
        self.max_file_size = max_file_size
        self.temp_dir: Optional[tempfile.TemporaryDirectory] = None
    
    async def analyze(
        self,
        repo_url: Optional[str] = None,
        local_path: Optional[str] = None,
        include_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Analyze a codebase from GitHub URL or local path.
        
        Args:
            repo_url: GitHub repository URL
            local_path: Local directory path
            include_patterns: File patterns to include
            exclude_patterns: File patterns to exclude
            
        Returns:
            Dictionary with codebase structure and metadata
        """
        if repo_url and local_path:
            raise ValueError("Cannot specify both repo_url and local_path")
        if not repo_url and not local_path:
            raise ValueError("Must specify either repo_url or local_path")
        
        include_patterns = include_patterns or Config.DEFAULT_INCLUDE_PATTERNS
        exclude_patterns = exclude_patterns or Config.DEFAULT_EXCLUDE_PATTERNS
        
        # Get codebase path
        if repo_url:
            codebase_path = await self._clone_repository(repo_url)
            is_temp = True
        else:
            codebase_path = Path(local_path)
            is_temp = False
        
        try:
            # Collect files
            files = self._collect_files(codebase_path, include_patterns, exclude_patterns)
            
            # Read file contents
            file_contents = self._read_files(files, codebase_path)
            
            # Parse code structure
            structure = self._parse_code_structure(file_contents)
            
            # Build dependency graph
            dependencies = self._build_dependency_graph(file_contents)
            
            # Generate summary
            summary = self._generate_structure_summary(structure, dependencies)
            
            return {
                "files": files,
                "file_contents": file_contents,
                "structure": structure,
                "dependencies": dependencies,
                "summary": summary,
                "root_path": str(codebase_path)
            }
        finally:
            # Cleanup temp directory if created
            if is_temp and self.temp_dir:
                self.temp_dir.cleanup()
                self.temp_dir = None
    
    async def _clone_repository(self, repo_url: str) -> Path:
        """Clone a GitHub repository to a temporary directory."""
        self.temp_dir = tempfile.TemporaryDirectory()
        temp_path = Path(self.temp_dir.name)
        
        # Clone repository
        if Config.GITHUB_TOKEN:
            # Use token for authentication
            repo_url_with_token = repo_url.replace(
                "https://github.com/",
                f"https://{Config.GITHUB_TOKEN}@github.com/"
            )
            Repo.clone_from(repo_url_with_token, temp_path)
        else:
            Repo.clone_from(repo_url, temp_path)
        
        return temp_path
    
    def _collect_files(
        self,
        root_path: Path,
        include_patterns: List[str],
        exclude_patterns: List[str]
    ) -> List[Path]:
        """Collect files matching include/exclude patterns."""
        files = []
        
        # Convert glob patterns to regex
        include_regexes = [self._glob_to_regex(p) for p in include_patterns]
        exclude_regexes = [self._glob_to_regex(p) for p in exclude_patterns]
        
        for file_path in root_path.rglob("*"):
            if not file_path.is_file():
                continue
            
            # Check file size
            try:
                if file_path.stat().st_size > self.max_file_size:
                    continue
            except (OSError, PermissionError):
                continue
            
            # Get relative path
            rel_path = file_path.relative_to(root_path)
            rel_path_str = str(rel_path).replace("\\", "/")
            
            # Check exclude patterns first
            if any(re.match(pattern, rel_path_str) for pattern in exclude_regexes):
                continue
            
            # Check include patterns
            if any(re.match(pattern, rel_path_str) for pattern in include_regexes):
                files.append(file_path)
        
        return sorted(files)
    
    def _glob_to_regex(self, pattern: str) -> re.Pattern:
        """Convert glob pattern to regex."""
        # Escape special regex characters
        pattern = re.escape(pattern)
        # Replace glob wildcards
        pattern = pattern.replace(r"\*\*", ".*")  # ** matches any path
        pattern = pattern.replace(r"\*", "[^/]*")  # * matches any filename
        pattern = pattern.replace(r"\?", ".")  # ? matches any character
        # Anchor to start
        pattern = "^" + pattern
        return re.compile(pattern)
    
    def _read_files(self, files: List[Path], root_path: Path) -> Dict[str, str]:
        """Read contents of files."""
        file_contents = {}
        
        for file_path in files:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    rel_path = str(file_path.relative_to(root_path))
                    file_contents[rel_path] = content
            except (UnicodeDecodeError, PermissionError, OSError):
                # Skip files that can't be read
                continue
        
        return file_contents
    
    def _parse_code_structure(self, file_contents: Dict[str, str]) -> Dict[str, any]:
        """Parse code structure from file contents."""
        structure = {
            "modules": {},
            "classes": {},
            "functions": {},
            "imports": {}
        }
        
        for file_path, content in file_contents.items():
            if file_path.endswith(".py"):
                try:
                    tree = ast.parse(content, filename=file_path)
                    file_structure = self._parse_python_file(tree, file_path)
                    structure["modules"][file_path] = file_structure
                    
                    # Extract classes and functions
                    for class_name, class_info in file_structure.get("classes", {}).items():
                        structure["classes"][f"{file_path}::{class_name}"] = class_info
                    
                    for func_name, func_info in file_structure.get("functions", {}).items():
                        structure["functions"][f"{file_path}::{func_name}"] = func_info
                    
                    # Extract imports
                    if "imports" in file_structure:
                        structure["imports"][file_path] = file_structure["imports"]
                except SyntaxError:
                    # Skip files with syntax errors
                    continue
            elif file_path.endswith((".js", ".ts", ".jsx", ".tsx")):
                # Basic JavaScript/TypeScript parsing (simplified)
                file_structure = self._parse_js_file(content, file_path)
                structure["modules"][file_path] = file_structure
        
        return structure
    
    def _parse_python_file(self, tree: ast.AST, file_path: str) -> Dict[str, Any]:
        """Parse a Python AST into structure."""
        file_structure = {
            "file_path": file_path,
            "classes": {},
            "functions": {},
            "imports": []
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    file_structure["imports"].append({
                        "module": alias.name,
                        "alias": alias.asname
                    })
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    file_structure["imports"].append({
                        "module": module,
                        "name": alias.name,
                        "alias": alias.asname
                    })
            elif isinstance(node, ast.ClassDef):
                methods = [m.name for m in node.body if isinstance(m, ast.FunctionDef)]
                file_structure["classes"][node.name] = {
                    "name": node.name,
                    "methods": methods,
                    "line": node.lineno,
                    "bases": [self._get_name(base) for base in node.bases]
                }
            elif isinstance(node, ast.FunctionDef):
                if not any(isinstance(parent, ast.ClassDef) for parent in ast.walk(tree) if hasattr(parent, 'body') and node in getattr(parent, 'body', [])):
                    # Top-level function
                    file_structure["functions"][node.name] = {
                        "name": node.name,
                        "line": node.lineno,
                        "args": [arg.arg for arg in node.args.args]
                    }
        
        return file_structure
    
    def _get_name(self, node) -> str:
        """Get name from AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return ""
    
    def _parse_js_file(self, content: str, file_path: str) -> Dict[str, Any]:
        """Basic JavaScript/TypeScript file parsing."""
        file_structure = {
            "file_path": file_path,
            "classes": {},
            "functions": {},
            "imports": []
        }
        
        # Extract imports (basic regex)
        import_pattern = r"import\s+(?:(?:\{[^}]*\}|\*\s+as\s+\w+|\w+)(?:\s*,\s*(?:\{[^}]*\}|\*\s+as\s+\w+|\w+))*\s+from\s+)?['\"]([^'\"]+)['\"]"
        for match in re.finditer(import_pattern, content):
            file_structure["imports"].append({"module": match.group(1)})
        
        # Extract class declarations
        class_pattern = r"class\s+(\w+)(?:\s+extends\s+(\w+))?"
        for match in re.finditer(class_pattern, content):
            file_structure["classes"][match.group(1)] = {
                "name": match.group(1),
                "extends": match.group(2) if match.group(2) else None
            }
        
        # Extract function declarations
        func_pattern = r"(?:export\s+)?(?:async\s+)?function\s+(\w+)|(?:export\s+)?(?:async\s+)?const\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>"
        for match in re.finditer(func_pattern, content):
            func_name = match.group(1) or match.group(2)
            if func_name:
                file_structure["functions"][func_name] = {"name": func_name}
        
        return file_structure
    
    def _build_dependency_graph(self, file_contents: Dict[str, str]) -> Dict[str, List[str]]:
        """Build dependency graph from imports."""
        dependencies = {}
        
        for file_path, content in file_contents.items():
            deps = []
            
            if file_path.endswith(".py"):
                try:
                    tree = ast.parse(content, filename=file_path)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                deps.append(alias.name.split(".")[0])
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                deps.append(node.module.split(".")[0])
                except SyntaxError:
                    pass
            elif file_path.endswith((".js", ".ts", ".jsx", ".tsx")):
                # Extract JS imports
                import_pattern = r"import\s+.*from\s+['\"]([^'\"]+)['\"]"
                for match in re.finditer(import_pattern, content):
                    module = match.group(1)
                    if not module.startswith("."):
                        deps.append(module.split("/")[0])
            
            dependencies[file_path] = list(set(deps))
        
        return dependencies
    
    def _generate_structure_summary(
        self,
        structure: Dict[str, Any],
        dependencies: Dict[str, List[str]]
    ) -> str:
        """Generate a text summary of the codebase structure."""
        summary_parts = []
        
        num_files = len(structure.get("modules", {}))
        num_classes = len(structure.get("classes", {}))
        num_functions = len(structure.get("functions", {}))
        
        summary_parts.append(f"Codebase Structure:")
        summary_parts.append(f"- {num_files} files analyzed")
        summary_parts.append(f"- {num_classes} classes")
        summary_parts.append(f"- {num_functions} functions")
        
        # List main modules
        if structure.get("modules"):
            summary_parts.append("\nMain Modules:")
            for file_path in list(structure["modules"].keys())[:10]:
                summary_parts.append(f"  - {file_path}")
            if len(structure["modules"]) > 10:
                summary_parts.append(f"  ... and {len(structure['modules']) - 10} more")
        
        return "\n".join(summary_parts)

