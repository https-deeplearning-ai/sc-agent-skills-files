"""
Multilingual PDF Processing Example
===================================

Process documents in different languages with appropriate OCR settings.

Usage:
    python multilingual_processing.py <pdf-path> <language-code>
    python multilingual_processing.py chinese.pdf zh-cn
"""

from pathlib import Path
from mineru.cli.client import parse_doc
import sys


# Language mapping: ISO code -> MinerU language code
LANGUAGE_CODES = {
    "en": "en",
    "zh-cn": "ch",
    "zh-tw": "chinese_cht",
    "ja": "japan",
    "ko": "korean",
    "es": "latin",
    "fr": "latin",
    "de": "latin",
    "pt": "latin",
    "ar": "arabic",
    "ru": "cyrillic",
    "hi": "devanagari",
}


def extract_multilingual_pdf(pdf_path: str, language: str = "en"):
    """
    Extract PDF with language-specific OCR.

    Args:
        pdf_path: Path to PDF
        language: ISO language code (e.g., 'en', 'zh-cn', 'ja')
    """
    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        print(f"❌ Error: File not found: {pdf_path}")
        return

    # Map to MinerU language code
    mineru_lang = LANGUAGE_CODES.get(language.lower(), "en")

    print(f"📄 PDF: {pdf_file.name}")
    print(f"🌍 Language: {language} -> {mineru_lang}")
    print(f"Processing...\n")

    # Process
    parse_doc(
        path_list=[pdf_file],
        output_dir=f"output_{language}",
        backend="hybrid-auto-engine",
        lang=mineru_lang
    )

    # Output location
    output_file = Path(f"output_{language}") / pdf_file.stem / "auto" / f"{pdf_file.stem}.md"

    if output_file.exists():
        print(f"✅ Success!")
        print(f"📄 Output: {output_file}")

        # Show preview
        with open(output_file, encoding='utf-8') as f:
            content = f.read()
            preview = content[:300]
            print(f"\n--- Preview ---")
            print(preview)
            if len(content) > 300:
                print("...")
    else:
        print(f"❌ Error: Output file not found")


def batch_multilingual(pdf_language_pairs: list):
    """
    Process multiple PDFs with different languages.

    Args:
        pdf_language_pairs: List of (pdf_path, language_code) tuples
    """
    print(f"📚 Processing {len(pdf_language_pairs)} documents\n")

    for pdf_path, lang_code in pdf_language_pairs:
        print(f"{'='*60}")
        extract_multilingual_pdf(pdf_path, lang_code)
        print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python multilingual_processing.py <pdf-path> [language-code]")
        print("\nSupported language codes:")
        for iso, mineru in sorted(LANGUAGE_CODES.items()):
            print(f"  {iso:8s} -> {mineru}")
        print("\nExamples:")
        print("  python multilingual_processing.py document.pdf en")
        print("  python multilingual_processing.py 文档.pdf zh-cn")
        print("  python multilingual_processing.py ドキュメント.pdf ja")
        sys.exit(1)

    pdf_path = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else "en"

    extract_multilingual_pdf(pdf_path, language)
