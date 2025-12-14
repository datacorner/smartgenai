# SmartGenAI Examples

This directory contains practical examples demonstrating how to use SmartGenAI.

## Examples Overview

| Example | Description | Prerequisites |
|---------|-------------|---------------|
| [basic_rag.py](basic_rag.py) | Complete RAG pipeline with PDF | Ollama + PDF file |
| [simple_llm_prompt.py](simple_llm_prompt.py) | Simple LLM interactions | Ollama or AWS/HF credentials |
| [web_content_rag.py](web_content_rag.py) | Analyze web pages | Ollama |
| [persistent_index.py](persistent_index.py) | Create & query persistent indexes | Ollama + PDF files |
| [similarity_scoring.py](similarity_scoring.py) | Text similarity calculations | None |

## Quick Start

### 1. Basic RAG (Recommended First Example)

```bash
# Ensure Ollama is running
ollama pull tinydolphin

# Place a PDF in the data directory, then run:
python basic_rag.py
```

### 2. Simple LLM Prompt

```bash
# Test different LLM providers
python simple_llm_prompt.py
```

### 3. Web Content Analysis

```bash
# Analyze any web page
python web_content_rag.py
```

### 4. Persistent Index

```bash
# Build a searchable document index
python persistent_index.py
```

### 5. Similarity Scoring

```bash
# Calculate text similarities
python similarity_scoring.py
```

## Requirements

### For Local Execution (Ollama)

```bash
# Install Ollama
# Download from https://ollama.com/

# Pull models
ollama pull tinydolphin    # LLM
ollama pull all-minilm     # Embeddings (optional)
```

### For AWS Bedrock

```bash
# Set environment variables
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
```

### For Hugging Face

```bash
# Set environment variable
export HUGGINGFACE_API_KEY="your-token"
```

## Creating Your Own Examples

### Basic Template

```python
from smartgenai.ragWrapper import ragWrapper
from smartgenai.framework.sets.chunks import chunks as Chunks
import json

def main():
    # Initialize
    rag = ragWrapper()
    
    # Configure components (as JSON)
    llm_config = json.dumps({
        "pclass": "smartgenai.connectors.llms.ollama",
        "url": "http://localhost:11434/api",
        "model": "tinydolphin",
        "temperature": 0.7,
        "contextwindow": 2048
    })
    
    # Use the RAG wrapper
    response, outputs = rag.prompt(llm_config, "Hello!")
    print(response)
    
    # Check trace for debugging
    print(rag.trace.getFullJSON())

if __name__ == "__main__":
    main()
```

### RAG Template

```python
from smartgenai.ragWrapper import ragWrapper
from smartgenai.framework.sets.chunks import chunks as Chunks
import json

def main():
    rag = ragWrapper()
    
    # 1. Read document
    doc_config = json.dumps({
        "pclass": "smartgenai.connectors.documents.simplePdf"
    })
    document = rag.read("document.pdf", doc_config)
    
    # 2. Chunk
    chunk_config = json.dumps({
        "method": "character",
        "separator": ".",
        "size": 500,
        "overlap": 50
    })
    chunks = rag.chunk(document, chunk_config)
    
    # 3. Embed
    embedding_config = json.dumps({
        "pclass": "smartgenai.connectors.embeddings.sentenceTransformer"
    })
    embeddings = rag.createEmbeddings(chunks, embedding_config)
    
    # 4. Search & Answer
    faiss_config = json.dumps({
        "pclass": "smartgenai.connectors.vstore.faiss"
    })
    
    llm_config = json.dumps({
        "pclass": "smartgenai.connectors.llms.ollama",
        "url": "http://localhost:11434/api",
        "model": "tinydolphin",
        "temperature": 0.5,
        "contextwindow": 2048
    })
    
    # Query
    question = "What is the main topic?"
    q_chunks = Chunks()
    q_chunks.add(question)
    q_embeddings = rag.createEmbeddings(q_chunks, embedding_config)
    
    similar = rag.memSimilaritySearch(
        k=3,
        textEmbeddings=q_embeddings.jsonContent,
        listEmbeddings=embeddings.jsonContent,
        jsonConfig=faiss_config
    )
    
    prompt = rag.buildPrompt(question, similar)
    response, _ = rag.prompt(llm_config, prompt)
    print(response)

if __name__ == "__main__":
    main()
```

## Troubleshooting

### "Connection refused" error

Ollama is not running. Start it:
```bash
ollama serve
```

### "Model not found" error

Pull the required model:
```bash
ollama pull tinydolphin
```

### Import errors

Reinstall SmartGenAI:
```bash
pip install --force-reinstall smartgenai
```

### Memory issues

- Use smaller chunk sizes
- Process documents in batches
- Use persistent FAISS storage

## More Resources

- [Getting Started Guide](../getting-started.md)
- [Configuration Reference](../configuration.md)
- [API Reference](../api-reference.md)
- [Best Practices](../best-practices.md)

