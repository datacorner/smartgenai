# Getting Started with SmartGenAI

This guide will help you get started with SmartGenAI, a lightweight RAG (Retrieval-Augmented Generation) framework.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Your First RAG Application](#your-first-rag-application)
4. [Understanding the Components](#understanding-the-components)
5. [Next Steps](#next-steps)

---

## Prerequisites

Before you begin, ensure you have:

- **Python 3.10 or higher** installed
- **pip** package manager
- (Optional) **Ollama** for local LLM execution
- (Optional) **ChromaDB** for persistent vector storage

### Hardware Requirements

SmartGenAI is designed to run on standard hardware:
- **Minimum**: 8GB RAM, any modern CPU
- **Recommended**: 16GB RAM for larger models and documents

---

## Installation

### Step 1: Install SmartGenAI

```bash
# Option A: From wheel file
pip install smartgenai-0.1.0.2-py3-none-any.whl

# Option B: From source
git clone https://github.com/datacorner/smartgenai.git
cd smartgenai
pip install -e .
```

### Step 2: Install Ollama (Recommended for Local LLMs)

1. Download from [ollama.com](https://ollama.com/)
2. Install and start Ollama
3. Pull a model:

```bash
# Small model (recommended for getting started)
ollama pull tinydolphin

# For embeddings
ollama pull all-minilm
```

### Step 3: Verify Installation

```python
from smartgenai.ragWrapper import ragWrapper

rag = ragWrapper()
print("SmartGenAI installed successfully!")
```

---

## Your First RAG Application

Let's build a simple question-answering system that reads a document and answers questions about it.

### Step 1: Create the Script

Create a file called `my_first_rag.py`:

```python
from smartgenai.ragWrapper import ragWrapper
from smartgenai.framework.sets.chunks import chunks as Chunks
import json

def main():
    # Initialize the RAG wrapper
    rag = ragWrapper()
    
    # Configuration for document reading (PyMuPDF)
    doc_config = json.dumps({
        "pclass": "smartgenai.connectors.documents.simplePdf"
    })
    
    # Configuration for chunking
    chunk_config = json.dumps({
        "method": "character",
        "separator": ".",
        "size": 500,
        "overlap": 50
    })
    
    # Configuration for embeddings (Sentence Transformers)
    embedding_config = json.dumps({
        "pclass": "smartgenai.connectors.embeddings.sentenceTransformer"
    })
    
    # Configuration for FAISS (in-memory)
    faiss_config = json.dumps({
        "pclass": "smartgenai.connectors.vstore.faiss"
    })
    
    # Configuration for Ollama LLM
    llm_config = json.dumps({
        "pclass": "smartgenai.connectors.llms.ollama",
        "url": "http://localhost:11434/api",
        "model": "tinydolphin",
        "temperature": 0.7,
        "contextwindow": 2048
    })
    
    # Step 1: Read the document
    print("📄 Reading document...")
    document = rag.read("your_document.pdf", doc_config)
    print(f"   Document loaded: {len(document.content)} characters")
    
    # Step 2: Chunk the document
    print("✂️ Chunking document...")
    chunks = rag.chunk(document, chunk_config)
    print(f"   Created {chunks.size} chunks")
    
    # Step 3: Create embeddings
    print("📐 Creating embeddings...")
    embeddings = rag.createEmbeddings(chunks, embedding_config)
    
    # Step 4: Store in FAISS (in-memory)
    print("🗄️ Storing in vector database...")
    rag.storeEmbeddings(embeddings.jsonContent, faiss_config)
    
    # Step 5: Ask a question
    question = "What is the main topic of this document?"
    print(f"\n❓ Question: {question}")
    
    # Create embeddings for the question
    question_chunks = Chunks()
    question_chunks.add(question)
    question_embeddings = rag.createEmbeddings(question_chunks, embedding_config)
    
    # Step 6: Find similar content
    print("🔍 Searching for relevant content...")
    similar = rag.memSimilaritySearch(
        k=3,
        textEmbeddings=question_embeddings.jsonContent,
        listEmbeddings=embeddings.jsonContent,
        jsonConfig=faiss_config
    )
    
    # Step 7: Build the RAG prompt
    prompt = rag.buildPrompt(question, similar)
    
    # Step 8: Get LLM response
    print("🤖 Getting LLM response...")
    response, outputs = rag.prompt(llm_config, prompt)
    
    print(f"\n💬 Answer: {response}")
    
    # Print trace information
    print("\n📊 Trace Summary:")
    print(rag.trace.getFullJSON())

if __name__ == "__main__":
    main()
```

### Step 2: Run Your Application

```bash
python my_first_rag.py
```

---

## Understanding the Components

### The RAG Wrapper

The `ragWrapper` class is the main entry point for all RAG operations:

```python
from smartgenai.ragWrapper import ragWrapper

rag = ragWrapper()
```

### Document Processing

SmartGenAI supports multiple document formats:

```python
# PDF with PyMuPDF
pdf_config = json.dumps({
    "pclass": "smartgenai.connectors.documents.simplePdf",
    "fromPage": 1,      # Optional: start page
    "toPage": 10,       # Optional: end page
    "heightToRemove": 0 # Optional: remove header/footer
})

# HTML from URL
html_config = json.dumps({
    "pclass": "smartgenai.connectors.documents.html"
})

# Use the read method
document = rag.read("https://example.com", html_config)
```

### Chunking

Two chunking methods are available:

```python
# Character-based chunking
char_chunk_config = json.dumps({
    "method": "character",
    "separator": ".",
    "size": 500,
    "overlap": 50
})

# Semantic chunking (uses embeddings to find natural breaks)
sem_chunk_config = json.dumps({
    "method": "semantic"
})

chunks = rag.chunk(document, char_chunk_config)
```

### Embeddings

Create vector representations of text:

```python
# Using Sentence Transformers (local)
st_config = json.dumps({
    "pclass": "smartgenai.connectors.embeddings.sentenceTransformer"
})

# Using Ollama (local)
ollama_emb_config = json.dumps({
    "pclass": "smartgenai.connectors.embeddings.ollama",
    "url": "http://localhost:11434/api",
    "model": "all-minilm"
})

embeddings = rag.createEmbeddings(chunks, st_config)
```

### Vector Stores

Store and search embeddings:

```python
# FAISS - Persistent storage
faiss_persist_config = json.dumps({
    "pclass": "smartgenai.connectors.vstore.faiss",
    "filepath": "./vstore",
    "name": "my_index"
})

# FAISS - In-memory
faiss_mem_config = json.dumps({
    "pclass": "smartgenai.connectors.vstore.faiss"
})

# ChromaDB
chroma_config = json.dumps({
    "pclass": "smartgenai.connectors.vstore.ChromaDB",
    "host": "localhost",
    "port": 8000,
    "collection": "my_docs"
})
```

### LLMs

Send prompts to language models:

```python
# Ollama (local)
ollama_config = json.dumps({
    "pclass": "smartgenai.connectors.llms.ollama",
    "url": "http://localhost:11434/api",
    "model": "tinydolphin",
    "temperature": 0.7,
    "contextwindow": 2048
})

# AWS Bedrock Claude
claude_config = json.dumps({
    "pclass": "smartgenai.connectors.llms.AWSModels.Claude",
    "region": "us-east-1",
    "model": "anthropic.claude-3-sonnet-20240229-v1:0",
    "temperature": 0.7,
    "max_tokens": 1024
})

response, outputs = rag.prompt(ollama_config, "Hello, how are you?")
```

---

## Next Steps

Now that you understand the basics, explore these advanced topics:

1. **[Configuration Guide](configuration.md)** - Detailed configuration options
2. **[Examples](examples/)** - More code examples
3. **[API Reference](api-reference.md)** - Complete API documentation
4. **[Best Practices](best-practices.md)** - Tips for production use

---

## Troubleshooting

### Common Issues

**1. Ollama not responding**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags
```

**2. Model not found**
```bash
# List installed models
ollama list

# Pull the model
ollama pull tinydolphin
```

**3. Memory issues with large documents**
- Use character chunking with smaller chunk sizes
- Process documents in batches
- Use persistent FAISS storage instead of in-memory

**4. Import errors**
```bash
# Reinstall the package
pip install --force-reinstall smartgenai
```

---

For more help, open an issue on [GitHub](https://github.com/datacorner/smartgenai/issues).

