"""
Simple PDF Extraction Example
=============================

This is your first MinerU script. It extracts content from a PDF
and saves it as markdown.

Requirements:
    pip install "mineru[all]"

Usage:
    python simple_extraction.py <path-to-pdf>
"""

from pathlib import Path
from mineru.cli.client import parse_doc
import sys


def extract_pdf(pdf_path: str, output_dir: str = "output"):
    """
    Extract content from a PDF into markdown format.

    Args:
        pdf_path: Path to input PDF
        output_dir: Where to save results (default: "output")

    Returns:
        Path to the generated markdown file
    """
    print(f"📄 Processing: {pdf_path}")

    # Convert to Path object
    pdf_file = Path(pdf_path)

    # Validate file exists
    if not pdf_file.exists():
        print(f"❌ Error: File not found: {pdf_path}")
        return None

    # Validate it's a PDF
    if pdf_file.suffix.lower() != '.pdf':
        print(f"❌ Error: Not a PDF file: {pdf_path}")
        return None

    # Parse the document
    parse_doc(
        path_list=[pdf_file],
        output_dir=output_dir,
        backend="hybrid-auto-engine",  # Best balance of speed and accuracy
        lang="en"  # Change to "ch" for Chinese, "japan" for Japanese, etc.
    )

    # Find the output markdown file
    pdf_name = pdf_file.stem
    markdown_file = Path(output_dir) / pdf_name / "auto" / f"{pdf_name}.md"

    if markdown_file.exists():
        print(f"✅ Extraction complete!")
        print(f"📄 Markdown: {markdown_file}")
        print(f"🖼️  Images: {markdown_file.parent / 'images'}")
        return markdown_file
    else:
        print(f"❌ Error: Output file not found at {markdown_file}")
        return None


if __name__ == "__main__":
    # Check command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python simple_extraction.py <path-to-pdf>")
        print("Example: python simple_extraction.py sample.pdf")
        sys.exit(1)

    # Get PDF path from command line
    pdf_path = sys.argv[1]

    # Extract the PDF
    result = extract_pdf(pdf_path)

    # Optional: Print first 500 characters of the output
    if result:
        print("\n--- Preview of extracted content ---")
        with open(result) as f:
            content = f.read()
            print(content[:500])
            if len(content) > 500:
                print("...\n(showing first 500 characters)")
