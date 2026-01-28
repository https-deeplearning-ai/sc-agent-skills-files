# Practical Patterns Examples

Real-world document processing pipelines and production use cases.

## Files

- `rag_pipeline.py` - Prepare documents for RAG systems
- `api_server.py` - Deploy MinerU as REST API service
- `client_example.py` - Example API client usage

## Patterns

### 1. RAG System Pipeline

Prepare document collections for vector databases and RAG systems.

**Install dependencies**:
```bash
pip install "mineru[all]"
```

**Usage**:
```bash
# Process folder of PDFs
python rag_pipeline.py ./knowledge-base

# Custom chunk size
python rag_pipeline.py ./docs --chunk-size 500

# Custom output directory
python rag_pipeline.py ./papers --output-dir processed_papers
```

**Output**:
```
rag_data/
├── document1/
│   └── auto/
│       └── document1.md
├── document2/
│   └── auto/
│       └── document2.md
└── rag_chunks.json  # Ready for vector DB
```

**rag_chunks.json format**:
```json
[
  {
    "id": "document1_chunk_0",
    "text": "Content of first chunk...",
    "source": "document1",
    "source_file": "/path/to/document1.pdf",
    "chunk_index": 0
  },
  ...
]
```

**Next steps**:
1. Generate embeddings (sentence-transformers, OpenAI, etc.)
2. Ingest into vector database (ChromaDB, Pinecone, Weaviate)
3. Build query interface
4. Connect to LLM for RAG

### 2. API Server

Deploy MinerU as a production REST API.

**Install dependencies**:
```bash
pip install fastapi uvicorn python-multipart "mineru[all]"
```

**Start server**:
```bash
python api_server.py
# Server runs on http://localhost:8000
```

**API Documentation**: http://localhost:8000/docs

**Endpoints**:

- `GET /` - API info
- `GET /health` - Health check
- `POST /parse` - Parse single PDF
- `POST /parse-batch` - Parse multiple PDFs

**Test with cURL**:

```bash
# Health check
curl http://localhost:8000/health

# Parse PDF
curl -X POST http://localhost:8000/parse \
  -F "file=@document.pdf" \
  -F "backend=hybrid-auto-engine" \
  -F "language=en"

# Parse with custom settings
curl -X POST http://localhost:8000/parse \
  -F "file=@chinese.pdf" \
  -F "backend=pipeline" \
  -F "language=ch"
```

**Test with Python** (see `client_example.py`):

```python
import requests

# Upload PDF
with open("document.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/parse",
        files={"file": f},
        data={"backend": "hybrid-auto-engine", "language": "en"}
    )

result = response.json()
print(result["markdown"])
```

**Production deployment**:
```bash
# With Gunicorn (production WSGI server)
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api_server:app

# With Docker
docker build -t mineru-api .
docker run -p 8000:8000 mineru-api
```

### 3. Client Example

Use the API from Python code.

```bash
python client_example.py http://localhost:8000 document.pdf
```

See `client_example.py` for implementation details.

## Use Cases

### Academic Research
Process research paper collections:
```bash
python rag_pipeline.py ./research-papers --chunk-size 1500
```

### Enterprise Documents
Batch process business documents:
```bash
python rag_pipeline.py ./contracts --chunk-size 800
```

### Knowledge Base
Build searchable knowledge base:
```bash
python rag_pipeline.py ./documentation
# Then ingest rag_chunks.json into your vector DB
```

### Multi-tenant API
Deploy API server for multiple users:
```bash
python api_server.py
# Add authentication middleware
# Add rate limiting
# Add usage tracking
```

## Performance Tips

**For large collections**:
1. Use pipeline backend for speed: `backend="pipeline"`
2. Process in batches (not all at once)
3. Use appropriate chunk size (500-1500 chars)
4. Monitor memory usage

**For production API**:
1. Use process pool (Gunicorn workers)
2. Add request queuing (Redis/Celery)
3. Set timeouts for long documents
4. Add caching for repeated requests
5. Monitor with Prometheus/Grafana

**For GPU servers**:
1. Use VLM backend for accuracy: `backend="vlm-auto-engine"`
2. Batch requests to GPU server
3. Monitor GPU memory usage
4. Load balance across multiple GPUs

## Next Steps

- Integrate with your vector database (ChromaDB, Pinecone, etc.)
- Add authentication to API (JWT, API keys)
- Build web UI with Streamlit/Gradio
- Deploy with Docker/Kubernetes
- Add monitoring and logging
- Implement job queue for long-running tasks

## Resources

- FastAPI docs: https://fastapi.tiangolo.com/
- ChromaDB docs: https://docs.trychroma.com/
- RAG guide: https://python.langchain.com/docs/use_cases/question_answering/
