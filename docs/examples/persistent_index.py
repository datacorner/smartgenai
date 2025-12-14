"""
Persistent Index Example
========================

This example demonstrates how to:
1. Create a persistent FAISS index from documents
2. Load the index later for querying
3. Add new documents to an existing index

This is useful for:
- Building document search engines
- Creating knowledge bases
- Processing large document collections
"""

from smartgenai.ragWrapper import ragWrapper
from smartgenai.framework.sets.chunks import chunks as Chunks
import json
import os
import glob


# Configuration
INDEX_PATH = "./vstore"
INDEX_NAME = "my_knowledge_base"

# Configurations
EMBEDDING_CONFIG = json.dumps({
    "pclass": "smartgenai.connectors.embeddings.sentenceTransformer",
    "model": "paraphrase-mpnet-base-v2"
})

FAISS_CONFIG = json.dumps({
    "pclass": "smartgenai.connectors.vstore.faiss",
    "filepath": INDEX_PATH,
    "name": INDEX_NAME
})

LLM_CONFIG = json.dumps({
    "pclass": "smartgenai.connectors.llms.ollama",
    "url": "http://localhost:11434/api",
    "model": "tinydolphin",
    "temperature": 0.5,
    "contextwindow": 2048
})


def create_index(pdf_files: list[str]):
    """Create a persistent FAISS index from PDF files."""
    
    # Ensure index directory exists
    os.makedirs(INDEX_PATH, exist_ok=True)
    
    rag = ragWrapper()
    
    doc_config = json.dumps({
        "pclass": "smartgenai.connectors.documents.simplePdf"
    })
    
    chunk_config = json.dumps({
        "method": "character",
        "separator": ".",
        "size": 500,
        "overlap": 50
    })
    
    print("📚 Creating persistent index")
    print(f"   Path: {INDEX_PATH}/{INDEX_NAME}")
    print(f"   Documents: {len(pdf_files)}")
    
    all_embeddings = None
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\n[{i}/{len(pdf_files)}] Processing: {os.path.basename(pdf_file)}")
        
        # Read document
        document = rag.read(pdf_file, doc_config)
        print(f"   📄 Loaded {len(document.content)} characters")
        
        # Chunk
        chunks = rag.chunk(document, chunk_config)
        print(f"   ✂️ Created {chunks.size} chunks")
        
        # Create embeddings
        embeddings = rag.createEmbeddings(chunks, EMBEDDING_CONFIG)
        print(f"   📐 Created embeddings")
        
        # Store in FAISS
        rag.storeEmbeddings(embeddings.jsonContent, FAISS_CONFIG)
        print(f"   💾 Added to index")
    
    print(f"\n✅ Index created successfully!")
    print(f"   Files: {INDEX_PATH}/{INDEX_NAME}.index")
    print(f"          {INDEX_PATH}/{INDEX_NAME}.data")


def query_index(question: str, k: int = 3):
    """Query an existing persistent index."""
    
    # Check if index exists
    index_file = os.path.join(INDEX_PATH, f"{INDEX_NAME}.index")
    if not os.path.exists(index_file):
        print(f"❌ Index not found: {index_file}")
        print("   Run 'create_index' first.")
        return None
    
    rag = ragWrapper()
    
    print(f"🔍 Querying index: {INDEX_NAME}")
    print(f"   Question: {question}")
    
    # Create question embeddings
    q_chunks = Chunks()
    q_chunks.add(question)
    q_embeddings = rag.createEmbeddings(q_chunks, EMBEDDING_CONFIG)
    
    # Search in persistent index
    similar = rag.similaritySearch(k, q_embeddings.jsonContent, FAISS_CONFIG)
    
    print(f"   Found {similar.size} relevant chunks")
    
    # Build prompt and get answer
    prompt = rag.buildPrompt(question, similar)
    response, _ = rag.prompt(LLM_CONFIG, prompt)
    
    return {
        'question': question,
        'answer': response,
        'sources': similar.items,
        'distances': similar.distances
    }


def add_to_index(pdf_file: str):
    """Add a new document to an existing index."""
    
    # Check if index exists
    index_file = os.path.join(INDEX_PATH, f"{INDEX_NAME}.index")
    if not os.path.exists(index_file):
        print("⚠️ Index not found. Creating new index...")
        create_index([pdf_file])
        return
    
    rag = ragWrapper()
    
    doc_config = json.dumps({
        "pclass": "smartgenai.connectors.documents.simplePdf"
    })
    
    chunk_config = json.dumps({
        "method": "character",
        "separator": ".",
        "size": 500,
        "overlap": 50
    })
    
    print(f"➕ Adding to index: {os.path.basename(pdf_file)}")
    
    # Process document
    document = rag.read(pdf_file, doc_config)
    chunks = rag.chunk(document, chunk_config)
    embeddings = rag.createEmbeddings(chunks, EMBEDDING_CONFIG)
    
    # Add to existing index
    rag.storeEmbeddings(embeddings.jsonContent, FAISS_CONFIG)
    
    print(f"✅ Added {chunks.size} chunks to index")


def interactive_search():
    """Interactive search mode."""
    
    print("\n" + "="*50)
    print("Interactive Index Search")
    print("="*50)
    print("Commands: 'quit', 'sources' (show sources)")
    
    while True:
        question = input("\n❓ Question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not question:
            continue
        
        result = query_index(question)
        
        if result:
            print(f"\n💬 Answer: {result['answer']}")
            
            show_sources = input("\nShow sources? (y/n): ").strip().lower()
            if show_sources == 'y':
                print("\n📚 Sources:")
                for i, (source, distance) in enumerate(
                    zip(result['sources'], result['distances']), 1
                ):
                    print(f"\n--- Source {i} (distance: {distance:.4f}) ---")
                    print(source[:300] + "..." if len(source) > 300 else source)


def main():
    """Main function with examples."""
    
    print("="*50)
    print("SmartGenAI - Persistent Index Example")
    print("="*50)
    
    print("\nOptions:")
    print("1. Create index from PDFs")
    print("2. Query existing index")
    print("3. Add document to index")
    print("4. Interactive search")
    print("q. Quit")
    
    while True:
        choice = input("\nSelect option: ").strip()
        
        if choice.lower() == 'q':
            break
        
        if choice == '1':
            # Create index
            pdf_dir = input("Enter PDF directory path: ").strip()
            if not os.path.isdir(pdf_dir):
                print("Invalid directory")
                continue
            
            pdf_files = glob.glob(os.path.join(pdf_dir, "*.pdf"))
            if not pdf_files:
                print("No PDF files found")
                continue
            
            print(f"Found {len(pdf_files)} PDF files")
            confirm = input("Create index? (y/n): ").strip().lower()
            if confirm == 'y':
                create_index(pdf_files)
        
        elif choice == '2':
            # Query index
            question = input("Enter question: ").strip()
            if question:
                result = query_index(question)
                if result:
                    print(f"\n💬 Answer: {result['answer']}")
        
        elif choice == '3':
            # Add document
            pdf_file = input("Enter PDF file path: ").strip()
            if os.path.isfile(pdf_file):
                add_to_index(pdf_file)
            else:
                print("File not found")
        
        elif choice == '4':
            # Interactive search
            interactive_search()


if __name__ == "__main__":
    main()

