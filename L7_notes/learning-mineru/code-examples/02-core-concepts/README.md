# Core Concepts Examples

Examples demonstrating MinerU's fundamental concepts.

## Files

- `backend_comparison.py` - Compare pipeline, hybrid, and VLM backends
- `multilingual_processing.py` - Process documents in different languages
- `scientific_paper.py` - Extract formulas and tables from research papers

## Usage

### Backend Comparison

Compare processing speed and results across backends:

```bash
python backend_comparison.py sample.pdf
```

**Output**:
```
Testing: pipeline
✅ Success! Time: 12.34s

Testing: hybrid-auto-engine
✅ Success! Time: 15.67s

📊 Results Summary
pipeline            :  12.34s
hybrid-auto-engine  :  15.67s

⚡ Fastest: pipeline (12.34s)
```

**Note**: VLM backend requires GPU with 10GB+ VRAM. Uncomment in the script if you have one.

### Multilingual Processing

Process documents in different languages:

```bash
# English
python multilingual_processing.py document.pdf en

# Chinese
python multilingual_processing.py 文档.pdf zh-cn

# Japanese
python multilingual_processing.py ドキュメント.pdf ja

# Korean
python multilingual_processing.py 문서.pdf ko
```

**Supported languages**: See script for full list (109 languages total)

### Scientific Paper Extraction

Extract formulas and tables from research papers:

```bash
python scientific_paper.py research_paper.pdf
```

**Output**:
```
🔬 Processing scientific paper: research_paper.pdf

📊 Statistics:
   Pages: 12
   Formulas: 47
   Tables: 5

📐 Extracted Formulas:
   Inline: 32
   Block: 15

   Sample block formulas:
   1. E = mc^2
   2. \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
   3. F = G\frac{m_1 m_2}{r^2}

✅ Complete!
```

## Key Concepts Demonstrated

### 1. Multiple Backends
- **pipeline**: Fastest, CPU-friendly, 82+ accuracy
- **hybrid**: Balanced, 90+ accuracy, works on CPU
- **vlm**: Highest accuracy, GPU required

### 2. Multilingual OCR
- 109 languages supported
- Language-specific models improve accuracy
- Easy language code mapping

### 3. Content Recognition
- Formulas converted to LaTeX
- Tables converted to HTML/Markdown
- Images extracted with captions
- Layout preserved

## Tips

**For best results**:
- Use correct language code for your documents
- Enable formulas/tables explicitly for scientific papers
- Use VLM backend for maximum accuracy (if you have GPU)
- Check layout visualization to debug extraction issues

**Performance**:
- Pipeline: ~10-20 seconds per page
- Hybrid: ~15-30 seconds per page
- VLM: ~20-40 seconds per page (GPU-dependent)

## Next Steps

Try `../03-patterns/` for real-world use cases:
- RAG system pipelines
- Batch processing workflows
- API server deployment
