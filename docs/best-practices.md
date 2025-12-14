# Best Practices

Guidelines for building production-ready RAG applications with SmartGenAI.

## Table of Contents

1. [Document Processing](#document-processing)
2. [Chunking Strategies](#chunking-strategies)
3. [Embedding Selection](#embedding-selection)
4. [Vector Store Management](#vector-store-management)
5. [LLM Configuration](#llm-configuration)
6. [Performance Optimization](#performance-optimization)
7. [Error Handling](#error-handling)
8. [Security Considerations](#security-considerations)

---

## Document Processing

### Choose the Right Parser

| Document Type | Recommended Parser | Use Case |
|---------------|-------------------|----------|
| Simple PDFs | PyMuPDF (`simplePdf`) | Fast, local processing |
| Complex PDFs | LlamaParse | Tables, complex layouts, OCR |
| Web pages | HTML parser | Dynamic content extraction |
| Plain text | `readTXT()` | Log files, markdown |

### Handle Large Documents

```python
# Process large PDFs in page ranges
for start in range(0, total_pages, 10):
    config = json.dumps({
        "pclass": "smartgenai.connectors.documents.simplePdf",
        "fromPage": start,
        "toPage": min(start + 10, total_pages)
    })
    partial_doc = rag.read(filename, config)
    # Process partial_doc...
```

### Remove Headers and Footers

```python
config = json.dumps({
    "pclass": "smartgenai.connectors.documents.simplePdf",
    "heightToRemove": 50  # Pixels to remove from top/bottom
})
```

---

## Chunking Strategies

### Character Chunking Guidelines

| Document Size | Recommended Size | Overlap |
|---------------|------------------|---------|
| < 10 pages | 200-300 | 20-30 |
| 10-50 pages | 400-600 | 50-75 |
| > 50 pages | 800-1200 | 100-150 |

### Use Semantic Chunking for Quality

Semantic chunking produces better results but is slower:

```python
# For high-quality results
config = json.dumps({"method": "semantic"})

# For fast processing
config = json.dumps({
    "method": "character",
    "separator": ".",
    "size": 500,
    "overlap": 50
})
```

### Consider Context Windows

Ensure chunks fit within your LLM's context window:

```python
# Ollama default: 2048 tokens
# Leave room for prompt template and response
max_chunk_size = 1500  # characters, roughly 375 tokens

config = json.dumps({
    "method": "character",
    "separator": ".",
    "size": max_chunk_size,
    "overlap": 100
})
```

---

## Embedding Selection

### Model Comparison

| Model | Speed | Quality | Dimensions | Best For |
|-------|-------|---------|------------|----------|
| all-MiniLM-L6-v2 | ⚡⚡⚡ | ⭐⭐ | 384 | Quick prototypes |
| paraphrase-mpnet-base-v2 | ⚡⚡ | ⭐⭐⭐ | 768 | General use |
| all-mpnet-base-v2 | ⚡ | ⭐⭐⭐⭐ | 768 | High accuracy |
| nomic-embed-text (Ollama) | ⚡⚡ | ⭐⭐⭐ | 768 | Local processing |

### Use Consistent Embeddings

Always use the same embedding model for indexing and querying:

```python
# Define once, use everywhere
EMBEDDING_CONFIG = json.dumps({
    "pclass": "smartgenai.connectors.embeddings.sentenceTransformer",
    "model": "paraphrase-mpnet-base-v2"
})

# For indexing
embeddings = rag.createEmbeddings(chunks, EMBEDDING_CONFIG)

# For querying
query_embeddings = rag.createEmbeddings(query_chunks, EMBEDDING_CONFIG)
```

---

## Vector Store Management

### FAISS vs ChromaDB

| Feature | FAISS | ChromaDB |
|---------|-------|----------|
| Speed | ⚡⚡⚡ | ⚡⚡ |
| Persistence | File-based | Database |
| Metadata | Limited | Full support |
| Scalability | High | High |
| Use case | Speed-critical | Feature-rich |

### Index Maintenance

```python
# For FAISS: Rebuild index periodically
def rebuild_index(documents, config):
    # Clear old index
    import os
    for ext in ['.index', '.data']:
        filepath = os.path.join(config['filepath'], config['name'] + ext)
        if os.path.exists(filepath):
            os.remove(filepath)
    
    # Rebuild
    for doc in documents:
        process_document(doc, config)
```

### Use Collections in ChromaDB

```python
# Organize documents by topic
topics = ['technical', 'legal', 'marketing']

for topic in topics:
    config = json.dumps({
        "pclass": "smartgenai.connectors.vstore.ChromaDB",
        "host": "localhost",
        "port": 8000,
        "collection": f"docs_{topic}"
    })
    # Process documents for this topic...
```

---

## LLM Configuration

### Temperature Guidelines

| Use Case | Temperature | Description |
|----------|-------------|-------------|
| Factual Q&A | 0.1 - 0.3 | Consistent, accurate |
| General chat | 0.5 - 0.7 | Balanced |
| Creative | 0.8 - 1.0 | Varied, creative |

### Context Window Management

```python
# Estimate tokens (rough: 1 token ≈ 4 characters)
def estimate_tokens(text):
    return len(text) // 4

# Build prompt within limits
def build_safe_prompt(question, context_items, max_tokens=1500):
    prompt_parts = []
    token_count = estimate_tokens(question)
    
    for item in context_items.items:
        item_tokens = estimate_tokens(item)
        if token_count + item_tokens < max_tokens:
            prompt_parts.append(item)
            token_count += item_tokens
        else:
            break
    
    return build_prompt(question, prompt_parts)
```

### Model Selection

| Task | Recommended Model | Notes |
|------|------------------|-------|
| Quick tests | tinydolphin | Fast, low resources |
| General use | mistral, llama2 | Good balance |
| Complex tasks | Claude, GPT-4 | Best quality |
| Code | codellama | Code-optimized |

---

## Performance Optimization

### Batch Processing

```python
# Process multiple documents efficiently
from concurrent.futures import ThreadPoolExecutor

def process_document(filepath):
    rag = ragWrapper()
    doc = rag.read(filepath, doc_config)
    chunks = rag.chunk(doc, chunk_config)
    embeddings = rag.createEmbeddings(chunks, embedding_config)
    return embeddings

# Process in parallel
with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(process_document, file_list))
```

### Caching Embeddings

```python
import hashlib
import json
import os

def get_cached_embeddings(text, config, cache_dir="./cache"):
    # Generate cache key
    key = hashlib.md5(f"{text}{config}".encode()).hexdigest()
    cache_file = os.path.join(cache_dir, f"{key}.json")
    
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)
    
    # Create embeddings
    chunks = Chunks()
    chunks.add(text)
    embeddings = rag.createEmbeddings(chunks, config)
    
    # Cache
    os.makedirs(cache_dir, exist_ok=True)
    with open(cache_file, 'w') as f:
        f.write(embeddings.jsonContent)
    
    return embeddings
```

### Optimize K Value

```python
# Start with fewer results, increase if needed
def adaptive_search(query, min_k=3, max_k=10, min_score=0.5):
    k = min_k
    while k <= max_k:
        results = rag.similaritySearch(k, query_emb, config)
        
        # Check if we have enough good results
        good_results = [
            r for i, r in enumerate(results.items)
            if results.distances[i] < min_score
        ]
        
        if len(good_results) >= min_k:
            return results
        
        k += 2
    
    return results
```

---

## Error Handling

### Graceful Degradation

```python
def safe_rag_query(question, document_path):
    try:
        # Try full RAG pipeline
        doc = rag.read(document_path, doc_config)
        chunks = rag.chunk(doc, chunk_config)
        # ... rest of pipeline
        return response
    
    except FileNotFoundError:
        return "Document not found. Please check the file path."
    
    except Exception as e:
        # Log error
        print(f"RAG failed: {e}")
        
        # Fallback to direct LLM query
        response, _ = rag.prompt(llm_config, question)
        return f"(Without context) {response}"
```

### Retry Logic

```python
import time

def retry_with_backoff(func, max_retries=3, base_delay=1):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            print(f"Attempt {attempt + 1} failed, retrying in {delay}s...")
            time.sleep(delay)
```

### Validate Responses

```python
def validate_response(response, question):
    # Check for empty response
    if not response or len(response.strip()) < 10:
        return False, "Response too short"
    
    # Check for error messages
    error_phrases = ["I don't know", "I cannot", "Error"]
    for phrase in error_phrases:
        if phrase.lower() in response.lower():
            return False, "Response indicates uncertainty"
    
    return True, "Valid"
```

---

## Security Considerations

### Protect API Keys

```python
import os
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

config = {
    "pclass": "smartgenai.connectors.llms.AWSModels.Claude",
    "region": "us-east-1",
    "model": "anthropic.claude-3-sonnet-20240229-v1:0",
    "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
    "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY")
}
```

### Sanitize User Input

```python
import re

def sanitize_input(text):
    # Remove potential injection patterns
    text = re.sub(r'<[^>]+>', '', text)  # Remove HTML
    text = re.sub(r'\{[^}]+\}', '', text)  # Remove template syntax
    text = text.strip()
    
    # Limit length
    max_length = 1000
    if len(text) > max_length:
        text = text[:max_length]
    
    return text
```

### Validate Document Sources

```python
import os

ALLOWED_EXTENSIONS = {'.pdf', '.txt', '.html'}
ALLOWED_DOMAINS = {'docs.example.com', 'internal.example.com'}

def validate_source(source):
    if source.startswith('http'):
        from urllib.parse import urlparse
        domain = urlparse(source).netloc
        if domain not in ALLOWED_DOMAINS:
            raise ValueError(f"Domain not allowed: {domain}")
    else:
        ext = os.path.splitext(source)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise ValueError(f"File type not allowed: {ext}")
```

---

## Monitoring and Logging

### Track Performance

```python
import time

class RAGMetrics:
    def __init__(self):
        self.metrics = []
    
    def track(self, operation, duration, success):
        self.metrics.append({
            'operation': operation,
            'duration': duration,
            'success': success,
            'timestamp': time.time()
        })
    
    def summary(self):
        import statistics
        by_operation = {}
        for m in self.metrics:
            op = m['operation']
            if op not in by_operation:
                by_operation[op] = []
            by_operation[op].append(m['duration'])
        
        return {
            op: {
                'avg': statistics.mean(durations),
                'max': max(durations),
                'count': len(durations)
            }
            for op, durations in by_operation.items()
        }
```

### Use Traces

```python
# Always check traces for debugging
rag = ragWrapper()
# ... operations ...

trace = rag.trace.getFullJSON()
import json
trace_data = json.loads(trace)

if trace_data.get('errors', 0) > 0:
    print("Errors detected!")
    for log in trace_data.get('logs', []):
        if log.get('level') == 'ERROR':
            print(f"  - {log.get('message')}")
```

---

For more examples, see the [Examples](examples/) directory.

