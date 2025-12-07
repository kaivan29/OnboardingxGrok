"""Test script to run analysis on example codebase."""
import asyncio
import json
import os
from pathlib import Path
from services.codebase_analyzer import CodebaseAnalyzer
from services.tutorial_generator import TutorialGenerator
from services.visualization_generator import VisualizationGenerator
from utils.grok_client import GrokClient
from config import Config


async def test_analysis():
    """Test the analysis pipeline on the example codebase."""
    print("=" * 60)
    print("Testing Codebase Analysis Pipeline")
    print("=" * 60)
    
    # Check if API key is set
    if not Config.XAI_API_KEY:
        print("\n⚠️  WARNING: XAI_API_KEY not set in environment.")
        print("   Set it with: export XAI_API_KEY=your_key_here")
        print("   Or create a .env file with XAI_API_KEY=your_key_here")
        print("\n   Continuing with analysis (will skip Grok API calls)...\n")
        use_grok = False
    else:
        use_grok = True
        print(f"✓ Using Grok API with model: {Config.XAI_MODEL}\n")
    
    # Get the test example directory
    test_dir = Path(__file__).parent / "test_example"
    
    if not test_dir.exists():
        print(f"❌ Test directory not found: {test_dir}")
        return
    
    print(f"📁 Analyzing codebase: {test_dir}")
    print("-" * 60)
    
    try:
        # Step 1: Analyze codebase structure
        print("\n1️⃣  Analyzing codebase structure...")
        analyzer = CodebaseAnalyzer(max_file_size=100000)
        analysis_result = await analyzer.analyze(
            local_path=str(test_dir),
            include_patterns=["*.py"],
            exclude_patterns=[]
        )
        
        print(f"   ✓ Found {len(analysis_result['files'])} files")
        print(f"   ✓ Parsed {len(analysis_result['structure']['modules'])} modules")
        print(f"   ✓ Found {len(analysis_result['structure']['classes'])} classes")
        print(f"   ✓ Found {len(analysis_result['structure']['functions'])} functions")
        
        # Step 2: Generate visualizations (doesn't require API)
        print("\n2️⃣  Generating visualizations...")
        viz_generator = VisualizationGenerator()
        
        dependency_viz = viz_generator.generate_dependency_graph(
            dependencies=analysis_result["dependencies"],
            format="svg"
        )
        print(f"   ✓ Generated dependency graph ({len(dependency_viz.data)} bytes)")
        
        # Build knowledge graph (doesn't require API)
        # Create a dummy client just for the method call
        class DummyClient:
            pass
        tutorial_gen = TutorialGenerator(DummyClient())
        knowledge_graph = tutorial_gen.build_knowledge_graph(
            structure=analysis_result["structure"],
            dependencies=analysis_result["dependencies"]
        )
        
        knowledge_viz = viz_generator.generate_knowledge_graph_visualization(
            knowledge_graph=knowledge_graph,
            format="svg"
        )
        print(f"   ✓ Generated knowledge graph ({len(knowledge_viz.data)} bytes)")
        
        structure_viz = viz_generator.generate_structure_tree(
            structure=analysis_result["structure"],
            format="svg"
        )
        print(f"   ✓ Generated structure tree ({len(structure_viz.data)} bytes)")
        
        # Step 3: Generate tutorial content with Grok API
        if use_grok:
            print("\n3️⃣  Generating tutorial content with Grok API...")
            grok_client = GrokClient()
            tutorial_generator = TutorialGenerator(grok_client)
            
            try:
                summary = await tutorial_generator.generate_summary(
                    codebase_summary=analysis_result["summary"],
                    file_contents=analysis_result["file_contents"]
                )
                print(f"   ✓ Generated summary ({len(summary)} characters)")
                print(f"\n   Summary Preview:")
                print(f"   {summary[:200]}...")
                
                abstractions = await tutorial_generator.identify_abstractions(
                    codebase_summary=analysis_result["summary"],
                    file_contents=analysis_result["file_contents"],
                    max_abstractions=5
                )
                print(f"   ✓ Identified {len(abstractions)} abstractions")
                for abs in abstractions:
                    print(f"      - {abs.name} ({abs.pattern_type})")
                
                chapters = await tutorial_generator.generate_chapters(
                    codebase_summary=analysis_result["summary"],
                    file_contents=analysis_result["file_contents"],
                    structure=analysis_result["structure"]
                )
                print(f"   ✓ Generated {len(chapters)} chapters")
                for chapter in chapters:
                    print(f"      - {chapter.title} ({len(chapter.files)} files)")
                
                await grok_client.close()
                
            except Exception as e:
                print(f"   ❌ Error calling Grok API: {e}")
                print("   Continuing with structure analysis only...")
        else:
            print("\n3️⃣  Skipping Grok API calls (no API key)")
            summary = analysis_result["summary"]
            abstractions = []
            chapters = []
        
        # Step 4: Display results
        print("\n" + "=" * 60)
        print("📊 ANALYSIS RESULTS")
        print("=" * 60)
        
        print(f"\n📝 Summary:")
        print(f"{summary[:500]}...")
        
        print(f"\n📚 Structure Summary:")
        print(analysis_result["summary"])
        
        print(f"\n🔗 Knowledge Graph:")
        print(f"   Nodes: {len(knowledge_graph.nodes)}")
        print(f"   Edges: {len(knowledge_graph.edges)}")
        
        print(f"\n📊 Visualizations Generated:")
        print(f"   - Dependency Graph: {len(dependency_viz.data)} bytes (SVG)")
        print(f"   - Knowledge Graph: {len(knowledge_viz.data)} bytes (SVG)")
        print(f"   - Structure Tree: {len(structure_viz.data)} bytes (SVG)")
        
        # Save visualizations to files
        output_dir = Path(__file__).parent / "test_output"
        output_dir.mkdir(exist_ok=True)
        
        import base64
        for viz_name, viz in [
            ("dependency_graph", dependency_viz),
            ("knowledge_graph", knowledge_viz),
            ("structure_tree", structure_viz)
        ]:
            svg_data = base64.b64decode(viz.data)
            output_file = output_dir / f"{viz_name}.svg"
            with open(output_file, "wb") as f:
                f.write(svg_data)
            print(f"   ✓ Saved {viz_name}.svg to {output_file}")
        
        # Save JSON results
        results = {
            "summary": summary,
            "structure_summary": analysis_result["summary"],
            "files_analyzed": len(analysis_result["files"]),
            "knowledge_graph": {
                "nodes": len(knowledge_graph.nodes),
                "edges": len(knowledge_graph.edges)
            },
            "abstractions": [{"name": a.name, "type": a.pattern_type, "description": a.description, "files": a.files} for a in abstractions],
            "chapters": [{"title": c.title, "content": c.content, "files": c.files, "order": c.order, "sections": c.sections} for c in chapters]
        }
        
        results_file = output_dir / "analysis_results.json"
        with open(results_file, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\n✓ Saved analysis results to {results_file}")
        
        # Generate markdown files
        print("\n4️⃣  Generating markdown documentation...")
        from utils.markdown_generator import MarkdownGenerator
        from datetime import datetime
        
        md_generator = MarkdownGenerator(output_dir)
        
        # Prepare metadata
        metadata = {
            "files_analyzed": len(analysis_result["files"]),
            "model_used": Config.XAI_MODEL if use_grok else "N/A",
            "root_path": analysis_result.get("root_path", ""),
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Generate main output.md
        output_md = md_generator.generate_output_md(
            summary=summary,
            structure_summary=analysis_result["summary"],
            abstractions=abstractions,
            knowledge_graph=knowledge_graph,
            visualizations={
                "dependency_graph": dependency_viz,
                "knowledge_graph": knowledge_viz,
                "structure_tree": structure_viz
            },
            metadata=metadata
        )
        print(f"   ✓ Generated {output_md.name}")
        
        # Generate chapter markdown files
        for i, chapter in enumerate(chapters, 1):
            chapter_md = md_generator.generate_chapter_md(chapter, i)
            print(f"   ✓ Generated {chapter_md.name}")
        
        print("\n" + "=" * 60)
        print("✅ Analysis complete!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_analysis())

