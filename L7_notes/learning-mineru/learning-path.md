# MinerU Learning Path

A progressive guide to mastering MinerU - from understanding its purpose to building production-ready document processing pipelines.

---

## Level 1: Overview & Motivation

### What Problem Does MinerU Solve?

**The Core Problem**: Traditional PDF extraction produces semantically incoherent text that's unsuitable for Large Language Model (LLM) training and processing.

When you extract text from a typical PDF with standard tools, you get:
- Text in the wrong order (columns mixed up, headers scattered)
- Mathematical formulas as gibberish or question marks
- Tables as unstructured text soup
- Headers, footers, and page numbers mixed into content
- Images with no metadata or context

**MinerU transforms this chaos into clean, structured, LLM-ready data.**

### Origin Story

MinerU was born during the pre-training process of **InternLM** (a large language model). The team needed to extract high-quality training data from scientific papers, which are notoriously difficult:
- Complex multi-column layouts
- Mathematical formulas with special symbols
- Tables with intricate structures
- Figures with captions
- Mixed languages

Existing tools failed to preserve semantic coherence and reading order. So they built MinerU.

### What Existed Before?

**Traditional PDF Extractors**:
- **pdfminer.six**: Gets raw text but no structure, wrong order
- **PyPDF2**: Basic extraction, struggles with complex layouts
- **Tesseract OCR**: Good for scanned docs but no layout understanding
- **Commercial tools** (Mathpix, Adobe): Expensive, closed-source, limited API access

**Problems**:
- No understanding of document structure
- Can't handle scientific notation
- Mixed reading order in multi-column layouts
- Poor table extraction
- No formula recognition

### Why is MinerU Better?

1. **Layout Understanding**: Recognizes document structure (headings, paragraphs, lists, tables)
2. **Reading Order Preservation**: Outputs text in human reading order
3. **Formula Recognition**: Converts mathematical formulas to LaTeX
4. **Table Extraction**: Transforms tables into HTML format
5. **Multilingual OCR**: Supports 109 languages
6. **Multiple Backends**: Choose speed vs accuracy tradeoffs
7. **Open Source**: Free, customizable, community-driven
8. **LLM-Ready Output**: Markdown and JSON formats optimized for AI

### Who Uses MinerU?

**Researchers & Academics**:
- Extracting training data from scientific papers
- Mining research literature
- Building academic knowledge bases

**AI/ML Developers**:
- Preparing corpora for LLM training
- Building RAG (Retrieval-Augmented Generation) systems
- Creating custom datasets

**Enterprise & Business**:
- Processing legal documents
- Extracting financial reports
- Converting technical documentation
- Building searchable knowledge bases

**Data Scientists**:
- Document intelligence systems
- Information extraction pipelines
- Multi-language document processing

### For What Use Cases?

✅ **Perfect for**:
- Scientific papers with formulas and tables
- Multi-column layouts (journals, magazines)
- Technical documentation
- Business reports with structured data
- Scanned documents (with OCR)
- Mixed-language documents
- Documents for LLM training/RAG systems

❌ **NOT recommended for**:
- Comic books and art albums
- Vertical text (not supported)
- Handwritten notes (poor accuracy)
- Primary school textbooks/exercises
- Documents requiring code block extraction
- Real-time processing (relatively slow)
- Simple text-only PDFs (overkill)

### When Should You NOT Use MinerU?

**Use simpler tools if**:
- You have simple, single-column text PDFs → Use `pdftotext` or `PyPDF2`
- You need instant processing → Use lightweight extractors
- You're on low-resource hardware → MinerU needs 16GB+ RAM
- You need code block extraction → Not yet supported
- Document has vertical text → Not supported

**Consider alternatives if**:
- You need commercial support → Use Adobe, Mathpix
- You want faster processing → Try Marker (but GPL license)
- You need better image handling → Marker excels here
- Budget allows paid APIs → Doc2X, Mathpix offer convenience

### Key Takeaway

**MinerU is your go-to tool when document structure and semantic coherence matter more than raw speed.** If you're building AI systems that need to understand documents (not just extract text), MinerU is likely your best open-source choice.

---

## Level 2: Installation & Hello World

### Prerequisites

**Hardware Requirements**:
- **RAM**: 16GB minimum, 32GB+ recommended
- **Disk Space**: 20GB+ (SSD preferred)
- **GPU** (optional): 10GB+ VRAM for VLM backends (CUDA, MPS, or NPU)

**Software Requirements**:
- **Python**: 3.10 - 3.13
  - ⚠️ Windows only supports 3.10-3.12 (Ray dependency limitation)
- **Operating Systems**:
  - Linux: 2019+ distributions
  - Windows: Python 3.10-3.12 only
  - macOS: 14.0 or later

### Installation Steps

#### Method 1: pip/uv (Recommended)

```bash
# Upgrade pip first
pip install --upgrade pip

# Install uv (modern fast Python package installer)
pip install uv

# Install MinerU with all dependencies
uv pip install -U "mineru[all]"
```

**What does this install?**
- MinerU core library
- All backend dependencies (pipeline, VLM, hybrid)
- OCR models and dependencies
- FastAPI and Gradio interfaces

#### Method 2: From Source (For Contributors)

```bash
# Clone the repository
git clone https://github.com/opendatalab/MinerU.git
cd MinerU

# Install in editable mode
uv pip install -e .[all]
```

#### Method 3: Docker (For Environment Isolation)

```bash
# Pull the official Docker image
docker pull opendatalab/mineru:latest

# Run container with GPU support
docker run --gpus all -v $(pwd)/data:/app/data opendatalab/mineru:latest
```

**When to use Docker?**
- Environment compatibility issues
- Multiple Python versions on your system
- Production deployment
- Avoiding dependency conflicts

### Verification

After installation, verify MinerU is working:

```bash
# Check version
mineru --version

# Should output: MinerU version 2.7.1 (or latest)
```

### Hello World: Your First PDF Extraction

Let's extract content from a PDF and see MinerU in action.

#### Step 1: Prepare a Sample PDF

Create a simple test PDF or use one from the demo folder:

```bash
# Download a sample PDF
curl -O https://raw.githubusercontent.com/opendatalab/MinerU/master/demo/pdfs/demo1.pdf
```

Or use any PDF you have available.

#### Step 2: Basic Command-Line Extraction

```bash
# Extract PDF to output folder
mineru -p demo1.pdf -o output

# For CPU-only systems (no GPU)
mineru -p demo1.pdf -o output -b pipeline
```

