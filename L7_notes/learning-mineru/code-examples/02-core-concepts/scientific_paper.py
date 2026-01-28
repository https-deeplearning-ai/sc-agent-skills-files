"""
Scientific Paper Processing Example
===================================

Extract formulas and tables from research papers.

Usage:
    python scientific_paper.py <path-to-paper>
"""

from pathlib import Path
from mineru.cli.client import do_parse
import json
import re
import sys


def extract_scientific_paper(pdf_path: str, output_dir: str = "papers_output"):
    """
    Extract scientific paper with formula and table recognition.

    Args:
        pdf_path: Path to research paper PDF
        output_dir: Output directory
    """
    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        print(f"❌ Error: File not found: {pdf_path}")
        return

    print(f"🔬 Processing scientific paper: {pdf_file.name}\n")

    # Process with all features enabled
    do_parse(
        pdf_path=str(pdf_file),
        output_dir=output_dir,
        backend="hybrid-auto-engine",  # or "vlm-auto-engine" for highest accuracy
        lang="en",
        formula_enable=True,  # Enable formula recognition
        table_enable=True,    # Enable table recognition
        f_dump_md=True,       # Generate markdown
        f_dump_middle_json=True,  # Generate intermediate JSON
        f_draw_layout_bbox=True   # Generate layout visualization
    )

    # Output paths
    pdf_name = pdf_file.stem
    output_path = Path(output_dir) / pdf_name / "auto"
    markdown_file = output_path / f"{pdf_name}.md"
    middle_json = output_path / "middle.json"
    layout_viz = output_path / "layout.png"

    # Extract statistics
    if middle_json.exists():
        with open(middle_json, encoding='utf-8') as f:
            data = json.load(f)

        # Count elements
        num_pages = len(data.get("pages", []))
        formulas = []
        tables = []

        for page in data.get("pages", []):
            for elem in page.get("elements", []):
                if elem.get("type") == "formula":
                    formulas.append(elem)
                elif elem.get("type") == "table":
                    tables.append(elem)

        print(f"📊 Statistics:")
        print(f"   Pages: {num_pages}")
        print(f"   Formulas: {len(formulas)}")
        print(f"   Tables: {len(tables)}")

    # Extract formulas from markdown
    if markdown_file.exists():
        with open(markdown_file, encoding='utf-8') as f:
            content = f.read()

        # Extract inline formulas: $...$
        inline_formulas = re.findall(r'\$([^\$]+)\$', content)

        # Extract block formulas: $$...$$
        block_formulas = re.findall(r'\$\$([^\$]+)\$\$', content, re.DOTALL)

        print(f"\n📐 Extracted Formulas:")
        print(f"   Inline: {len(inline_formulas)}")
        print(f"   Block: {len(block_formulas)}")

        # Show first few block formulas
        if block_formulas:
            print(f"\n   Sample block formulas:")
            for i, formula in enumerate(block_formulas[:3], 1):
                print(f"   {i}. {formula.strip()[:80]}...")

    # Results
    print(f"\n✅ Complete!")
    print(f"📄 Markdown: {markdown_file}")
    print(f"📊 Data: {middle_json}")
    print(f"🖼️  Layout: {layout_viz}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scientific_paper.py <path-to-paper>")
        print("Example: python scientific_paper.py quantum_physics.pdf")
        sys.exit(1)

    extract_scientific_paper(sys.argv[1])
