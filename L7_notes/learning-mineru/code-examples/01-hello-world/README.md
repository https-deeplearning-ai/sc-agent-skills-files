# Hello World Examples

Your first steps with MinerU.

## Files

- `simple_extraction.py` - Extract a single PDF to markdown
- `batch_processing.py` - Process multiple PDFs at once

## Quick Start

### 1. Simple Extraction

```bash
# Extract a PDF
python simple_extraction.py your-document.pdf

# View the output
cat output/your-document/auto/your-document.md
```

**What it does**:
- Takes a PDF file path
- Extracts text, images, tables, formulas
- Saves as markdown in `output/` folder
- Shows preview of extracted content

### 2. Batch Processing

```bash
# Process all PDFs in a folder
python batch_processing.py /path/to/pdf-folder

# Or current directory
python batch_processing.py .
```

**What it does**:
- Finds all `.pdf` files in the folder
- Processes each one
- Shows progress bar
- Saves all outputs to `batch_output/`

## Expected Output

After running `simple_extraction.py sample.pdf`:

```
output/
└── sample/
    └── auto/
        ├── sample.md           # Markdown version
        ├── middle.json         # Intermediate data
        ├── layout.png          # Layout visualization (optional)
        └── images/             # Extracted images
            ├── image1.png
            └── image2.png
```

## Troubleshooting

**Problem**: `ModuleNotFoundError: No module named 'mineru'`
```bash
# Solution: Install MinerU
pip install uv
uv pip install -U "mineru[all]"
```

**Problem**: `FileNotFoundError`
```bash
# Solution: Check PDF path is correct
ls your-document.pdf  # Verify file exists
```

**Problem**: Out of memory
```bash
# Solution: Use pipeline backend (faster, less memory)
# Edit the script: backend="pipeline"
```

## Next Steps

- Try different PDFs (simple text, complex layouts, scanned)
- Experiment with language settings (change `lang="en"` to other codes)
- Check `../02-core-concepts/` for more advanced examples