**What happens?**
1. MinerU analyzes the PDF layout
2. Detects if OCR is needed
3. Extracts text, formulas, tables, and images
4. Generates output in multiple formats

#### Step 3: Examine the Output

```bash
# Navigate to output folder
cd output

# List files
ls -la
```

**You should see**:
```
demo1/
├── auto/
│   ├── demo1.md              # Markdown version
│   ├── middle.json           # Intermediate format
│   ├── layout.png            # Layout visualization
│   └── images/               # Extracted images
```

#### Step 4: View the Markdown

```bash
# View the extracted markdown
cat demo1/auto/demo1.md
```

**Expected output**: Clean, structured markdown with:
- Proper heading hierarchy
- Paragraphs in reading order
- Tables in HTML format
- Formulas in LaTeX notation
- Image references

### Hello World: Python API

Create a file `hello_mineru.py`:

```python
from pathlib import Path
from mineru.cli.client import parse_doc

# Input PDF path
pdf_path = Path("demo1.pdf")

# Output directory
output_dir = Path("output")

# Parse the document
parse_doc(
    path_list=[pdf_path],
    output_dir=output_dir,
    backend="hybrid-auto-engine",  # Default: best balance
    lang="en"                       # Language for OCR
)

print(f"✅ Extraction complete! Check {output_dir}")
```

Run it:

```bash
python hello_mineru.py
```

**What this does**:
1. Imports the main parsing function
2. Specifies input PDF and output directory
3. Uses hybrid backend (best accuracy/speed balance)
4. Sets language to English for OCR
5. Generates all output formats

### Troubleshooting

**Problem**: `ImportError: libGL.so.1: cannot open shared object file`
```bash
# Solution (Ubuntu/Debian)
sudo apt-get install libgl1-mesa-glx
```

**Problem**: Missing CJK (Chinese/Japanese/Korean) fonts on Linux
```bash
# Solution: Install Noto fonts
sudo apt install fonts-noto-core fonts-noto-cjk
fc-cache -fv
```

**Problem**: Out of memory errors
```bash
# Solution: Use pipeline backend (lower memory)
mineru -p input.pdf -o output -b pipeline
```

**Problem**: Slow processing
- Use GPU if available (automatically detected)
- Reduce resolution in config for faster processing
- Consider using pipeline backend for speed

### Success Criteria

✅ You're ready to move on if:
- MinerU installed without errors
- Verification command shows version
- Sample PDF extracted successfully
- Output folder contains markdown and JSON
- Python API script runs without errors

### Next Step Preview

In Level 3, we'll explore MinerU's core concepts:
- Processing backends (pipeline, VLM, hybrid)
- Layout understanding and reading order
- Intelligent content recognition
- Multilingual OCR
- Flexible deployment architecture

---

## Level 3: Core Concepts

Now that MinerU is running, let's understand the fundamental concepts that make it powerful.

### Concept 1: Multiple Processing Backends

MinerU offers **three distinct backends**, each with different accuracy/speed tradeoffs.

#### Pipeline Backend

**How it works**: Traditional model-based processing with explicit stages:
1. Layout detection (YOLO-based)
2. OCR for text extraction
3. Formula recognition (MFR)
4. Table structure parsing
5. Reading order determination

**Characteristics**:
- ⚡ **Fast**: Optimized for speed
- 📊 **Accuracy**: 82+ on OmniDocBench
- 💾 **Resource-friendly**: Lower memory usage
- 🎯 **No hallucinations**: Rule-based, deterministic

**Best for**:
- CPU-only systems
- Batch processing many documents
- When speed matters more than perfection
- Simple to moderately complex layouts

**Example**:
```python
from pathlib import Path
from mineru.cli.client import parse_doc

parse_doc(
    path_list=[Path("document.pdf")],
    output_dir="output",
    backend="pipeline",  # Use pipeline backend
    lang="en"
)
```

#### VLM Backend

**How it works**: Uses **MinerU2.5-2509-1.2B** vision-language model with two-stage inference:
1. Global layout understanding (structure, regions)
2. Fine-grained content recognition (text, formulas, tables)

**Characteristics**:
- 🎯 **High accuracy**: 90+ on benchmarks
- 🧠 **Context-aware**: Understands document semantics
- 💪 **Handles complexity**: Best for intricate layouts
- 🔥 **GPU required**: 10GB+ VRAM needed

**Best for**:
- Maximum accuracy requirements
- Complex scientific papers
- Documents with unusual layouts
- GPU-equipped systems

**Example**:
```python
parse_doc(
    path_list=[Path("complex_paper.pdf")],
    output_dir="output",
    backend="vlm-auto-engine",  # Use VLM backend locally
    lang="en"
)
```

#### Hybrid Backend (Default in v2.7+)

**How it works**: Combines advantages of both approaches:
- Direct text extraction for text PDFs
- VLM for complex elements (formulas, tables)
- Multi-language OCR (109 languages)
- Optional inline formula recognition

**Characteristics**:
- ⚖️ **Balanced**: Best of both worlds
- 🎯 **Accuracy**: 90+ on benchmarks
- 🔄 **Adaptive**: Chooses right tool for each element
- 🚀 **Default choice**: Recommended for most users

**Best for**:
- General-purpose document processing
- Unknown document types
- Production systems
- When you want "just works" experience

**Example**:
```python
parse_doc(
    path_list=[Path("mixed_document.pdf")],
    output_dir="output",
    backend="hybrid-auto-engine",  # Default: recommended
    lang="en"
)
```

#### Backend Selection Decision Tree

```
Do you have a GPU with 10GB+ VRAM?
├─ Yes → Use "vlm-auto-engine" (highest accuracy)
└─ No
   ├─ Do you need maximum speed?
   │  └─ Yes → Use "pipeline" (fastest)
   └─ Do you want best overall results?
      └─ Yes → Use "hybrid-auto-engine" (default, balanced)
```

**Common Mistake**: Using VLM backend without enough VRAM
```python
# ❌ This will fail on CPU or low-VRAM GPU
parse_doc(..., backend="vlm-auto-engine")  # Requires 10GB+ VRAM

# ✅ Use hybrid instead
parse_doc(..., backend="hybrid-auto-engine")  # Works on CPU
```

---

### Concept 2: Layout Understanding and Reading Order Preservation

MinerU doesn't just extract text—it **understands document structure**.

#### What is Layout Understanding?

**Layout detection** identifies:
- Document regions (text blocks, images, tables, formulas)
- Hierarchical structure (headings, subheadings, paragraphs)
- Reading flow (column order, page flow)
- Semantic elements (captions, footnotes, headers/footers)

**Example**: Multi-column journal paper

