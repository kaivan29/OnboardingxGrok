"""
Visualization Generation Service
==================================

Purpose:
    Generates visual representations of codebase structure, dependencies, and knowledge
    graphs. Creates SVG and PNG images using NetworkX and Matplotlib.

Key Responsibilities:
    - Generate dependency graphs showing module dependencies
    - Generate knowledge graph visualizations
    - Generate code structure trees
    - Export visualizations as SVG or PNG (base64 encoded)
    - Handle graph layout and styling

Main Methods:
    - generate_dependency_graph(): Creates dependency visualization
    - generate_knowledge_graph_visualization(): Visualizes knowledge graph
    - generate_structure_tree(): Creates hierarchical structure tree
    - _render_graph_svg(): Renders graph as SVG string
    - _render_graph_png(): Renders graph as PNG (base64)
    - _render_tree_svg(): Renders tree structure as SVG
    - _render_tree_png(): Renders tree structure as PNG

Visualization Types:
    1. Dependency Graph: Shows import relationships between files
    2. Knowledge Graph: Complete graph with all components and relationships
    3. Structure Tree: Hierarchical view (files -> classes -> methods)

Graph Layout:
    - Uses NetworkX for graph creation and manipulation
    - Uses spring_layout or circular_layout for positioning
    - Optionally uses pygraphviz for hierarchical layouts (if available)
    - Colors nodes by type (file, class, function, method)

Output:
    Returns Visualization objects with:
        - type: Visualization type name
        - format: "svg" or "png"
        - data: Base64 encoded image data

Dependencies:
    - networkx: Graph creation and layout
    - matplotlib: Graph rendering
    - pygraphviz: Optional, for better tree layouts (requires C++ build tools)
"""
import base64
import io
from typing import Dict, Any
import networkx as nx
from matplotlib import pyplot as plt

# Try to import pygraphviz, but it's optional
try:
    import pygraphviz
    HAS_PYGRAPHVIZ = True
except ImportError:
    HAS_PYGRAPHVIZ = False
from models.schemas import KnowledgeGraph, Visualization


