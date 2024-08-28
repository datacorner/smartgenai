__author__ = "datacorner community"
__email__ = "admin@datacorner.fr"
__license__ = "MIT"

import logging
from enum import IntEnum
    
# Diverse Consts
NULLSTRING = ""
ENCODING = "utf-8"

# Logger configuration
TRACE_DEFAULT_LEVEL = logging.DEBUG
TRACE_DEFAULT_FORMAT = "%(asctime)s|%(name)s|%(levelname)s|%(message)s"
TRACE_FILENAME = "rag-framework.log"
TRACE_MAXBYTES = 10000
TRACE_LOGGER = "RAGFMK"
TRACE_MSG_LENGTH = 200
RAGCLI_LOGFILE_ENV = "RAGFMK_LOGFILE"
FAISS_DEFAULT_NAME = "faiss"
FAISS_DEFAULT_STORE = "./vstore"
LOGERROR = "ERROR"
LOGINFO = "INFO"
LOGDEBUG = "DEBUG"
ACTIVE_LOG_DEBUG = True

# LLM stuff
SEMCHUNK_EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
EMBEDDING_MODEL = "paraphrase-mpnet-base-v2"
OLLAMA_LOCAL_URL = "http://localhost:11434/api"
OLLAMA_DEFAULT_LLM = "tinydolphin"
OLLAMA_DEFAULT_EMB = "all-minilm"
OLLAMA_DEFAULT_CTXWIN = 2048
LLM_DEFAULT_TEMPERATURE = 0.9
SM_DEFAULT_NEAREST = 3
CHKS_DEFAULT_SIZE = 500
CHKS_DEFAULT_OVERLAP = 50
CHKS_DEFAULT_SEP = "."

# JSON "tags" for chunks & embeddings
JST_CHUNKS = "chunks"
JST_TEXT = "text"
JST_EMBEDDINGS = "embedding"
JST_NEAREST = "nearest"

# Prompts
TPL_QUESTION = "question"
TPL_NEAREST = "nearestItems"
PROMPT_RAG_JINJA_TEMPLATE = "Question: {{question}}\n \
    Please answer the question based on the informations listed below: \n \
    {%- for item in nearestItems.items %} \
    Item: \n \
    {{ item }} \n \
    {% endfor %}"

# Output status
OUT_ERROR = "ERROR"
OUT_SUCCESS = "SUCCESS"

# Llamaparse
LLAMAPARSE_API_URL = "https://api.cloud.llamaindex.ai/api/parsing"
LLAMAPARSE_API_WAITSEC = 2
LLAMAPARSE_ITERATION_MAX = 20
LLAMAINDEX_API_KEY = "LLAMAINDEX_API_KEY"
READER_VALPYPDF = "pymupdf"
READER_VALLLAMAPARSE = "llamaparse"

# Hugging Face
HUGGINGFACE_API_KEY = "HUGGINGFACE_API_KEY"
HUGGING_FACE_MODELS_URL = "https://api-inference.huggingface.co/models"
HUGGING_FACE_DEFAULT_CTXWIN = 2048
HF_API_WAITSEC = 2
HF_ITERATION_MAX = 20

# Chroma DB
CDB_DEFAULT_HOST = "localhost"
CDB_DEFAULT_PORT = 8000
CDB_DEFAULT_COLLECTION = "default"
CDB_DEFAULT_EMBEDDINGSMODEL_ST = "all-MiniLM-L6-v2"