```
┌─────────────────────────────┐
│  Title: Neural Networks     │
│  Author: Jane Doe          │
├──────────────┬──────────────┤
│  Column 1    │  Column 2    │
│  Text flows  │  Text flows  │
│  top to      │  top to      │
│  bottom      │  bottom      │
│              │              │
│  [Figure 1]  │  [Table 1]   │
│  Caption     │  Caption     │
└──────────────┴──────────────┘
```

**Traditional extractors produce**:
```
Title: Neural Networks Column 1 Column 2 Author: Jane Doe Text flows Text flows
top to top to [Figure 1] bottom bottom Caption [Table 1] Caption
```
❌ Completely garbled!

**MinerU produces**:
```markdown
# Neural Networks

**Author**: Jane Doe

Text flows top to bottom [Column 1 content]

Text flows top to bottom [Column 2 content]

![Figure 1](images/figure1.png)
*Figure 1: Caption*

| Table 1 |
|---------|
| Data    |
*Table 1: Caption*
```
✅ Perfect reading order!

#### How Reading Order Works

1. **Layout detection** identifies all elements
2. **Region classification** labels each (text/image/table/formula)
3. **Reading order determination** sorts elements:
   - Top-to-bottom within columns
   - Left-to-right for columns
   - Proper handling of spans and floats

4. **Noise removal** filters out:
   - Headers and footers
   - Page numbers
   - Decorative elements
   - Watermarks

**Example**: Preserve structure

```python
from pathlib import Path
from mineru.cli.client import parse_doc

# Parse with structure preservation
parse_doc(
    path_list=[Path("journal.pdf")],
    output_dir="output",
    backend="hybrid-auto-engine"
)

# Result maintains semantic coherence
# - Headings marked with #, ##, ###
# - Lists properly formatted
# - Paragraphs in logical order
# - Tables and images inline at correct positions
```

**Common Mistake**: Expecting perfect order for extremely complex layouts
```python
# ❌ Very complex layouts may still have minor ordering issues
# Documents with:
# - Irregular grids
# - Text wrapping around multiple images
# - Rotated text boxes
# - Overlapping elements

# ✅ Best practice: Review output for critical documents
# Use layout visualization to verify
```

#### Verify Layout Detection

Generate layout visualization to see what MinerU detected:

```python
from mineru.cli.client import do_parse

do_parse(
    pdf_path="document.pdf",
    output_dir="output",
    f_draw_layout_bbox=True  # Enable layout visualization
)

# Check output/document/auto/layout.png
# Shows bounding boxes for detected elements
```

**Use cases**:
- Debugging extraction issues
- Understanding model behavior
- Quality assurance for critical documents

---

### Concept 3: Intelligent Content Recognition

MinerU recognizes and converts different content types intelligently.

#### Formula Recognition

**Problem**: Mathematical formulas in PDFs are either:
- Embedded as images (unextractable)
- Encoded with special fonts (garbled text)

**Solution**: MinerU converts formulas to **LaTeX notation**.

**Example**:

PDF shows: E = mc²

MinerU extracts:
```markdown
$E = mc^2$
```

For block formulas:
```markdown
$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$
```

**Code example**:
```python
from mineru.cli.client import do_parse

do_parse(
    pdf_path="scientific_paper.pdf",
    output_dir="output",
    formula_enable=True  # Enable formula recognition
)

# Output markdown will contain LaTeX formulas
# Can be rendered in Markdown viewers, Jupyter, LaTeX
```

**Common Mistake**: Expecting perfect handwritten formula recognition
```python
# ❌ Handwritten formulas have poor accuracy
# MinerU is optimized for typeset formulas

# ✅ Best for:
# - Journal articles (LaTeX-generated)
# - Textbooks (professional typesetting)
# - Technical reports
```

#### Table Conversion

**Problem**: Tables in PDFs lose structure when extracted as plain text.

**Solution**: MinerU converts tables to **HTML format** (structured).

**Example**:

PDF table:
```
┌──────────┬──────────┐
│  Name    │  Score   │
├──────────┼──────────┤
│  Alice   │  95      │
│  Bob     │  87      │
└──────────┴──────────┘
```

MinerU extracts:
```html
<table>
  <thead>
    <tr><th>Name</th><th>Score</th></tr>
  </thead>
  <tbody>
    <tr><td>Alice</td><td>95</td></tr>
    <tr><td>Bob</td><td>87</td></tr>
  </tbody>
</table>
```

In markdown:
```markdown
| Name  | Score |
|-------|-------|
| Alice | 95    |
| Bob   | 87    |
```

**Code example**:
```python
from mineru.cli.client import do_parse

do_parse(
    pdf_path="report.pdf",
    output_dir="output",
    table_enable=True  # Enable table recognition
)
```

**Complex tables**: MinerU handles:
- Merged cells (spanning rows/columns)
- Nested headers
- Multi-line cells
- Tables spanning pages

**Known limitation**: Very complex tables may have row/column errors.

#### Image Extraction

**What MinerU does**:
- Extracts images from PDFs
- Saves with unique filenames
- Preserves metadata (captions)
- Links images in markdown

**Example**:
```markdown
![Figure 1: Neural network architecture](images/abc123.png)

*Figure 1: Neural network architecture showing input, hidden, and output layers.*
```

**Code example**:
```python
# Images extracted automatically
parse_doc(
    path_list=[Path("paper.pdf")],
    output_dir="output"
)

# Check output/paper/auto/images/ folder
# All images saved with MD5 hashes as filenames
```

#### Automatic OCR Detection

**Problem**: Some PDFs contain scanned images (no text layer).

**Solution**: MinerU automatically detects and enables OCR.

**How it works**:
1. Analyzes if PDF has extractable text
2. If not (scanned PDF), activates OCR
3. If garbled text detected, switches to OCR mode

**Example**:
```python
parse_doc(
    path_list=[Path("scanned_document.pdf")],
    output_dir="output",
    method="auto"  # Auto-detect if OCR needed (default)
)

# Alternatives:
# method="txt"  → Force text extraction (faster, no OCR)
# method="ocr"  → Force OCR (even if text exists)
```

**Common Mistake**: Not specifying language for OCR
```python
# ❌ May produce poor results for non-English
parse_doc(..., lang="en")  # Wrong for Chinese document

# ✅ Specify correct language
parse_doc(..., lang="ch")  # Correct for Chinese
```

---

### Concept 4: Multilingual OCR Support

MinerU supports **109 languages** for OCR processing.

#### Supported Language Groups

