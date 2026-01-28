"""
MinerU API Server Example
=========================

Deploy MinerU as a REST API service with FastAPI.

Features:
- Upload PDF via HTTP
- Process with MinerU
- Return markdown content
- Health check endpoint

Installation:
    pip install fastapi uvicorn python-multipart

Usage:
    python api_server.py
    # Or: uvicorn api_server:app --host 0.0.0.0 --port 8000

Test:
    curl http://localhost:8000/health
    curl -X POST http://localhost:8000/parse -F "file=@document.pdf"
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from pathlib import Path
import tempfile
import shutil
from mineru.cli.client import parse_doc
from typing import Optional

app = FastAPI(
    title="MinerU API",
    description="PDF to Markdown conversion service",
    version="1.0.0"
)


@app.get("/")
def root():
    """API root endpoint."""
    return {
        "service": "MinerU API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "mineru-api"
    }


@app.post("/parse")
async def parse_pdf(
    file: UploadFile = File(...),
    backend: str = Form("hybrid-auto-engine"),
    language: str = Form("en")
):
    """
    Parse uploaded PDF and return markdown content.

    Args:
        file: PDF file to parse
        backend: Processing backend (pipeline, hybrid-auto-engine, vlm-auto-engine)
        language: Language code for OCR (en, ch, japan, etc.)

    Returns:
        JSON with markdown content and metadata
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    # Validate backend
    valid_backends = ["pipeline", "hybrid-auto-engine", "vlm-auto-engine"]
    if backend not in valid_backends:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid backend. Choose from: {valid_backends}"
        )

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    # Create output directory
    output_dir = tempfile.mkdtemp()

    try:
        # Process PDF
        parse_doc(
            path_list=[Path(tmp_path)],
            output_dir=output_dir,
            backend=backend,
            lang=language
        )

        # Read markdown output
        pdf_name = Path(tmp_path).stem
        md_file = Path(output_dir) / pdf_name / "auto" / f"{pdf_name}.md"

        if not md_file.exists():
            raise HTTPException(
                status_code=500,
                detail="Processing completed but output file not found"
            )

        with open(md_file, encoding='utf-8') as f:
            markdown_content = f.read()

        # Count extracted images
        images_dir = md_file.parent / "images"
        num_images = len(list(images_dir.glob("*"))) if images_dir.exists() else 0

        return {
            "status": "success",
            "filename": file.filename,
            "backend": backend,
            "language": language,
            "markdown": markdown_content,
            "metadata": {
                "content_length": len(markdown_content),
                "num_images": num_images
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Processing failed: {str(e)}"
        )

    finally:
        # Cleanup
        try:
            Path(tmp_path).unlink()
            shutil.rmtree(output_dir)
        except:
            pass


@app.post("/parse-batch")
async def parse_batch(
    files: list[UploadFile] = File(...),
    backend: str = Form("hybrid-auto-engine"),
    language: str = Form("en")
):
    """
    Parse multiple PDFs in batch.

    Args:
        files: List of PDF files
        backend: Processing backend
        language: Language code

    Returns:
        JSON with results for each file
    """
    results = []

    for file in files:
        try:
            result = await parse_pdf(file, backend, language)
            results.append({
                "filename": file.filename,
                "status": "success",
                "content_length": result["metadata"]["content_length"]
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "status": "error",
                "error": str(e)
            })

    return {
        "total": len(files),
        "results": results
    }


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting MinerU API Server")
    print("📖 Docs: http://localhost:8000/docs")
    print("🏥 Health: http://localhost:8000/health")
    uvicorn.run(app, host="0.0.0.0", port=8000)
