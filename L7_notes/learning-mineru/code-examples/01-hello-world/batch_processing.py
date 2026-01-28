"""
Batch PDF Processing Example
============================

Process multiple PDFs in a folder at once.

Usage:
    python batch_processing.py <folder-path>
    python batch_processing.py .  # Current directory
"""

from pathlib import Path
from mineru.cli.client import parse_doc
from tqdm import tqdm
import sys


def batch_extract_pdfs(input_folder: str, output_dir: str = "batch_output"):
    """
    Process all PDFs in a folder.

    Args:
        input_folder: Folder containing PDFs
        output_dir: Where to save results
    """
    # Find all PDFs
    input_path = Path(input_folder)
    pdf_files = list(input_path.glob("*.pdf"))

    if not pdf_files:
        print(f"❌ No PDFs found in {input_folder}")
        return

    print(f"📚 Found {len(pdf_files)} PDFs to process")
    print(f"📁 Output directory: {output_dir}\n")

    # Process with progress bar
    successful = 0
    failed = 0

    for pdf_file in tqdm(pdf_files, desc="Processing PDFs"):
        try:
            parse_doc(
                path_list=[pdf_file],
                output_dir=output_dir,
                backend="hybrid-auto-engine",
                lang="en"
            )
            successful += 1
            tqdm.write(f"✅ {pdf_file.name}")
        except Exception as e:
            failed += 1
            tqdm.write(f"❌ {pdf_file.name}: {e}")

    # Summary
    print(f"\n{'='*50}")
    print(f"📊 Processing Summary")
    print(f"{'='*50}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📁 Results in: {output_dir}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python batch_processing.py <folder-path>")
        print("Example: python batch_processing.py ./my-pdfs")
        sys.exit(1)

    folder_path = sys.argv[1]

    if not Path(folder_path).exists():
        print(f"❌ Error: Folder not found: {folder_path}")
        sys.exit(1)

    batch_extract_pdfs(folder_path)