- **Latin script**: English, Spanish, French, German, Portuguese, etc.
- **CJK**: Chinese, Japanese, Korean
- **Cyrillic**: Russian, Ukrainian, Bulgarian
- **Devanagari**: Hindi, Marathi, Nepali
- **Arabic script**: Arabic, Urdu, Persian
- **Other**: Thai, Tamil, Telugu, Kannada, Greek, and more

#### Language Codes

Common codes:
- `en` - English
- `ch` - Chinese (Simplified)
- `ch_server` - Chinese (Server model, higher accuracy)
- `chinese_cht` - Chinese (Traditional)
- `korean` - Korean
- `japan` - Japanese
- `latin` - Latin-based scripts (general)
- `arabic` - Arabic
- `cyrillic` - Cyrillic scripts
- `devanagari` - Hindi and related scripts

#### Using Languages

**Single language**:
```python
parse_doc(
    path_list=[Path("chinese_doc.pdf")],
    output_dir="output",
    lang="ch"  # Specify language
)
```

**Auto-detection** (for mixed languages):
```python
parse_doc(
    path_list=[Path("multilang_doc.pdf")],
    output_dir="output",
    lang="ch"  # Primary language, auto-detects others
)
```

**Multiple documents with different languages**:
```python
documents = [
    (Path("english.pdf"), "en"),
    (Path("chinese.pdf"), "ch"),
    (Path("japanese.pdf"), "japan")
]

for pdf_path, language in documents:
    parse_doc(
        path_list=[pdf_path],
        output_dir="output",
        lang=language
    )
```

#### Language Performance Notes

**Best performance**:
- English (`en`)
- Chinese Simplified (`ch_server` for highest accuracy)
- European languages (Latin group)

**Moderate performance**:
- Japanese, Korean
- Cyrillic scripts
- Thai, Devanagari

**Challenging**:
- Arabic script (easily confused characters)
- Diacritical marks in Latin scripts
- Mixed-script documents

**Common Mistake**: Using wrong language model
```python
# ❌ Using English for Chinese text
parse_doc(..., lang="en")  # Poor results for Chinese

# ✅ Use appropriate language
parse_doc(..., lang="ch")  # Much better results
```

**Tip**: If text is garbled, try:
1. Checking language setting
2. Forcing OCR mode (`method="ocr"`)
3. Installing CJK fonts on Linux systems

---

### Concept 5: Flexible Deployment Architecture

MinerU offers multiple ways to deploy and scale.

#### Local Processing (Default)

**Single-machine processing**: Everything runs on your machine.

```python
parse_doc(
    path_list=[Path("doc.pdf")],
    output_dir="output",
    backend="hybrid-auto-engine"  # Local processing
)
```

**Pros**:
- No network latency
- Data privacy (nothing leaves your machine)
- No API costs

**Cons**:
- Resource-intensive (uses your RAM/GPU)
- Scales only with your hardware

#### Client-Server Architecture

**Scenario**: Lightweight CPU clients + powerful GPU server.

**Setup**:

**Server** (GPU machine):
```bash
# Start VLM inference server
mineru-vllm-server \
  --host 0.0.0.0 \
  --port 8001 \
  --model opendatalab/MinerU2.5-2509-1.2B-hf
```

**Client** (CPU machine):
```python
parse_doc(
    path_list=[Path("doc.pdf")],
    output_dir="output",
    backend="vlm-http-client",  # Use remote server
    server_url="http://gpu-server:8001"  # Server address
)
```

**Benefits**:
- CPU-only clients can use GPU processing
- Centralized resource management
- Scale by adding more servers
- Multiple clients share one GPU server

**Use cases**:
- Team with one GPU machine
- Cloud deployment with GPU instances
- Batch processing from multiple sources

#### API Server

**FastAPI REST API** for HTTP-based processing.

**Start server**:
```bash
mineru-api --host 0.0.0.0 --port 8000
```

**Access API docs**: http://127.0.0.1:8000/docs

**Use from any language**:

Python:
```python
import requests

response = requests.post(
    "http://localhost:8000/parse",
    json={
        "pdf_url": "https://example.com/document.pdf",
        "backend": "hybrid-auto-engine"
    },
    headers={"Authorization": "Bearer YOUR_TOKEN"}
)

result = response.json()
```

cURL:
```bash
curl -X POST http://localhost:8000/parse \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"pdf_url":"https://example.com/doc.pdf"}'
```

**Benefits**:
- Language-agnostic (HTTP interface)
- Stateless, scalable
- Easy integration with existing systems

#### Web Interface (Gradio)

**Interactive web UI** for manual processing.

```bash
mineru-gradio --server-name 0.0.0.0 --server-port 7860
```

**Access**: http://127.0.0.1:7860

**Features**:
- Upload PDFs through browser
- Visual feedback and previews
- Download results directly
- No coding required

**Use cases**:
- One-off document processing
- Demos and presentations
- Non-technical users

#### Cloud Services

**Official cloud**: https://mineru.net
- 2000 pages/day at highest priority
- No installation needed
- API access with token

**Limitations**:
- 200MB max file size
- 600 pages max per file
- Beta service (limits may change)

#### Deployment Decision Tree

```
What's your use case?

├─ Quick local processing
│  └─ Use: Command-line or Python API locally

├─ Team with shared GPU server
│  └─ Use: Client-server architecture

├─ Web service / production API
│  └─ Use: FastAPI server + load balancer

├─ Non-technical users
│  └─ Use: Gradio web interface

└─ No local resources
   └─ Use: Official cloud service at mineru.net
```

**Common Mistake**: Running VLM backend on CPU
```python
# ❌ VLM backend requires GPU (10GB+ VRAM)
parse_doc(..., backend="vlm-auto-engine")  # Fails on CPU

# ✅ Options:
# 1. Use hybrid backend (works on CPU)
parse_doc(..., backend="hybrid-auto-engine")

# 2. Use remote GPU server
parse_doc(..., backend="vlm-http-client", server_url="...")

# 3. Use pipeline backend (CPU-friendly)
parse_doc(..., backend="pipeline")
```

---

### Concepts Summary

| Concept | Key Idea | Common Mistake |
|---------|----------|----------------|
| **Multiple Backends** | Choose speed vs accuracy | Using VLM without GPU |
| **Layout Understanding** | Structure + reading order | Expecting perfection on complex docs |
| **Content Recognition** | Formulas, tables, images | Not enabling features explicitly |
| **Multilingual OCR** | 109 languages supported | Wrong language code |
| **Flexible Deployment** | Local, server, cloud | Not choosing right architecture |

**You've mastered the concepts!** Next: Apply them in practical patterns.