class VisualizationGenerator:
    """Service for generating visualizations from codebase analysis."""
    
    def __init__(self):
        """Initialize visualization generator."""
        plt.style.use('default')
    
    def generate_dependency_graph(
        self,
        dependencies: Dict[str, list],
        format: str = "svg"
    ) -> Visualization:
        """Generate dependency graph visualization."""
        G = nx.DiGraph()
        
        # Add nodes and edges
        for file_path, deps in dependencies.items():
            G.add_node(file_path, label=file_path.split("/")[-1])
            for dep in deps:
                # Try to find matching file
                for other_file in dependencies.keys():
                    if dep in other_file or other_file.endswith(f"/{dep}.py"):
                        if other_file != file_path:
                            G.add_edge(file_path, other_file)
                        break
        
        # Generate visualization
        if format == "svg":
            img_data = self._render_graph_svg(G, "Dependency Graph")
        else:
            img_data = self._render_graph_png(G, "Dependency Graph")
        
        return Visualization(
            type="dependency_graph",
            format=format,
            data=img_data
        )
    
    def generate_knowledge_graph_visualization(
        self,
        knowledge_graph: KnowledgeGraph,
        format: str = "svg"
    ) -> Visualization:
        """Generate visualization from knowledge graph."""
        G = nx.DiGraph()
        
        # Add nodes
        node_type_colors = {
            "file": "#E3F2FD",
            "class": "#FFF3E0",
            "function": "#F3E5F5",
            "module": "#E8F5E9"
        }
        
        for node in knowledge_graph.nodes:
            node_type = node.type
            color = node_type_colors.get(node_type, "#FFFFFF")
            G.add_node(
                node.id,
                label=node.label,
                type=node_type,
                color=color
            )
        
        # Add edges
        for edge in knowledge_graph.edges:
            G.add_edge(
                edge.source,
                edge.target,
                relationship=edge.relationship
            )
        
        # Generate visualization
        if format == "svg":
            img_data = self._render_graph_svg(G, "Knowledge Graph", use_colors=True)
        else:
            img_data = self._render_graph_png(G, "Knowledge Graph", use_colors=True)
        
        return Visualization(
            type="knowledge_graph",
            format=format,
            data=img_data
        )
    
    def generate_structure_tree(
        self,
        structure: Dict[str, Any],
        format: str = "svg"
    ) -> Visualization:
        """Generate code structure tree visualization."""
        G = nx.DiGraph()
        
        # Add file nodes
        for file_path, module_info in structure.get("modules", {}).items():
            file_name = file_path.split("/")[-1]
            G.add_node(file_path, label=file_name, type="file")
            
            # Add class nodes
            for class_key, class_info in structure.get("classes", {}).items():
                if class_key.startswith(f"{file_path}::"):
                    class_name = class_key.split("::")[-1]
                    G.add_node(class_key, label=class_name, type="class")
                    G.add_edge(file_path, class_key)
                    
                    # Add method nodes
                    for method in class_info.get("methods", []):
                        method_key = f"{class_key}::{method}"
                        G.add_node(method_key, label=method, type="method")
                        G.add_edge(class_key, method_key)
            
            # Add function nodes
            for func_key, func_info in structure.get("functions", {}).items():
                if func_key.startswith(f"{file_path}::"):
                    func_name = func_key.split("::")[-1]
                    G.add_node(func_key, label=func_name, type="function")
                    G.add_edge(file_path, func_key)
        
        # Generate visualization
        if format == "svg":
            img_data = self._render_tree_svg(G, "Code Structure Tree")
        else:
            img_data = self._render_tree_png(G, "Code Structure Tree")
        
        return Visualization(
            type="structure_tree",
            format=format,
            data=img_data
        )
    
    def _render_graph_svg(
        self,
        G: nx.DiGraph,
        title: str,
        use_colors: bool = False
    ) -> str:
        """Render graph as SVG string."""
        if len(G.nodes) == 0:
            return self._empty_graph_svg(title)
        
        # Use a layout that works well for dependency graphs
        try:
            pos = nx.spring_layout(G, k=1, iterations=50, seed=42)
        except:
            pos = nx.circular_layout(G)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        
        # Draw nodes
        node_colors = []
        if use_colors:
            node_colors = [G.nodes[node].get('color', '#E3F2FD') for node in G.nodes()]
        else:
            node_colors = ['#E3F2FD'] * len(G.nodes())
        
        nx.draw_networkx_nodes(
            G, pos,
            node_color=node_colors,
            node_size=1000,
            alpha=0.9,
            ax=ax
        )
        
        # Draw edges
        nx.draw_networkx_edges(
            G, pos,
            edge_color='gray',
            arrows=True,
            arrowsize=20,
            alpha=0.6,
            ax=ax
        )
        
        # Draw labels
        labels = {node: G.nodes[node].get('label', node.split("/")[-1][:20]) for node in G.nodes()}
        nx.draw_networkx_labels(
            G, pos,
            labels,
            font_size=8,
            ax=ax
        )
        
        ax.axis('off')
        
        # Convert to SVG string
        svg_buffer = io.BytesIO()
        fig.savefig(svg_buffer, format='svg', bbox_inches='tight')
        svg_buffer.seek(0)
        svg_data = svg_buffer.read().decode('utf-8')
        plt.close(fig)
        
        # Encode as base64
        return base64.b64encode(svg_data.encode('utf-8')).decode('utf-8')
    
    def _render_graph_png(
        self,
        G: nx.DiGraph,
        title: str,
        use_colors: bool = False
    ) -> str:
        """Render graph as PNG base64 string."""
        if len(G.nodes) == 0:
            return self._empty_graph_png(title)
        
        try:
            pos = nx.spring_layout(G, k=1, iterations=50, seed=42)
        except:
            pos = nx.circular_layout(G)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        
        node_colors = []
        if use_colors:
            node_colors = [G.nodes[node].get('color', '#E3F2FD') for node in G.nodes()]
        else:
            node_colors = ['#E3F2FD'] * len(G.nodes())
        
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1000, alpha=0.9, ax=ax)
        nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=20, alpha=0.6, ax=ax)
        
        labels = {node: G.nodes[node].get('label', node.split("/")[-1][:20]) for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels, font_size=8, ax=ax)
        
        ax.axis('off')
        
        # Convert to PNG base64
        png_buffer = io.BytesIO()
        fig.savefig(png_buffer, format='png', bbox_inches='tight', dpi=150)
        png_buffer.seek(0)
        png_data = base64.b64encode(png_buffer.read()).decode('utf-8')
        plt.close(fig)
        
        return png_data
    
    def _render_tree_svg(self, G: nx.DiGraph, title: str) -> str:
        """Render tree structure as SVG."""
        if len(G.nodes) == 0:
            return self._empty_graph_svg(title)
        
        # Use hierarchical layout for tree
        if HAS_PYGRAPHVIZ:
            try:
                pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
            except:
                pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
        else:
            try:
                pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
            except:
                pos = nx.circular_layout(G)
        
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        
        # Color nodes by type
        node_colors = []
        for node in G.nodes():
            node_type = G.nodes[node].get('type', 'file')
            colors = {
                'file': '#E3F2FD',
                'class': '#FFF3E0',
                'function': '#F3E5F5',
                'method': '#E8F5E9'
            }
            node_colors.append(colors.get(node_type, '#FFFFFF'))
        
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=800, alpha=0.9, ax=ax)
        nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=15, alpha=0.5, ax=ax)
        
        labels = {node: G.nodes[node].get('label', node.split("::")[-1][:15]) for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels, font_size=7, ax=ax)
        
        ax.axis('off')
        
        svg_buffer = io.BytesIO()
        fig.savefig(svg_buffer, format='svg', bbox_inches='tight')
        svg_buffer.seek(0)
        svg_data = svg_buffer.read().decode('utf-8')
        plt.close(fig)
        
        return base64.b64encode(svg_data.encode('utf-8')).decode('utf-8')
    
    def _render_tree_png(self, G: nx.DiGraph, title: str) -> str:
        """Render tree structure as PNG."""
        if len(G.nodes) == 0:
            return self._empty_graph_png(title)
        
        if HAS_PYGRAPHVIZ:
            try:
                pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
            except:
                pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
        else:
            try:
                pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
            except:
                pos = nx.circular_layout(G)
        
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        
        node_colors = []
        for node in G.nodes():
            node_type = G.nodes[node].get('type', 'file')
            colors = {
                'file': '#E3F2FD',
                'class': '#FFF3E0',
                'function': '#F3E5F5',
                'method': '#E8F5E9'
            }
            node_colors.append(colors.get(node_type, '#FFFFFF'))
        
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=800, alpha=0.9, ax=ax)
        nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=15, alpha=0.5, ax=ax)
        
        labels = {node: G.nodes[node].get('label', node.split("::")[-1][:15]) for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels, font_size=7, ax=ax)
        
        ax.axis('off')
        
        png_buffer = io.BytesIO()
        fig.savefig(png_buffer, format='png', bbox_inches='tight', dpi=150)
        png_buffer.seek(0)
        png_data = base64.b64encode(png_buffer.read()).decode('utf-8')
        plt.close(fig)
        
        return png_data
    
    def _empty_graph_svg(self, title: str) -> str:
        """Return empty graph SVG."""
        svg = f'''<svg width="400" height="200" xmlns="http://www.w3.org/2000/svg">
            <text x="200" y="100" text-anchor="middle" font-size="16" fill="#666">{title}</text>
            <text x="200" y="120" text-anchor="middle" font-size="12" fill="#999">No data available</text>
        </svg>'''
        return base64.b64encode(svg.encode('utf-8')).decode('utf-8')
    
    def _empty_graph_png(self, title: str) -> str:
        """Return empty graph PNG."""
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, f"{title}\nNo data available", 
                ha='center', va='center', fontsize=14, color='#666')
        ax.axis('off')
        
        png_buffer = io.BytesIO()
        fig.savefig(png_buffer, format='png', bbox_inches='tight')
        png_buffer.seek(0)
        png_data = base64.b64encode(png_buffer.read()).decode('utf-8')
        plt.close(fig)
        
        return png_data

