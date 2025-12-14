# Configuration Guide

SmartGenAI uses JSON configuration files to specify component settings. This guide covers all available configuration options.

## Table of Contents

1. [Configuration Overview](#configuration-overview)
2. [LLM Configurations](#llm-configurations)
3. [Embedding Configurations](#embedding-configurations)
4. [Vector Store Configurations](#vector-store-configurations)
5. [Document Reader Configurations](#document-reader-configurations)
6. [Chunking Configurations](#chunking-configurations)
7. [Environment Variables](#environment-variables)

---

## Configuration Overview

All SmartGenAI components use JSON configuration objects. The key parameter is `pclass`, which specifies the Python class to instantiate.

```python
import json

config = json.dumps({
    "pclass": "smartgenai.connectors.llms.ollama",
    "url": "http://localhost:11434/api",
    "model": "tinydolphin"
})
```

---

## LLM Configurations

### Ollama

Run LLMs locally using Ollama.

```json
{
    "pclass": "smartgenai.connectors.llms.ollama",
    "url": "http://localhost:11434/api",
    "model": "tinydolphin",
    "temperature": 0.9,
    "contextwindow": 2048
}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | string | - | Ollama API URL |
| `model` | string | - | Model name (e.g., tinydolphin, llama2, mistral) |
| `temperature` | float | 0.9 | Creativity (0.0 - 1.0) |
| `contextwindow` | int | 2048 | Context window size |

**Available Models:**
- `tinydolphin` - Very small, fast (1.1B parameters)
- `phi` - Small, good quality (2.7B parameters)
- `mistral` - Medium, excellent quality (7B parameters)
- `llama2` - Medium, Meta's LLaMA 2 (7B parameters)
- `codellama` - Optimized for code (7B parameters)

### AWS Bedrock - Claude

```json
{
    "pclass": "smartgenai.connectors.llms.AWSModels.Claude",
    "region": "us-east-1",
    "model": "anthropic.claude-3-sonnet-20240229-v1:0",
    "temperature": 0.7,
    "max_tokens": 1024,
    "aws_access_key_id": "YOUR_KEY",
    "aws_secret_access_key": "YOUR_SECRET"
}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `region` | string | - | AWS region |
| `model` | string | - | Model ID |
| `temperature` | float | 0.7 | Creativity (0.0 - 1.0) |
| `max_tokens` | int | 1024 | Maximum response tokens |
| `aws_access_key_id` | string | env var | AWS access key (optional if env var set) |
| `aws_secret_access_key` | string | env var | AWS secret key (optional if env var set) |

**Available Claude Models:**
- `anthropic.claude-3-sonnet-20240229-v1:0` - Balanced performance
- `anthropic.claude-3-haiku-20240307-v1:0` - Fast, cost-effective
- `anthropic.claude-3-opus-20240229-v1:0` - Most capable

### AWS Bedrock - Mistral

```json
{
    "pclass": "smartgenai.connectors.llms.AWSModels.Mistral",
    "region": "us-east-1",
    "model": "mistral.mistral-7b-instruct-v0:2",
    "temperature": 0.7,
    "max_tokens": 1024
}
```

### AWS Bedrock - Titan

```json
{
    "pclass": "smartgenai.connectors.llms.AWSModels.Titan",
    "region": "us-east-1",
    "model": "amazon.titan-text-lite-v1",
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

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | string | - | Hugging Face model ID |

**Note:** Requires `HUGGINGFACE_API_KEY` environment variable.

---

## Embedding Configurations

### Sentence Transformers

Local embeddings using Sentence Transformers.

```json
{
    "pclass": "smartgenai.connectors.embeddings.sentenceTransformer",
    "model": "paraphrase-mpnet-base-v2"
}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | string | paraphrase-mpnet-base-v2 | Model name |

**Recommended Models:**
- `paraphrase-mpnet-base-v2` - Good all-around (768 dimensions)
- `all-MiniLM-L6-v2` - Fast, smaller (384 dimensions)
- `all-mpnet-base-v2` - High quality (768 dimensions)
- `multi-qa-mpnet-base-dot-v1` - Optimized for Q&A

### Ollama Embeddings

Local embeddings using Ollama.

```json
{
    "pclass": "smartgenai.connectors.embeddings.ollama",
    "url": "http://localhost:11434/api",
    "model": "all-minilm"
}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | string | http://localhost:11434/api | Ollama API URL |
| `model` | string | all-minilm | Embedding model name |

**Available Models:**
- `all-minilm` - Fast, lightweight
- `nomic-embed-text` - High quality
- `mxbai-embed-large` - Large, high quality

---

## Vector Store Configurations

### FAISS - Persistent Storage

Store index on disk for persistence.

```json
{
    "pclass": "smartgenai.connectors.vstore.faiss",
    "filepath": "./vstore",
    "name": "my_index"
}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `filepath` | string | - | Directory to store index |
| `name` | string | - | Index name (creates .index and .data files) |

**Files Created:**
- `{filepath}/{name}.index` - FAISS index file
- `{filepath}/{name}.data` - Associated data (chunks)

### FAISS - In-Memory

Temporary storage for quick experiments.

```json
{
    "pclass": "smartgenai.connectors.vstore.faiss"
}
```

**Note:** Data is lost when the program exits.

### ChromaDB

Persistent vector database with metadata support.

```json
{
    "pclass": "smartgenai.connectors.vstore.ChromaDB",
    "host": "localhost",
    "port": 8000,
    "collection": "my_collection"
}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `host` | string | localhost | ChromaDB server host |
| `port` | int | 8000 | ChromaDB server port |
| `collection` | string | - | Collection name |

**Starting ChromaDB Server:**
```bash
chroma run --host localhost --port 8000 --path /path/to/data
```

---

## Document Reader Configurations

### PDF with PyMuPDF

Fast, local PDF parsing.

```json
{
    "pclass": "smartgenai.connectors.documents.simplePdf",
    "fromPage": 1,
    "toPage": 0,
    "heightToRemove": 0
}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `fromPage` | int | 0 | Start page (0 = first page) |
| `toPage` | int | 0 | End page (0 = last page) |
| `heightToRemove` | int | 0 | Pixels to remove from top/bottom (headers/footers) |

### PDF with LlamaParse

Advanced PDF parsing via LlamaIndex API.

```json
{
    "pclass": "smartgenai.connectors.documents.llamaparsePdf"
}
```

**Note:** Requires `LLAMAINDEX_API_KEY` environment variable.

**Features:**
- Better handling of complex layouts
- Table extraction
- OCR support

### HTML

Parse web pages using BeautifulSoup.

```json
{
    "pclass": "smartgenai.connectors.documents.html"
}
```

**Usage:**
```python
document = rag.read("https://example.com/page", html_config)
```

### Plain Text

Read text files directly.

```python
document = rag.readTXT("path/to/file.txt")
```

---

## Chunking Configurations

### Character-Based Chunking

Split text by character count with overlap.

```json
{
    "method": "character",
    "separator": ".",
    "size": 500,
    "overlap": 50
}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `method` | string | - | Must be "character" |
| `separator` | string | "." | Character to split on |
| `size` | int | 500 | Maximum chunk size |
| `overlap` | int | 50 | Overlap between chunks |

**Recommended Settings:**
- Small documents: `size: 200, overlap: 20`
- Medium documents: `size: 500, overlap: 50`
- Large documents: `size: 1000, overlap: 100`

### Semantic Chunking

Split text based on meaning using embeddings.

```json
{
    "method": "semantic"
}
```

**Features:**
- Automatically finds natural break points
- Preserves context better than character chunking
- Uses HuggingFace embeddings internally

**Note:** Slower than character chunking but produces better results.

---

## Environment Variables

### Required Variables

| Variable | Service | Description |
|----------|---------|-------------|
| `LLAMAINDEX_API_KEY` | LlamaParse | API key from cloud.llamaindex.ai |
| `HUGGINGFACE_API_KEY` | Hugging Face | API token from huggingface.co |
| `AWS_ACCESS_KEY_ID` | AWS Bedrock | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | AWS Bedrock | AWS secret key |

### Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `RAGFMK_LOGFILE` | rag-framework.log | Log file location |

### Setting Environment Variables

**Linux/macOS:**
```bash
export LLAMAINDEX_API_KEY="your-key-here"
export AWS_ACCESS_KEY_ID="your-key-here"
export AWS_SECRET_ACCESS_KEY="your-secret-here"
```

**Windows (PowerShell):**
```powershell
$env:LLAMAINDEX_API_KEY = "your-key-here"
$env:AWS_ACCESS_KEY_ID = "your-key-here"
$env:AWS_SECRET_ACCESS_KEY = "your-secret-here"
```

**In Python:**
```python
import os
os.environ["LLAMAINDEX_API_KEY"] = "your-key-here"
```

---

## Configuration Best Practices

### 1. Use Configuration Files

Store configurations in JSON files for reusability:

```python
def load_config(filename):
    with open(filename, "r") as f:
        return f.read()

llm_config = load_config("configs/ollama.json")
```

### 2. Environment-Specific Configurations

Create different configs for development and production:

```
configs/
├── dev/
│   ├── llm.json        # Uses Ollama locally
│   └── vstore.json     # In-memory FAISS
└── prod/
    ├── llm.json        # Uses AWS Bedrock
    └── vstore.json     # Persistent ChromaDB
```

### 3. Validate Configurations

Check that required parameters are present:

```python
import json

def validate_llm_config(config_str):
    config = json.loads(config_str)
    required = ["pclass", "model"]
    for key in required:
        if key not in config:
            raise ValueError(f"Missing required key: {key}")
    return True
```

### 4. Secure Credentials

Never commit credentials to version control:

```python
import os
import json

config = {
    "pclass": "smartgenai.connectors.llms.AWSModels.Claude",
    "region": "us-east-1",
    "model": "anthropic.claude-3-sonnet-20240229-v1:0",
    # Credentials from environment
    "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
    "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY")
}
```

---

For more examples, see the [Examples](examples/) directory.