---

## Level 4: Practical Patterns

Now let's build real-world document processing pipelines using MinerU's concepts.

### Pattern 1: Simple Document Extraction

**Scenario**: Extract content from a single PDF for reading or analysis.

**Code**:

```python
from pathlib import Path
from mineru.cli.client import parse_doc

def extract_simple_pdf(pdf_path: str, output_dir: str = "output"):
    """
    Extract content from a PDF into markdown format.

    Args:
        pdf_path: Path to input PDF
        output_dir: Where to save results
    """
    parse_doc(
        path_list=[Path(pdf_path)],
        output_dir=output_dir,
        backend="hybrid-auto-engine",  # Best balance
        lang="en"  # Adjust for your language
    )

    # Output location
    pdf_name = Path(pdf_path).stem
    markdown_file = Path(output_dir) / pdf_name / "auto" / f"{pdf_name}.md"

    print(f"✅ Extraction complete!")
    print(f"📄 Markdown: {markdown_file}")

    return markdown_file

# Usage
extract_simple_pdf("research_paper.pdf")
```

**Expected output**:
```
✅ Extraction complete!
📄 Markdown: output/research_paper/auto/research_paper.md
```

**When to use**:
- Single document processing
- Manual review needed
- One-off conversions

---

### Pattern 2: Batch Processing Multiple PDFs

**Scenario**: Process an entire folder of PDFs.

**Code**:

```python
from pathlib import Path
from mineru.cli.client import parse_doc
from typing import List

def batch_extract_pdfs(input_folder: str, output_dir: str = "batch_output"):
    """
    Process all PDFs in a folder.

    Args:
        input_folder: Folder containing PDFs
        output_dir: Where to save results
    """
    # Find all PDFs
    pdf_files = list(Path(input_folder).glob("*.pdf"))

    if not pdf_files:
        print(f"❌ No PDFs found in {input_folder}")
        return

    print(f"📚 Found {len(pdf_files)} PDFs to process")

    # Process all at once
    parse_doc(
        path_list=pdf_files,
        output_dir=output_dir,
        backend="hybrid-auto-engine",
        lang="en"
    )

    print(f"✅ Processed {len(pdf_files)} documents")
    print(f"📁 Results in: {output_dir}")

# Usage
batch_extract_pdfs("./pdfs_to_process", "output")
```

**For better control** (process one-by-one):

```python
def batch_extract_with_progress(input_folder: str, output_dir: str = "output"):
    """Process PDFs one by one with progress tracking."""
    from tqdm import tqdm  # Progress bar

    pdf_files = list(Path(input_folder).glob("*.pdf"))

    for pdf_file in tqdm(pdf_files, desc="Processing PDFs"):
        try:
            parse_doc(
                path_list=[pdf_file],
                output_dir=output_dir,
                backend="hybrid-auto-engine",
                lang="en"
            )
            print(f"✅ {pdf_file.name}")
        except Exception as e:
            print(f"❌ {pdf_file.name}: {e}")

# Usage
batch_extract_with_progress("./papers")
```

**When to use**:
- Processing document archives
- Building datasets
- Automated pipelines

---

### Pattern 3: Language-Specific Processing

**Scenario**: Handle documents in different languages correctly.

**Code**:

```python
from pathlib import Path
from mineru.cli.client import parse_doc
import fast_langdetect  # Optional: auto-detect language

# Language mapping
LANGUAGE_CODES = {
    "en": "en",
    "zh-cn": "ch",
    "zh-tw": "chinese_cht",
    "ja": "japan",
    "ko": "korean",
    "es": "latin",
    "fr": "latin",
    "de": "latin",
    "ar": "arabic",
    "ru": "cyrillic"
}

def extract_multilingual_pdf(pdf_path: str, language: str = None):
    """
    Extract PDF with language-specific OCR.

    Args:
        pdf_path: Path to PDF
        language: ISO language code (e.g., 'en', 'zh-cn')
                  If None, attempts auto-detection
    """
    # Auto-detect if not specified
    if language is None:
        # Simple heuristic: check filename or use default
        language = "en"  # Default to English
        print(f"⚠️  No language specified, using: {language}")

    # Map to MinerU language code
    mineru_lang = LANGUAGE_CODES.get(language, "en")

    print(f"🌍 Processing with language: {mineru_lang}")

    parse_doc(
        path_list=[Path(pdf_path)],
        output_dir="output",
        backend="hybrid-auto-engine",
        lang=mineru_lang
    )

# Usage examples
extract_multilingual_pdf("paper_english.pdf", "en")
extract_multilingual_pdf("论文_中文.pdf", "zh-cn")
extract_multilingual_pdf("논문_한국어.pdf", "ko")
```

**Advanced: Batch with language detection**:

```python
def batch_extract_multilingual(pdf_language_pairs: List[tuple]):
    """
    Process multiple PDFs with different languages.

    Args:
        pdf_language_pairs: List of (pdf_path, language_code) tuples
    """
    for pdf_path, lang_code in pdf_language_pairs:
        mineru_lang = LANGUAGE_CODES.get(lang_code, "en")

        print(f"📄 Processing {Path(pdf_path).name} ({mineru_lang})")

        parse_doc(
            path_list=[Path(pdf_path)],
            output_dir="output",
            lang=mineru_lang
        )

# Usage
documents = [
    ("report_en.pdf", "en"),
    ("报告_中文.pdf", "zh-cn"),
    ("レポート.pdf", "ja"),
    ("доклад.pdf", "ru")
]

batch_extract_multilingual(documents)
```

**When to use**:
- International document collections
- Multi-language research
- Global content processing

---

### Pattern 4: Scientific Paper Processing

**Scenario**: Extract structured data from academic papers (formulas, tables, figures).

**Code**:

