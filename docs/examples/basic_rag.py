"""
Basic RAG Example with SmartGenAI
=================================

This example demonstrates a complete RAG pipeline:
1. Read a PDF document
2. Chunk the document
3. Create embeddings
4. Store in FAISS
5. Search for similar content
6. Build a prompt with context
7. Get an answer from the LLM

Requirements:
- Ollama running locally with 'tinydolphin' model
- A PDF file to process
"""

from smartgenai.ragWrapper import ragWrapper
from smartgenai.framework.sets.chunks import chunks as Chunks
import json
import os

# Configuration constants
OLLAMA_URL = "http://localhost:11434/api"
LLM_MODEL = "tinydolphin"
EMBEDDING_MODEL = "paraphrase-mpnet-base-v2"

def get_configs():
    """Return all configuration objects."""
    
    # Document reader configuration
    doc_config = json.dumps({
        "pclass": "smartgenai.connectors.documents.simplePdf"
    })
    
    # Chunking configuration
    chunk_config = json.dumps({
        "method": "character",
        "separator": ".",
        "size": 500,
        "overlap": 50
    })
    
    # Embedding configuration
    embedding_config = json.dumps({
        "pclass": "smartgenai.connectors.embeddings.sentenceTransformer",
        "model": EMBEDDING_MODEL
    })
    
    # FAISS configuration (in-memory)
    faiss_config = json.dumps({
        "pclass": "smartgenai.connectors.vstore.faiss"
    })
    
    # LLM configuration
    llm_config = json.dumps({
        "pclass": "smartgenai.connectors.llms.ollama",
        "url": OLLAMA_URL,
        "model": LLM_MODEL,
        "temperature": 0.7,
        "contextwindow": 2048
    })
    
    return doc_config, chunk_config, embedding_config, faiss_config, llm_config


def process_document(rag, pdf_path, doc_config, chunk_config, embedding_config):
    """Process a PDF document and return embeddings."""
    
    print(f"📄 Reading document: {pdf_path}")
    document = rag.read(pdf_path, doc_config)
    print(f"   Loaded {len(document.content)} characters")
    
    print("✂️ Chunking document...")
    chunks = rag.chunk(document, chunk_config)
    print(f"   Created {chunks.size} chunks")
    
    print("📐 Creating embeddings...")
    embeddings = rag.createEmbeddings(chunks, embedding_config)
    print("   Embeddings created successfully")
    
    return embeddings


def ask_question(rag, question, embeddings, configs):
    """Ask a question and get an answer using RAG."""
    
    embedding_config, faiss_config, llm_config = configs
    
    print(f"\n❓ Question: {question}")
    
    # Create embeddings for the question
    question_chunks = Chunks()
    question_chunks.add(question)
    question_embeddings = rag.createEmbeddings(question_chunks, embedding_config)
    
    # Search for similar content
    print("🔍 Searching for relevant content...")
    similar = rag.memSimilaritySearch(
        k=3,
        textEmbeddings=question_embeddings.jsonContent,
        listEmbeddings=embeddings.jsonContent,
        jsonConfig=faiss_config
    )
    
    print(f"   Found {similar.size} relevant chunks")
    
    # Build the RAG prompt
    prompt = rag.buildPrompt(question, similar)
    
    # Get LLM response
    print("🤖 Getting LLM response...")
    response, outputs = rag.prompt(llm_config, prompt)
    
    return response, similar


def main():
    """Main function to run the RAG example."""
    
    # Check for PDF file
    pdf_path = "data/sample.pdf"  # Change this to your PDF file
    if not os.path.exists(pdf_path):
        print(f"⚠️ Please provide a PDF file at: {pdf_path}")
        print("   Or modify the pdf_path variable in this script.")
        return
    
    # Initialize
    rag = ragWrapper()
    doc_config, chunk_config, embedding_config, faiss_config, llm_config = get_configs()
    
    # Process document
    embeddings = process_document(
        rag, pdf_path, doc_config, chunk_config, embedding_config
    )
    
    # Interactive Q&A loop
    print("\n" + "="*50)
    print("Document processed! You can now ask questions.")
    print("Type 'quit' to exit.")
    print("="*50)
    
    while True:
        question = input("\nYour question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not question:
            continue
        
        response, similar = ask_question(
            rag, question, embeddings,
            (embedding_config, faiss_config, llm_config)
        )
        
        print(f"\n💬 Answer: {response}")
        
        # Optionally show sources
        show_sources = input("\nShow sources? (y/n): ").strip().lower()
        if show_sources == 'y':
            print("\n📚 Sources:")
            for i, item in enumerate(similar.items, 1):
                print(f"\n--- Source {i} ---")
                print(item[:200] + "..." if len(item) > 200 else item)


if __name__ == "__main__":
    main()

