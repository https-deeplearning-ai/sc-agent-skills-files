"""
Backend Comparison Example
==========================

Compare MinerU's three processing backends:
- pipeline: Fast, CPU-friendly
- vlm-auto-engine: High accuracy, GPU required
- hybrid-auto-engine: Balanced (default)

Usage:
    python backend_comparison.py <path-to-pdf>
"""

from pathlib import Path
from mineru.cli.client import parse_doc
import time
import sys


def test_backend(pdf_path: Path, backend: str, output_dir: str):
    """
    Process PDF with specific backend and measure time.

    Args:
        pdf_path: Input PDF
        backend: Backend name
        output_dir: Output directory

    Returns:
        Processing time in seconds
    """
    print(f"\n{'='*50}")
    print(f"Testing: {backend}")
    print(f"{'='*50}")

    start_time = time.time()

    try:
        parse_doc(
            path_list=[pdf_path],
            output_dir=output_dir,
            backend=backend,
            lang="en"
        )
        elapsed = time.time() - start_time
        print(f"✅ Success! Time: {elapsed:.2f}s")
        return elapsed

    except Exception as e:
        print(f"❌ Failed: {e}")
        return None


def compare_backends(pdf_path: str):
    """
    Compare all three backends on the same PDF.

    Args:
        pdf_path: Path to PDF file
    """
    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        print(f"❌ Error: File not found: {pdf_path}")
        return

    print(f"📄 PDF: {pdf_file.name}")

    # Test each backend
    backends = [
        ("pipeline", "output_pipeline"),
        ("hybrid-auto-engine", "output_hybrid"),
        # Uncomment if you have GPU with 10GB+ VRAM:
        # ("vlm-auto-engine", "output_vlm"),
    ]

    results = {}

    for backend, output_dir in backends:
        elapsed = test_backend(pdf_file, backend, output_dir)
        if elapsed:
            results[backend] = elapsed

    # Summary
    if results:
        print(f"\n{'='*50}")
        print("📊 Results Summary")
        print(f"{'='*50}")

        for backend, elapsed in sorted(results.items(), key=lambda x: x[1]):
            print(f"{backend:20s}: {elapsed:6.2f}s")

        fastest = min(results, key=results.get)
        print(f"\n⚡ Fastest: {fastest} ({results[fastest]:.2f}s)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python backend_comparison.py <path-to-pdf>")
        print("Example: python backend_comparison.py sample.pdf")
        sys.exit(1)

    compare_backends(sys.argv[1])