```python
from pathlib import Path
from mineru.cli.client import parse_doc
import json

def extract_scientific_paper(
    pdf_path: str,
    output_dir: str = "papers_output",
    visualize: bool = True
):
    """
    Extract scientific paper with formula and table recognition.

    Args:
        pdf_path: Path to research paper PDF
        output_dir: Output directory
        visualize: Generate layout visualization
    """
    from mineru.cli.client import do_parse

    print(f"🔬 Processing scientific paper: {Path(pdf_path).name}")

    do_parse(
        pdf_path=pdf_path,
        output_dir=output_dir,
        backend="vlm-auto-engine",  # Highest accuracy for papers
        lang="en",
        formula_enable=True,  # Enable formula recognition
        table_enable=True,    # Enable table recognition
        f_dump_md=True,       # Generate markdown
        f_dump_middle_json=True,  # Generate intermediate JSON
        f_draw_layout_bbox=visualize  # Layout visualization
    )

    pdf_name = Path(pdf_path).stem
    output_path = Path(output_dir) / pdf_name / "auto"

    # Load structured data
    middle_json = output_path / "middle.json"
    if middle_json.exists():
        with open(middle_json) as f:
            data = json.load(f)

        # Extract statistics
        num_pages = len(data.get("pages", []))
        formulas = [elem for page in data.get("pages", [])
                   for elem in page.get("elements", [])
                   if elem.get("type") == "formula"]
        tables = [elem for page in data.get("pages", [])
                 for elem in page.get("elements", [])
                 if elem.get("type") == "table"]

        print(f"📊 Statistics:")
        print(f"   Pages: {num_pages}")
        print(f"   Formulas: {len(formulas)}")
        print(f"   Tables: {len(tables)}")

    print(f"✅ Complete! Check {output_path}")

# Usage
extract_scientific_paper(
    "quantum_physics_paper.pdf",
    visualize=True
)
```

**Access extracted formulas**:

```python
def extract_formulas_from_paper(pdf_path: str):
    """Extract all LaTeX formulas from a paper."""
    # First process the paper
    extract_scientific_paper(pdf_path)

    # Read markdown output
    pdf_name = Path(pdf_path).stem
    md_file = Path("papers_output") / pdf_name / "auto" / f"{pdf_name}.md"

    with open(md_file) as f:
        content = f.read()

    # Extract inline formulas: $...$
    import re
    inline_formulas = re.findall(r'\$([^\$]+)\$', content)

    # Extract block formulas: $$...$$
    block_formulas = re.findall(r'\$\$([^\$]+)\$\$', content)

    print(f"Found {len(inline_formulas)} inline formulas")
    print(f"Found {len(block_formulas)} block formulas")

    return inline_formulas, block_formulas

# Usage
inline, block = extract_formulas_from_paper("paper.pdf")
for formula in block[:5]:  # Show first 5
    print(f"  {formula.strip()}")
```

**When to use**:
- Academic research mining
- Building training datasets from papers
- Extracting mathematical content
- Citation analysis pipelines

---

### Pattern 5: Building a RAG System Data Pipeline

**Scenario**: Prepare document collection for a Retrieval-Augmented Generation (RAG) system.

**Code**:

```python
from pathlib import Path
from mineru.cli.client import parse_doc
import json
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

    print(f"📚 Processing {len(pdf_files)} documents for RAG")

    # Process all PDFs
    parse_doc(
        path_list=pdf_files,
        output_dir=output_dir,
        backend="hybrid-auto-engine",
        lang="en"
    )

    # Extract and chunk content
    chunks = []

    for pdf_file in pdf_files:
        pdf_name = pdf_file.stem
        md_file = Path(output_dir) / pdf_name / "auto" / f"{pdf_name}.md"

        if not md_file.exists():
            print(f"⚠️  Skipping {pdf_name} (no markdown output)")
            continue

        with open(md_file) as f:
            content = f.read()

        # Simple chunking by paragraphs
        paragraphs = content.split('\n\n')
        current_chunk = ""

        for para in paragraphs:
            if len(current_chunk) + len(para) > chunk_size:
                # Save current chunk
                if current_chunk:
                    chunks.append({
                        "text": current_chunk.strip(),
                        "source": pdf_name,
                        "source_file": str(pdf_file)
                    })
                current_chunk = para
            else:
                current_chunk += "\n\n" + para

        # Add remaining chunk
        if current_chunk:
            chunks.append({
                "text": current_chunk.strip(),
                "source": pdf_name,
                "source_file": str(pdf_file)
            })

    # Save chunked dataset
    output_file = Path(output_dir) / "rag_chunks.json"
    with open(output_file, 'w') as f:
        json.dump(chunks, f, indent=2)

    print(f"✅ Created {len(chunks)} chunks")
    print(f"💾 Saved to: {output_file}")

    return chunks

# Usage
chunks = prepare_rag_dataset("./knowledge_base", chunk_size=1000)

# Sample output
print(f"\nSample chunk:")
print(f"Source: {chunks[0]['source']}")
print(f"Text: {chunks[0]['text'][:200]}...")
```

**Integrate with vector database**:

```python
def ingest_into_vectordb(chunks: List[Dict], collection_name: str = "documents"):
    """
    Ingest chunks into a vector database (example with ChromaDB).

    Note: Requires `pip install chromadb sentence-transformers`
    """
    import chromadb
    from chromadb.utils import embedding_functions

    # Initialize client
    client = chromadb.Client()

    # Create collection with embedding function
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    collection = client.create_collection(
        name=collection_name,
        embedding_function=sentence_transformer_ef
    )

    # Add documents
    collection.add(
        documents=[chunk["text"] for chunk in chunks],
        metadatas=[{"source": chunk["source"]} for chunk in chunks],
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )

    print(f"✅ Ingested {len(chunks)} chunks into ChromaDB")

# Full pipeline
chunks = prepare_rag_dataset("./docs")
ingest_into_vectordb(chunks)
```

**When to use**:
- Building knowledge bases for LLMs
- Question-answering systems
- Document search and retrieval
- AI-powered research assistants

---

### Pattern 6: API Server for Production

**Scenario**: Deploy MinerU as a production REST API service.

**Setup API server**:

```python
# server.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import tempfile
import shutil
from mineru.cli.client import parse_doc

app = FastAPI(title="MinerU API", version="1.0")

@app.post("/parse")
async def parse_pdf(
    file: UploadFile = File(...),
    backend: str = "hybrid-auto-engine",
    language: str = "en"
):
    """
    Parse uploaded PDF and return markdown content.
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(400, "Only PDF files are supported")

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

        with open(md_file) as f:
            markdown_content = f.read()

        return {
            "status": "success",
            "filename": file.filename,
            "markdown": markdown_content
        }

    except Exception as e:
        raise HTTPException(500, f"Processing failed: {str(e)}")

    finally:
        # Cleanup
        Path(tmp_path).unlink()
        shutil.rmtree(output_dir)

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

# Run with: uvicorn server:app --host 0.0.0.0 --port 8000
```

**Client usage**:

```python
# client.py
import requests

def parse_pdf_via_api(pdf_path: str, server_url: str = "http://localhost:8000"):
    """Send PDF to API server for processing."""

    with open(pdf_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            f"{server_url}/parse",
            files=files,
            params={'backend': 'hybrid-auto-engine', 'language': 'en'}
        )

    if response.status_code == 200:
        result = response.json()
        print(f"✅ Processed: {result['filename']}")
        return result['markdown']
    else:
        print(f"❌ Error: {response.status_code}")
        return None

# Usage
markdown = parse_pdf_via_api("document.pdf")
```

