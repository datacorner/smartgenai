# Description
Lightweight RAG Framework: Simple and Scalable Framework with Efficient Embeddings. Leverage: FAISS, ChromaDB, and Ollama 
* LLMs
* Vector Database or Similarity Search engine
* Embeddings
* Chunking techniques
* Data Collection  
Each of these objects are managed by the framework and provides the same IN/OUT to enable interoperability and facilitates changes (as this area is moving super fast !).  

This project can totally runs locally (meaning on a single laptop without GPUs) and leverages:
* **Ollama** (https://ollama.com/) for running locally LLMs
* **AWS Bedrock** LLMs provided through AWS bedrock
* **Sentence-transformers** (https://pypi.org/project/sentence-transformers/) for the embeddings management
* potentially **llamaParse** from llamaindex (https://docs.llamaindex.ai/) can be used.
* **langchain** (https://www.langchain.com/) for chunking (semantic or character)
* Meta **FAISS** for similarity search (also enable storing and loading indexes)
* **ChromaDB** for storing and searching into the vector store
* **PyMuPDF** by default to read and convert PDF content

# Framework description
Several objects are provided to manage the main RAG features and characteristics:
* **rag**: is the main interface for managing all needed request.
* **IDocument**: manages the document reading and loading (pdf or direct content)
* **IChunks**: manages the chunks list
* **IEmbeddings**: Manages the vector and data embeddings
* **INearest**: Manages the k nearest neighbors retreived by the similarity search engine
* **IPrompt**: Manages Prompt templating and simple prompt

LLMs supported:
* Ollama
* AWS Claude
* Hugging Face

Document reading methods are supported:
* PDF via PyMuPDF
* PDF via Llamaparse
* HTML stream

Chunking methods are supported:
* Character chunkink (langchain)
* Semantic chunking (langchain)

Vectors stores are currently supported:
* FAISS: search + load and store indexes
* ChromaDB

Embeddings methods are supported:
* via HF Sentence Transformer (the model can be changed)
* via Ollama Embeddings Models (the model can be changed)

# Installation
## Python Framework installation
1) Download and Install Python, 
2)  install ragfmk by using pip
```
pip install [--force-reinstall] wheel file (see the /dist folder)
```

## Environment variables
Some environment variables may need to be set:  
* If you need to use llamaParse, the llamaindex token (generated on the web site: https://cloud.llamaindex.ai/login) must be filled out to **LLAMAINDEX_API_KEY** 
* If you need to use hugging face, the hugging face env. token must be filled out into **HUGGINGFACE_API_KEY** 
* For AWS please set the following variables:
    * **AWS_ACCESS_KEY_ID**=...
    * **AWS_SECRET_ACCESS_KEY**=...

## Installation/Preparation for Ollama
1) Install ollama (https://ollama.com/)
2) Run ollama in the command line and pull at least one model. *tinydolphin* for example is a good choice as it is a very small model and can then run on a simple laptop without a big latency.

# Example of use
See the tests folder.