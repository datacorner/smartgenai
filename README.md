<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" alt="Python 3.10+"/>
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License"/>
  <img src="https://img.shields.io/badge/Status-Alpha-orange" alt="Development Status"/>
</p>

# 🧠 SmartGenAI

**Lightweight RAG Framework**: A simple and scalable framework with efficient embeddings for building Retrieval-Augmented Generation (RAG) applications.

SmartGenAI provides a unified interface for managing all components of a RAG pipeline:
- 🤖 **LLMs** (Large Language Models)
- 🗄️ **Vector Databases** / Similarity Search Engines
- 📐 **Embeddings**
- ✂️ **Chunking Techniques**
- 📄 **Document Processing**

Each component is managed by the framework with consistent interfaces, enabling easy interoperability and facilitating technology changes as the AI landscape evolves rapidly.

---

## ✨ Features

### LLM Support
| Provider | Models | Notes |
|----------|--------|-------|
| **Ollama** | Any Ollama model (tinydolphin, llama2, mistral, etc.) | Local execution, no GPU required |
| **AWS Bedrock** | Claude, Mistral, Titan | Cloud-based, requires AWS credentials |
| **Hugging Face** | Any HF Inference API model | Cloud-based, requires HF token |

### Document Processing
| Format | Method | Description |
|--------|--------|-------------|
| PDF | PyMuPDF | Fast, local PDF parsing |
| PDF | LlamaParse | Advanced parsing via LlamaIndex API |
| HTML | BeautifulSoup | Web page content extraction |
| TXT | Native | Plain text file reading |

### Chunking Methods
- **Character Chunking** (via LangChain) - Split by character count with overlap
- **Semantic Chunking** (via LangChain) - Split by meaning using embeddings

### Embeddings
| Provider | Models | Notes |
|----------|--------|-------|
| **Sentence Transformers** | paraphrase-mpnet-base-v2, all-MiniLM-L6-v2, etc. | Local execution |
| **Ollama** | all-minilm, nomic-embed-text, etc. | Local execution |

### Vector Stores
| Store | Features |
|-------|----------|
| **FAISS** | In-memory or persistent index, fast similarity search |
| **ChromaDB** | Persistent storage, metadata support, server mode |

### Additional Features
- 📊 **Re-ranking** support via FlashRank
- 📝 **Jinja2 prompt templates** for RAG queries
- 🔍 **Detailed tracing and logging**
- 🌐 **REST API** (Flask-based)

---

## 🚀 Installation

### Option 1: Install from wheel (Recommended)

```bash
pip install smartgenai-0.1.0.2-py3-none-any.whl
```

### Option 2: Install from source

```bash
git clone https://github.com/datacorner/smartgenai.git
cd smartgenai
pip install -e .
```

### Option 3: Install dependencies manually

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### Environment Variables

Set the following environment variables based on the services you plan to use:

| Variable | Required For | Description |
|----------|--------------|-------------|
| `LLAMAINDEX_API_KEY` | LlamaParse | API key from [LlamaIndex Cloud](https://cloud.llamaindex.ai/) |
| `HUGGINGFACE_API_KEY` | Hugging Face | API token from [Hugging Face](https://huggingface.co/settings/tokens) |
| `AWS_ACCESS_KEY_ID` | AWS Bedrock | AWS access key ID |
| `AWS_SECRET_ACCESS_KEY` | AWS Bedrock | AWS secret access key |

### Ollama Setup (for local LLM execution)

1. Install Ollama from [ollama.com](https://ollama.com/)
2. Pull a model:
```bash
ollama pull tinydolphin    # Small model, good for laptops
ollama pull llama2         # More capable model
ollama pull mistral        # Alternative model
```
3. (Optional) Pull an embedding model:
```bash
ollama pull all-minilm     # For embeddings
ollama pull nomic-embed-text
```

### ChromaDB Setup (optional)

```bash
# Install ChromaDB
pip install chromadb

# Start the server
chroma run --host localhost --port 8000 --path /path/to/chromadb
```

---

## 📖 Quick Start

### Basic RAG Pipeline

```python
from smartgenai.ragWrapper import ragWrapper
import json

# Initialize the RAG wrapper
rag = ragWrapper()

# 1. Read a PDF document
doc_config = json.dumps({
    "pclass": "smartgenai.connectors.documents.simplePdf"
})
document = rag.read("data/my_document.pdf", doc_config)

# 2. Chunk the document
chunk_config = json.dumps({
    "method": "character",
    "separator": ".",
    "size": 500,
    "overlap": 50
})
chunks = rag.chunk(document, chunk_config)

# 3. Create embeddings
embedding_config = json.dumps({
    "pclass": "smartgenai.connectors.embeddings.sentenceTransformer"
})
embeddings = rag.createEmbeddings(chunks, embedding_config)

# 4. Store embeddings in FAISS
faiss_config = json.dumps({
    "pclass": "smartgenai.connectors.vstore.faiss",
    "filepath": "./vstore",
    "name": "my_index"
})
rag.storeEmbeddings(embeddings.jsonContent, faiss_config)

# 5. Create embeddings for a question
from smartgenai.framework.sets.chunks import chunks as Chunks
question = "What is the main topic of this document?"
question_chunks = Chunks()
question_chunks.add(question)
question_embeddings = rag.createEmbeddings(question_chunks, embedding_config)

# 6. Find similar content
similar = rag.similaritySearch(3, question_embeddings.jsonContent, faiss_config)

# 7. Build the RAG prompt
prompt = rag.buildPrompt(question, similar)

# 8. Get LLM response
llm_config = json.dumps({
    "pclass": "smartgenai.connectors.llms.ollama",
    "url": "http://localhost:11434/api",
    "model": "tinydolphin",
    "temperature": 0.7,
    "contextwindow": 2048
})
response, outputs = rag.prompt(llm_config, prompt)
print(response)
```

### Simple LLM Prompt (without RAG)

```python
from smartgenai.ragWrapper import ragWrapper
import json

rag = ragWrapper()

# Configure Ollama
llm_config = json.dumps({
    "pclass": "smartgenai.connectors.llms.ollama",
    "url": "http://localhost:11434/api",
    "model": "tinydolphin",
    "temperature": 0.9,
    "contextwindow": 2048
})

# Send a prompt
response, outputs = rag.prompt(llm_config, "What is machine learning?")
print(response)
```

### Using AWS Bedrock (Claude)

```python
from smartgenai.ragWrapper import ragWrapper
import json

rag = ragWrapper()

llm_config = json.dumps({
    "pclass": "smartgenai.connectors.llms.AWSModels.Claude",
    "region": "us-east-1",
    "model": "anthropic.claude-3-sonnet-20240229-v1:0",
    "temperature": 0.7,
    "max_tokens": 1024
})

response, outputs = rag.prompt(llm_config, "Explain quantum computing in simple terms.")
print(response)
```

---

## 🔧 Configuration Files

SmartGenAI uses JSON configuration files to specify component settings. Here are example configurations:

### Ollama LLM
```json
{
    "pclass": "smartgenai.connectors.llms.ollama",
    "url": "http://localhost:11434/api",
    "model": "tinydolphin",
    "temperature": 0.9,
    "contextwindow": 2048
}
```

### AWS Claude
```json
{
    "pclass": "smartgenai.connectors.llms.AWSModels.Claude",
    "region": "us-east-1",
    "model": "anthropic.claude-3-sonnet-20240229-v1:0",
    "temperature": 0.7,
    "max_tokens": 1024
}
```

### Hugging Face
```json
{
    "pclass": "smartgenai.connectors.llms.huggingFace",
    "model": "mistralai/Mistral-7B-Instruct-v0.1"
}
```

### Sentence Transformer Embeddings
```json
{
    "pclass": "smartgenai.connectors.embeddings.sentenceTransformer",
    "model": "paraphrase-mpnet-base-v2"
}
```

### Ollama Embeddings
```json
{
    "pclass": "smartgenai.connectors.embeddings.ollama",
    "url": "http://localhost:11434/api",
    "model": "all-minilm"
}
```

### FAISS Vector Store (Persistent)
```json
{
    "pclass": "smartgenai.connectors.vstore.faiss",
    "filepath": "./vstore",
    "name": "my_index"
}
```

### FAISS Vector Store (In-Memory)
```json
{
    "pclass": "smartgenai.connectors.vstore.faiss"
}
```

### ChromaDB
```json
{
    "pclass": "smartgenai.connectors.vstore.ChromaDB",
    "host": "localhost",
    "port": 8000,
    "collection": "my_collection"
}
```

### PDF Document (PyMuPDF)
```json
{
    "pclass": "smartgenai.connectors.documents.simplePdf",
    "fromPage": 1,
    "toPage": 10,
    "heightToRemove": 50
}
```

### PDF Document (LlamaParse)
```json
{
    "pclass": "smartgenai.connectors.documents.llamaparsePdf"
}
```

### HTML Document
```json
{
    "pclass": "smartgenai.connectors.documents.html"
}
```

### Character Chunking
```json
{
    "method": "character",
    "separator": ".",
    "size": 500,
    "overlap": 50
}
```

### Semantic Chunking
```json
{
    "method": "semantic"
}
```

---

## 🏗️ Architecture

### Framework Components

```
smartgenai/
├── ragWrapper.py           # Main RAG interface
├── app.py                  # Flask REST API
├── connectors/             # Technology-specific implementations
│   ├── documents/          # PDF, HTML, TXT parsers
│   ├── embeddings/         # Sentence Transformers, Ollama
│   ├── llms/               # Ollama, AWS Bedrock, Hugging Face
│   └── vstore/             # FAISS, ChromaDB
├── framework/              # Base classes and factories
│   ├── documents/          # Document base object and factory
│   ├── embeddings/         # Embeddings base object and factory
│   ├── llms/               # LLM base object and factory
│   ├── vstore/             # Vector store base object and factory
│   └── sets/               # Chunks, Nearest, Prompt classes
├── interfaces/             # Abstract interfaces (ABC)
└── utils/                  # Constants and utilities
```

### Key Classes

| Class | Purpose |
|-------|---------|
| `ragWrapper` | Main entry point for all RAG operations |
| `IDocument` | Interface for document reading |
| `IChunks` | Interface for chunk management |
| `IEmbeddings` | Interface for embeddings |
| `INearest` | Interface for similarity search results |
| `IPrompt` | Interface for prompt building |
| `IVStore` | Interface for vector stores |

---

## 🌐 REST API

SmartGenAI includes a Flask-based REST API:

### Start the server

```bash
python -m smartgenai.app
```

### Endpoints

#### POST `/v1/prompt`

Send a prompt to the LLM.

**Request Body:**
```json
{
    "pclass": "smartgenai.connectors.llms.ollama",
    "url": "http://localhost:11434/api",
    "model": "tinydolphin",
    "temperature": 0.9,
    "contextwindow": 2048
}
```

**Response:**
```json
{
    "response": "LLM response text...",
    "trace": { ... },
    "output": { ... }
}
```

---

## 🧪 Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/rag_test.py

# Run with verbose output
python -m pytest tests/ -v
```

---

## 📦 Building from Source

```bash
# Install build dependencies
pip install build twine

# Build the package
python -m build

# The wheel file will be in dist/
ls dist/
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **datacorner community** - [benoit@datacorner.fr](mailto:benoit@datacorner.fr)

---

## 🙏 Acknowledgments

- [Ollama](https://ollama.com/) for local LLM execution
- [LangChain](https://www.langchain.com/) for chunking utilities
- [Sentence Transformers](https://www.sbert.net/) for embeddings
- [Meta FAISS](https://github.com/facebookresearch/faiss) for similarity search
- [ChromaDB](https://www.trychroma.com/) for vector storage
- [PyMuPDF](https://pymupdf.readthedocs.io/) for PDF processing
- [AWS Bedrock](https://aws.amazon.com/bedrock/) for cloud LLM access
