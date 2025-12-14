"""
Web Content RAG Example
=======================

This example demonstrates how to:
1. Fetch content from a web page
2. Chunk and embed the content
3. Answer questions about the web page

This is useful for:
- Analyzing news articles
- Summarizing documentation
- Extracting information from web pages
"""

from smartgenai.ragWrapper import ragWrapper
from smartgenai.framework.sets.chunks import chunks as Chunks
import json


def analyze_webpage(url: str, questions: list[str]):
    """Analyze a web page and answer questions about it."""
    
    # Initialize RAG
    rag = ragWrapper()
    
    # Configuration
    html_config = json.dumps({
        "pclass": "smartgenai.connectors.documents.html"
    })
    
    chunk_config = json.dumps({
        "method": "character",
        "separator": ".",
        "size": 400,
        "overlap": 50
    })
    
    embedding_config = json.dumps({
        "pclass": "smartgenai.connectors.embeddings.sentenceTransformer",
        "model": "paraphrase-mpnet-base-v2"
    })
    
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
    
    # Step 1: Fetch web content
    print(f"🌐 Fetching: {url}")
    document = rag.read(url, html_config)
    
    if len(document.content) == 0:
        print("❌ Failed to fetch content")
        return None
    
    print(f"   Retrieved {len(document.content)} characters")
    
    # Step 2: Chunk the content
    print("✂️ Chunking content...")
    chunks = rag.chunk(document, chunk_config)
    print(f"   Created {chunks.size} chunks")
    
    # Step 3: Create embeddings
    print("📐 Creating embeddings...")
    embeddings = rag.createEmbeddings(chunks, embedding_config)
    
    # Step 4: Answer each question
    results = []
    for question in questions:
        print(f"\n❓ {question}")
        
        # Create question embeddings
        q_chunks = Chunks()
        q_chunks.add(question)
        q_embeddings = rag.createEmbeddings(q_chunks, embedding_config)
        
        # Search
        similar = rag.memSimilaritySearch(
            k=3,
            textEmbeddings=q_embeddings.jsonContent,
            listEmbeddings=embeddings.jsonContent,
            jsonConfig=faiss_config
        )
        
        # Build prompt and get answer
        prompt = rag.buildPrompt(question, similar)
        response, _ = rag.prompt(llm_config, prompt)
        
        print(f"💬 {response}")
        results.append({
            'question': question,
            'answer': response
        })
    
    return results


def summarize_webpage(url: str):
    """Get a summary of a web page."""
    
    rag = ragWrapper()
    
    # Fetch content
    html_config = json.dumps({
        "pclass": "smartgenai.connectors.documents.html"
    })
    
    document = rag.read(url, html_config)
    
    if len(document.content) == 0:
        return "Failed to fetch content"
    
    # Get first portion for summarization
    content_preview = document.content[:3000]  # First 3000 chars
    
    # Build summarization prompt
    prompt = f"""Please provide a brief summary of the following web page content:

{content_preview}

Summary:"""
    
    llm_config = json.dumps({
        "pclass": "smartgenai.connectors.llms.ollama",
        "url": "http://localhost:11434/api",
        "model": "tinydolphin",
        "temperature": 0.3,
        "contextwindow": 4096
    })
    
    response, _ = rag.prompt(llm_config, prompt)
    return response


def main():
    """Main function with examples."""
    
    print("="*50)
    print("SmartGenAI - Web Content Analysis")
    print("="*50)
    
    # Example 1: Analyze a documentation page
    print("\n📖 Example 1: Analyze Python documentation")
    print("-" * 40)
    
    url = "https://docs.python.org/3/tutorial/introduction.html"
    questions = [
        "What is this page about?",
        "How do you write comments in Python?",
        "What types of numbers does Python support?"
    ]
    
    try:
        results = analyze_webpage(url, questions)
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Summarize a web page
    print("\n\n📝 Example 2: Web page summary")
    print("-" * 40)
    
    try:
        summary = summarize_webpage("https://www.python.org/about/")
        print(f"\n📄 Summary:\n{summary}")
    except Exception as e:
        print(f"Error: {e}")


def interactive_mode():
    """Interactive web analysis mode."""
    
    print("\n" + "="*50)
    print("Interactive Web Analysis")
    print("="*50)
    
    while True:
        url = input("\nEnter URL (or 'quit'): ").strip()
        
        if url.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not url.startswith('http'):
            url = 'https://' + url
        
        print("\nEnter questions (empty line to finish):")
        questions = []
        while True:
            q = input(f"  Q{len(questions)+1}: ").strip()
            if not q:
                break
            questions.append(q)
        
        if not questions:
            questions = ["What is this page about?"]
        
        try:
            analyze_webpage(url, questions)
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
    
    # Uncomment for interactive mode
    # interactive_mode()

