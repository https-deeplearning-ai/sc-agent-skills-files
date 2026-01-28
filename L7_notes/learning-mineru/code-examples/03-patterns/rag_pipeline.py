"""
RAG System Data Pipeline Example
================================

Prepare document collection for Retrieval-Augmented Generation (RAG) systems.

This example:
1. Processes PDFs with MinerU
2. Chunks the markdown output
3. Creates a JSON dataset for vector database ingestion

Usage:
    python rag_pipeline.py <pdf-folder> [--chunk-size 1000]
"""

from pathlib import Path
from mineru.cli.client import parse_doc
import json
import argparse
from typing import List, Dict


def prepare_rag_dataset(
    pdf_folder: str,
    output_dir: str = "rag_data",
    chunk_size: int = 1000
) -> List[Dict]:
    """
    Process PDFs and prepare for RAG system ingestion.

    Args:
        pdf_folder: Folder with PDF documents
        output_dir: Where to save processed data
        chunk_size: Target size for text chunks (characters)

    Returns:
        List of document chunks with metadata
    """
    pdf_files = list(Path(pdf_folder).glob("*.pdf"))

    if not pdf_files:
        print(f"❌ No PDFs found in {pdf_folder}")
        return []

    print(f"📚 Processing {len(pdf_files)} documents for RAG")
    print(f"📏 Chunk size: {chunk_size} characters\n")

    # Process all PDFs
    parse_doc(
        path_list=pdf_files,
        output_dir=output_dir,
        backend="hybrid-auto-engine",
        lang="en"
    )

    print(f"✅ Processing complete. Creating chunks...\n")

    # Extract and chunk content
    chunks = []
    total_chars = 0

    for pdf_file in pdf_files:
        pdf_name = pdf_file.stem
        md_file = Path(output_dir) / pdf_name / "auto" / f"{pdf_name}.md"

        if not md_file.exists():
            print(f"⚠️  Skipping {pdf_name} (no markdown output)")
            continue

        with open(md_file, encoding='utf-8') as f:
            content = f.read()

        total_chars += len(content)

        # Simple chunking by paragraphs
        paragraphs = content.split('\n\n')
        current_chunk = ""
        chunk_index = 0

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            if len(current_chunk) + len(para) > chunk_size:
                # Save current chunk
                if current_chunk:
                    chunks.append({
                        "id": f"{pdf_name}_chunk_{chunk_index}",
                        "text": current_chunk.strip(),
                        "source": pdf_name,
                        "source_file": str(pdf_file),
                        "chunk_index": chunk_index
                    })
                    chunk_index += 1
                current_chunk = para
            else:
                current_chunk += "\n\n" + para if current_chunk else para

        # Add remaining chunk
        if current_chunk:
            chunks.append({
                "id": f"{pdf_name}_chunk_{chunk_index}",
                "text": current_chunk.strip(),
                "source": pdf_name,
                "source_file": str(pdf_file),
                "chunk_index": chunk_index
            })

    # Save chunked dataset
    output_file = Path(output_dir) / "rag_chunks.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    # Statistics
    print(f"📊 Dataset Statistics:")
    print(f"   Documents: {len(pdf_files)}")
    print(f"   Total characters: {total_chars:,}")
    print(f"   Chunks created: {len(chunks)}")
    print(f"   Avg chunk size: {total_chars // len(chunks) if chunks else 0} chars")
    print(f"\n💾 Saved to: {output_file}")

    return chunks


def preview_chunks(chunks: List[Dict], num_samples: int = 3):
    """
    Show sample chunks from the dataset.

    Args:
        chunks: List of chunk dictionaries
        num_samples: Number of samples to show
    """
    print(f"\n{'='*60}")
    print(f"Sample Chunks (showing {num_samples} of {len(chunks)})")
    print(f"{'='*60}\n")

    for i, chunk in enumerate(chunks[:num_samples], 1):
        print(f"Chunk {i}:")
        print(f"  ID: {chunk['id']}")
        print(f"  Source: {chunk['source']}")
        print(f"  Length: {len(chunk['text'])} chars")
        print(f"  Text preview: {chunk['text'][:150]}...")
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Prepare PDFs for RAG system ingestion"
    )
    parser.add_argument("pdf_folder", help="Folder containing PDF files")
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=1000,
        help="Target chunk size in characters (default: 1000)"
    )
    parser.add_argument(
        "--output-dir",
        default="rag_data",
        help="Output directory (default: rag_data)"
    )

    args = parser.parse_args()

    # Create dataset
    chunks = prepare_rag_dataset(
        args.pdf_folder,
        output_dir=args.output_dir,
        chunk_size=args.chunk_size
    )

    # Show samples
    if chunks:
        preview_chunks(chunks)

        print(f"\n💡 Next steps:")
        print(f"   1. Load rag_chunks.json")
        print(f"   2. Generate embeddings (e.g., with sentence-transformers)")
        print(f"   3. Ingest into vector database (ChromaDB, Pinecone, etc.)")
        print(f"   4. Build RAG query interface")
