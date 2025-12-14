# API Reference

Complete API documentation for SmartGenAI.

## Table of Contents

1. [ragWrapper Class](#ragwrapper-class)
2. [Document Classes](#document-classes)
3. [Chunk Classes](#chunk-classes)
4. [Embedding Classes](#embedding-classes)
5. [Vector Store Classes](#vector-store-classes)
6. [LLM Classes](#llm-classes)
7. [Utility Classes](#utility-classes)

---

## ragWrapper Class

The main entry point for all RAG operations.

```python
from smartgenai.ragWrapper import ragWrapper
```

### Constructor

```python
rag = ragWrapper()
```

Creates a new ragWrapper instance with tracing enabled.

### Properties

#### trace

```python
@property
def trace(self) -> trace
```

Returns the trace object for logging and debugging.

**Example:**
```python
print(rag.trace.getFullJSON())
```

### Methods

#### read()

```python
def read(self, iddocument: str, jsonConfig: str) -> documentBaseObject
```

Reads a document (PDF, HTML, etc.) and converts it to text.

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `iddocument` | str | File path or URL |
| `jsonConfig` | str | JSON configuration for document reader |

**Returns:** `documentBaseObject` with content loaded

**Example:**
```python
config = json.dumps({
    "pclass": "smartgenai.connectors.documents.simplePdf"
})
document = rag.read("my_file.pdf", config)
print(document.content)
```

---

#### readTXT()

```python
def readTXT(self, txtfile: str) -> txt
```

Reads a plain text file.

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `txtfile` | str | Path to text file |

**Returns:** `txt` document object

**Example:**
```python
document = rag.readTXT("my_file.txt")
```

---

#### chunk()

```python
def chunk(self, document: documentBaseObject, jsonConfig: str) -> chunks
```

Chunks a document into smaller pieces.

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `document` | documentBaseObject | Document to chunk |
| `jsonConfig` | str | JSON chunking configuration |

**Returns:** `chunks` object containing the chunks

**Example:**
```python
config = json.dumps({
    "method": "character",
    "separator": ".",
    "size": 500,
    "overlap": 50
})
chunks = rag.chunk(document, config)
print(f"Created {chunks.size} chunks")
```

---

#### createEmbeddings()

```python
def createEmbeddings(self, cks: chunks, jsonConfig: str) -> embeddingsBaseObject
```

Creates vector embeddings for chunks.

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `cks` | chunks | Chunks to embed |
| `jsonConfig` | str | JSON embedding configuration |

**Returns:** `embeddingsBaseObject` with vectors

**Example:**
```python
config = json.dumps({
    "pclass": "smartgenai.connectors.embeddings.sentenceTransformer"
})
embeddings = rag.createEmbeddings(chunks, config)
```

---

#### storeEmbeddings()

```python
def storeEmbeddings(self, embds: str, jsonConfig: str) -> bool
```

Stores embeddings in a vector store.

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `embds` | str | JSON embeddings content |
| `jsonConfig` | str | JSON vector store configuration |

**Returns:** `True` if successful

**Example:**
```python
config = json.dumps({
    "pclass": "smartgenai.connectors.vstore.faiss",
    "filepath": "./vstore",
    "name": "my_index"
})
rag.storeEmbeddings(embeddings.jsonContent, config)
```

---

#### similaritySearch()

```python
def similaritySearch(self, k: int, embds: str, jsonConfig: str) -> nearest
```

Searches for similar items in a stored index.

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `k` | int | Number of nearest neighbors |
| `embds` | str | JSON embeddings for query |
| `jsonConfig` | str | JSON vector store configuration |

**Returns:** `nearest` object with results

**Example:**
```python
similar = rag.similaritySearch(3, query_embeddings.jsonContent, faiss_config)
for item in similar.items:
    print(item)
```

---

#### memSimilaritySearch()

```python
def memSimilaritySearch(
    self, 
    k: int, 
    textEmbeddings: str, 
    listEmbeddings: str, 
    jsonConfig: str
) -> nearest
```

Searches for similar items in memory (without persistent storage).

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `k` | int | Number of nearest neighbors |
| `textEmbeddings` | str | Query embeddings JSON |
| `listEmbeddings` | str | Document embeddings JSON |
| `jsonConfig` | str | JSON configuration |

**Returns:** `nearest` object with results

---

#### similarityScore()

```python
def similarityScore(
    self, 
    text1: str, 
    text2: str, 
    vStoreJsonConfig: str, 
    embdsJsonConfig: str
) -> float
```

Calculates similarity between two texts.

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `text1` | str | First text |
| `text2` | str | Second text |
| `vStoreJsonConfig` | str | Vector store config |
| `embdsJsonConfig` | str | Embeddings config |

**Returns:** Similarity score (lower = more similar for L2 distance)

**Example:**
```python
score = rag.similarityScore(
    "My cat is red",
    "My cat is orange",
    faiss_config,
    embedding_config
)
print(f"Similarity: {score}")
```

---

#### buildPrompt()

```python
def buildPrompt(self, question: str, nr: nearest) -> str
```

Builds a RAG prompt with question and context.

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `question` | str | User's question |
| `nr` | nearest | Similar items for context |

**Returns:** Formatted prompt string

**Example:**
```python
prompt = rag.buildPrompt("What is the main topic?", similar_items)
```

---

#### prompt()

```python
def prompt(self, jsonLLMConfig: str, prompt: str = "") -> Tuple[str, dict]
```

Sends a prompt to an LLM.

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `jsonLLMConfig` | str | JSON LLM configuration |
| `prompt` | str | Prompt to send |

**Returns:** Tuple of (response text, outputs dict)

**Example:**
```python
response, outputs = rag.prompt(llm_config, "What is AI?")
print(response)
```

---

#### addMilestone()

```python
def addMilestone(self, name: str, description: str, *others)
```

Adds a milestone to the trace.

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | str | Milestone name |
| `description` | str | Description |
| `*others` | any | Additional data |

---

## Document Classes

### documentBaseObject

Base class for all document types.

```python
from smartgenai.framework.documents.documentBaseObject import documentBaseObject
```

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | str | Document identifier (filename/URL) |
| `content` | str | Document text content |
| `parameters` | dict | Configuration parameters |
| `trace` | trace | Trace object |

#### Methods

| Method | Description |
|--------|-------------|
| `load()` | Load document content |
| `save(filename)` | Save content to file |
| `characterChunk(separator, size, overlap)` | Character chunking |
| `semanticChunk()` | Semantic chunking |

---

## Chunk Classes

### chunks

Manages a collection of text chunks.

```python
from smartgenai.framework.sets.chunks import chunks
```

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `items` | list | List of chunk strings |
| `size` | int | Number of chunks |
| `jsonContent` | str | JSON representation |

#### Methods

| Method | Description |
|--------|-------------|
| `add(chunk)` | Add a chunk |
| `save(filename)` | Save to JSON file |
| `load(filename)` | Load from JSON file |
| `setLangchainDocument(lcDoc)` | Import from LangChain |

**Example:**
```python
cks = chunks()
cks.add("First chunk of text")
cks.add("Second chunk of text")
print(f"Total chunks: {cks.size}")
```

---

## Embedding Classes

### embeddingsBaseObject

Base class for embeddings.

```python
from smartgenai.framework.embeddings.embeddingsBaseObject import embeddingsBaseObject
```

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `items` | dict | Embeddings dictionary |
| `content` | dict | Embeddings content |
| `jsonContent` | str | JSON representation |

#### Methods

| Method | Description |
|--------|-------------|
| `create(chunks)` | Create embeddings for chunks |

---

## Vector Store Classes

### vstoreBaseObject

Base class for vector stores.

```python
from smartgenai.framework.vstore.vstoreBaseObject import vstoreBaseObject
```

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `ready` | bool | Whether store is ready |

#### Methods

| Method | Description |
|--------|-------------|
| `init()` | Initialize the store |
| `add(embeddings)` | Add embeddings |
| `getNearest(query, k)` | Get k nearest neighbors |
| `save()` | Persist the store |
| `load()` | Load from persistence |

---

## LLM Classes

### LLMBaseObject

Base class for LLM connectors.

```python
from smartgenai.framework.llms.LLMBaseObject import LLMBaseObject
```

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `parameters` | dict | Input parameters |
| `outputs` | dict | LLM outputs |
| `jsonOutputs` | dict | JSON outputs |

#### Methods

| Method | Description |
|--------|-------------|
| `init()` | Initialize the LLM |
| `prompt(text)` | Send prompt and get response |
| `getParameterValue(name, default)` | Get a parameter |
| `setJSONParameters(json)` | Set parameters from JSON |

---

## Utility Classes

### nearest

Stores similarity search results.

```python
from smartgenai.framework.sets.nearest import nearest
```

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `items` | list | List of similar items |
| `distances` | list | Distance scores |
| `metadatas` | list | Metadata for items |
| `ids` | list | Item identifiers |
| `size` | int | Number of results |
| `jsonContent` | str | JSON representation |

#### Methods

| Method | Description |
|--------|-------------|
| `add(item)` | Add an item |
| `save(filename)` | Save to file |
| `load(filename)` | Load from file |
| `rerank(text)` | Re-rank results |

---

### prompt

Manages prompt templates.

```python
from smartgenai.framework.sets.prompt import prompt
```

#### Constructor

```python
p = prompt(question, similarItems)
```

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `question` | str | The question |
| `similarItems` | nearest | Context items |
| `template` | str | Jinja2 template |

#### Methods

| Method | Description |
|--------|-------------|
| `build()` | Build the final prompt |
| `loadTemplate(filename)` | Load template from file |

**Default Template:**
```
Question: {{question}}
Please answer the question based on the informations listed below:
{%- for item in nearestItems.items %}
Item:
{{ item }}
{% endfor %}
```

---

### trace

Logging and tracing utility.

```python
from smartgenai.utils.trace import trace
```

#### Methods

| Method | Description |
|--------|-------------|
| `start()` | Start tracing |
| `add(name, description, *data)` | Add milestone |
| `addlog(level, message)` | Add log entry |
| `getFullJSON()` | Get full trace as JSON |

---

## Factory Classes

SmartGenAI uses factory classes for dynamic instantiation:

- `LLMFactory.getInstance(jsonConfig)` - Create LLM instance
- `embeddingsFactory.getInstance(jsonConfig)` - Create embeddings instance
- `vstoreFactory.getInstance(jsonConfig)` - Create vector store instance
- `documentFactory.getInstance(jsonConfig)` - Create document reader instance

**Example:**
```python
from smartgenai.framework.llms.LLMFactory import LLMFactory

llm = LLMFactory.getInstance(json.dumps({
    "pclass": "smartgenai.connectors.llms.ollama",
    "url": "http://localhost:11434/api",
    "model": "tinydolphin"
}))
response = llm.prompt("Hello!")
```

---

## Error Handling

All methods log errors via the trace system:

```python
try:
    response, _ = rag.prompt(config, "Hello")
except Exception as e:
    print(f"Error: {e}")
    print(rag.trace.getFullJSON())  # Check trace for details
```

---

For examples, see the [Examples](examples/) directory.