**When to use**:
- Production deployments
- Microservices architecture
- Multi-language client integration
- Scalable processing systems

---

### Pattern 7: GPU Server + CPU Clients

**Scenario**: Centralized GPU server serving multiple CPU-only clients.

**GPU Server setup**:

```bash
# On GPU machine (server)
mineru-vllm-server \
  --host 0.0.0.0 \
  --port 8001 \
  --model opendatalab/MinerU2.5-2509-1.2B-hf \
  --gpu-memory-utilization 0.9
```

**CPU Client**:

```python
# On CPU machine (client)
from pathlib import Path
from mineru.cli.client import parse_doc

def parse_using_remote_gpu(pdf_path: str, server_url: str = "http://gpu-server:8001"):
    """
    Process PDF using remote GPU server.

    Args:
        pdf_path: Local PDF path
        server_url: GPU server address
    """
    parse_doc(
        path_list=[Path(pdf_path)],
        output_dir="output",
        backend="vlm-http-client",  # Use HTTP client
        server_url=server_url,      # Connect to GPU server
        lang="en"
    )

    print(f"✅ Processed using remote GPU at {server_url}")

# Usage
parse_using_remote_gpu(
    "complex_paper.pdf",
    server_url="http://192.168.1.100:8001"
)
```

**Multiple clients**:

```python
# Different team members can use same GPU server
parse_using_remote_gpu("doc1.pdf", "http://gpu-server:8001")  # Client 1
parse_using_remote_gpu("doc2.pdf", "http://gpu-server:8001")  # Client 2
parse_using_remote_gpu("doc3.pdf", "http://gpu-server:8001")  # Client 3
```

**When to use**:
- Team with limited GPU resources
- Cloud deployment (GPU instances expensive)
- Distributed processing
- Cost optimization

---

### Practical Patterns Summary

| Pattern | Use Case | Key Code |
|---------|----------|----------|
| **Simple Extraction** | Single PDF, one-off | `parse_doc([Path(pdf)], ...)` |
| **Batch Processing** | Multiple PDFs | Loop or pass list |
| **Multilingual** | International docs | `lang="ch"` / `lang="japan"` |
| **Scientific Papers** | Formulas, tables | `formula_enable=True` |
| **RAG Pipeline** | Knowledge bases | Chunk markdown output |
| **API Server** | Production service | FastAPI + MinerU |
| **GPU Server** | Distributed processing | `backend="vlm-http-client"` |

**Next**: Level 5 - Advanced topics and community resources.

---

## Level 5: Next Steps

Congratulations! You've learned MinerU fundamentals. Here's where to go deeper.

### Advanced Topics to Explore

#### 1. Custom Model Configuration

**What**: Fine-tune MinerU's behavior with `mineru.json` configuration.

**Where to learn**:
- Official docs: https://opendatalab.github.io/MinerU/usage/advanced_usage/
- Example config: `~/.mineru.json`

**Topics**:
- Custom LaTeX delimiters
- LLM-assisted processing
- Local model paths
- Backend preferences
- S3 bucket integration

**Example**:
```json
{
  "layout_model": {
    "path": "/path/to/custom/layout/model"
  },
  "formula_config": {
    "enable": true,
    "model": "UniMERNet"
  },
  "table_config": {
    "enable": true,
    "model": "SLANet+"
  }
}
```

#### 2. Client-Server Deployment

**What**: Scale MinerU with distributed architecture.

**Where to learn**:
- MinerU Beginner's Guide: https://stable-learn.com/en/mineru-tutorial/ (Section: Client-Server Architecture)
- Official deployment guide (check docs)

**Topics**:
- Setting up VLM servers
- Load balancing multiple servers
- Authentication and security
- Docker deployment

#### 3. Performance Optimization

**What**: Speed up processing for large document collections.

**Where to learn**:
- GitHub Issues: Performance-related discussions
- Community Discord: #optimization channel

**Topics**:
- Batch size tuning (`MINERU_MIN_BATCH_INFERENCE_SIZE`)
- GPU memory optimization
- Multi-GPU processing
- Asynchronous processing (see `projects/` directory)

#### 4. Custom OCR Models

**What**: Use custom or alternative OCR models.

**Where to learn**:
- PaddleOCR documentation: https://github.com/PaddlePaddle/PaddleOCR
- MinerU model configuration docs

**Topics**:
- Training custom OCR for domain-specific text
- Integrating alternative OCR engines
- Fine-tuning for specific languages

#### 5. Extending MinerU

**What**: Build custom features and integrations.

**Where to learn**:
- GitHub `projects/` folder: Community extensions
- MinerU source code: `mineru/` directory

**Topics**:
- Custom output formats
- Additional content recognizers
- Integration with document management systems
- Plugins and extensions

---

### Best Resources for Each Topic

#### Official Resources

1. **Documentation** (Comprehensive)
   - URL: https://opendatalab.github.io/MinerU/
   - Best for: API reference, configuration, troubleshooting

2. **GitHub Repository** (Source code, examples)
   - URL: https://github.com/opendatalab/MinerU
   - Best for: Code examples, issues, discussions

3. **Research Paper** (Deep technical details)
   - URL: https://arxiv.org/abs/2409.18839
   - Best for: Understanding architecture, model performance

#### Community Tutorials

4. **MinerU Beginner's Guide** by Suke (Most comprehensive)
   - URL: https://stable-learn.com/en/mineru-tutorial/
   - Best for: Complete walkthrough, advanced features

5. **Extract Any PDF with MinerU 2.5** by Sonu Sahani (Practical insights)
   - URL: https://sonusahani.com/blogs/mineru
   - Best for: Real-world testing, production tips

6. **Deep Dive into PDF to Markdown Tools** by Jimmy Song (Comparisons)
   - URL: https://jimmysong.io/blog/pdf-to-markdown-open-source-deep-dive/
   - Best for: Choosing the right tool for your needs

#### Video & Interactive

7. **Hugging Face Demo** (Try online)
   - URL: https://huggingface.co/spaces/opendatalab/MinerU
   - Best for: Quick testing without installation

8. **YouTube** (Search for latest tutorials)
   - Query: "MinerU PDF extraction tutorial"
   - Best for: Visual walkthroughs

#### Comparison & Alternatives

9. **12 Open-Source PDF Parsing Tools Comparison**
   - URL: https://liduos.com/en/ai-develope-tools-series-2-open-source-doucment-parsing.html
   - Best for: Understanding strengths/weaknesses

10. **MinerU vs Marker Comparison**
    - URL: https://www.aitoolnet.com/compare/mineru-vs-marker
    - Best for: Deciding between top tools

---

### Community Resources

#### Where to Ask Questions

1. **Discord** (Most active)
   - URL: https://discord.com/invite/Tdedn9GTXq
   - 878+ members, responsive community

2. **GitHub Discussions** (Technical Q&A)
   - URL: https://github.com/opendatalab/MinerU/discussions

3. **GitHub Issues** (Bug reports, feature requests)
   - URL: https://github.com/opendatalab/MinerU/issues

#### Stay Updated

- **GitHub Releases**: https://github.com/opendatalab/MinerU/releases
- **PyPI Updates**: https://pypi.org/project/mineru/#history
- **Discord Announcements**: Join for latest news

#### Contributing

- **Contributing Guide**: See `CONTRIBUTING.md` on GitHub
- **Code of Conduct**: See `CODE_OF_CONDUCT.md`
- **Pull Requests**: Submit improvements, examples, docs

---

### How to Get Help

#### Troubleshooting Steps

1. **Check FAQ**: https://opendatalab.github.io/MinerU/faq/
2. **Search GitHub Issues**: Someone may have had the same problem
3. **Enable verbose logging**: Add debug flags to see detailed errors
4. **Ask on Discord**: Community usually responds within hours

#### Common Issues Quick Reference

| Problem | Solution | Link |
|---------|----------|------|
| LibGL missing | Install mesa | [FAQ](https://opendatalab.github.io/MinerU/faq/) |
| CJK text loss | Install fonts | [FAQ](https://opendatalab.github.io/MinerU/faq/) |
| Out of memory | Use pipeline backend | Concept 1 |
| Wrong language | Set correct `lang` | Concept 4 |
| Poor table accuracy | Complex tables are challenging | Known limitations |

#### When Asking for Help

Include:
1. **MinerU version**: `mineru --version`
2. **Python version**: `python --version`
3. **Operating system**: Linux/Windows/macOS
4. **Backend used**: pipeline/vlm/hybrid
5. **Error message**: Full traceback
6. **Sample PDF**: If possible, share (or describe structure)

---

### Mini-Project: Build a Document Q&A System

**Goal**: Combine MinerU with an LLM to create a question-answering system over your documents.

#### Project Steps

**Step 1**: Process your document collection
```python
from pathlib import Path
from mineru.cli.client import parse_doc

# Process all PDFs in a folder
parse_doc(
    path_list=list(Path("./documents").glob("*.pdf")),
    output_dir="processed_docs",
    backend="hybrid-auto-engine"
)
```

**Step 2**: Index documents (use ChromaDB or similar)
```python
import chromadb
from chromadb.utils import embedding_functions

client = chromadb.Client()
ef = embedding_functions.SentenceTransformerEmbeddingFunction()

collection = client.create_collection("docs", embedding_function=ef)

# Add processed markdown files
for md_file in Path("processed_docs").rglob("*.md"):
    with open(md_file) as f:
        content = f.read()

    collection.add(
        documents=[content],
        ids=[md_file.stem]
    )
```

**Step 3**: Query with LLM
```python
def ask_question(question: str):
    # Retrieve relevant documents
    results = collection.query(
        query_texts=[question],
        n_results=3
    )

    context = "\n\n".join(results['documents'][0])

    # Send to LLM (example with OpenAI)
    from openai import OpenAI
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Answer based on provided context."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ]
    )

    return response.choices[0].message.content

# Usage
answer = ask_question("What are the key findings in the research papers?")
print(answer)
```

**Extensions**:
- Add web interface with Streamlit/Gradio
- Support follow-up questions
- Show source documents for citations
- Multi-language support

---

### Hands-On Exercises

#### Exercise 1: Multilingual Processing
Process documents in 3 different languages and compare results.

**Tasks**:
1. Find PDFs in English, Chinese, and Spanish
2. Process each with correct language code
3. Compare accuracy and processing time
4. Document challenges for each language

#### Exercise 2: Scientific Paper Mining
Extract all formulas and tables from a set of research papers.

**Tasks**:
1. Download 10 scientific papers (arXiv works great)
2. Process with formula and table recognition enabled
3. Extract all LaTeX formulas using regex
4. Save tables as CSV files
5. Analyze formula/table distribution

#### Exercise 3: Build a Document Converter
Create a web app that converts PDFs to markdown.

**Tasks**:
1. Build Gradio interface
2. Allow file upload
3. Show processing progress
4. Display markdown output
5. Provide download button
6. Add error handling

#### Exercise 4: Performance Benchmarking
Compare processing speed across backends.

**Tasks**:
1. Select 20 PDFs of varying complexity
2. Time processing with each backend (pipeline, vlm, hybrid)
3. Measure memory usage
4. Compare output quality
5. Create performance report

#### Exercise 5: Production API
Deploy MinerU as a production-ready API.

**Tasks**:
1. Create FastAPI server with authentication
2. Add rate limiting
3. Implement job queue (Celery/Redis)
4. Add monitoring (Prometheus)
5. Deploy with Docker
6. Write API documentation

---

### Success Criteria

You've mastered MinerU when you can:

✅ Extract content from any PDF reliably
✅ Choose the right backend for your use case
✅ Handle multilingual documents correctly
✅ Build production-ready document pipelines
✅ Troubleshoot common issues independently
✅ Integrate MinerU into larger systems
✅ Optimize performance for your needs

---

### Final Tips

1. **Start simple**: Don't overcomplicate early projects
2. **Test with diverse PDFs**: Different document types behave differently
3. **Monitor resource usage**: MinerU can be memory-intensive
4. **Join the community**: Discord is invaluable for tips and help
5. **Contribute back**: Share your learnings, examples, and improvements
6. **Stay updated**: MinerU is actively developed; new features arrive regularly
7. **Read the source**: When docs aren't clear, the code is well-structured
8. **Experiment boldly**: Try different backends and configurations

---

### You're Ready! 🎉

You now have everything needed to:
- Process documents at any scale
- Build intelligent document systems
- Integrate MinerU into production workflows
- Contribute to the community

**What will you build with MinerU?**

Share your projects in the Discord community - we'd love to see what you create!

---

## Additional Resources

See `resources.md` for:
- Complete link directory
- Community tutorials
- Comparison articles
- Troubleshooting guides
- Real-world use cases

**Happy document processing!** 📄✨
