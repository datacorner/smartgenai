"""
Text Similarity Scoring Example
===============================

This example demonstrates how to use SmartGenAI to:
1. Calculate similarity between texts
2. Find the most similar text from a list
3. Cluster similar texts together

Use cases:
- Duplicate detection
- Content matching
- Semantic search
- Text clustering
"""

from smartgenai.ragWrapper import ragWrapper
from smartgenai.framework.sets.chunks import chunks as Chunks
import json


# Configurations
EMBEDDING_CONFIG = json.dumps({
    "pclass": "smartgenai.connectors.embeddings.sentenceTransformer",
    "model": "paraphrase-mpnet-base-v2"
})

FAISS_MEM_CONFIG = json.dumps({
    "pclass": "smartgenai.connectors.vstore.faiss"
})


def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate similarity score between two texts."""
    
    rag = ragWrapper()
    
    # Lower score = more similar (L2 distance)
    score = rag.similarityScore(
        text1, text2,
        FAISS_MEM_CONFIG,
        EMBEDDING_CONFIG
    )
    
    return score


def find_most_similar(query: str, candidates: list[str], top_k: int = 3) -> list[dict]:
    """Find the most similar texts from a list of candidates."""
    
    rag = ragWrapper()
    
    # Create embeddings for candidates
    cand_chunks = Chunks()
    for c in candidates:
        cand_chunks.add(c)
    cand_embeddings = rag.createEmbeddings(cand_chunks, EMBEDDING_CONFIG)
    
    # Create embeddings for query
    query_chunks = Chunks()
    query_chunks.add(query)
    query_embeddings = rag.createEmbeddings(query_chunks, EMBEDDING_CONFIG)
    
    # Search
    similar = rag.memSimilaritySearch(
        k=min(top_k, len(candidates)),
        textEmbeddings=query_embeddings.jsonContent,
        listEmbeddings=cand_embeddings.jsonContent,
        jsonConfig=FAISS_MEM_CONFIG
    )
    
    results = []
    for i, (text, distance) in enumerate(zip(similar.items, similar.distances)):
        results.append({
            'rank': i + 1,
            'text': text,
            'distance': distance,
            'similarity': 1 / (1 + distance)  # Convert distance to similarity
        })
    
    return results


def detect_duplicates(texts: list[str], threshold: float = 0.3) -> list[tuple]:
    """Detect potential duplicate or near-duplicate texts."""
    
    duplicates = []
    
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            score = calculate_similarity(texts[i], texts[j])
            if score < threshold:
                duplicates.append((i, j, score, texts[i][:50], texts[j][:50]))
    
    return duplicates


def example_basic_similarity():
    """Basic similarity comparison example."""
    
    print("\n" + "="*50)
    print("Example 1: Basic Similarity Comparison")
    print("="*50)
    
    pairs = [
        ("The cat sat on the mat", "A cat was sitting on a mat"),
        ("The cat sat on the mat", "The weather is nice today"),
        ("Machine learning is a subset of AI", "ML is part of artificial intelligence"),
        ("I love pizza", "Pizza is my favorite food"),
        ("I love pizza", "The stock market crashed"),
    ]
    
    for text1, text2 in pairs:
        score = calculate_similarity(text1, text2)
        print(f"\nText 1: '{text1}'")
        print(f"Text 2: '{text2}'")
        print(f"Distance: {score:.4f} (lower = more similar)")


def example_find_similar():
    """Find most similar texts example."""
    
    print("\n" + "="*50)
    print("Example 2: Find Most Similar")
    print("="*50)
    
    query = "How do I write a Python function?"
    
    candidates = [
        "Python functions are defined using the def keyword",
        "The weather forecast predicts rain tomorrow",
        "To create a function in Python, use def followed by the function name",
        "JavaScript uses the function keyword for function declarations",
        "Python is a popular programming language",
        "Functions in Python can return values using the return statement",
        "The cat jumped over the fence",
        "Python functions can have default parameters",
    ]
    
    print(f"\nQuery: '{query}'")
    print("\nMost similar texts:")
    
    results = find_most_similar(query, candidates, top_k=5)
    
    for r in results:
        print(f"\n  #{r['rank']} (distance: {r['distance']:.4f})")
        print(f"     {r['text']}")


def example_duplicate_detection():
    """Duplicate detection example."""
    
    print("\n" + "="*50)
    print("Example 3: Duplicate Detection")
    print("="*50)
    
    documents = [
        "Machine learning algorithms learn from data",
        "The stock market showed gains today",
        "ML algorithms are trained on datasets",  # Similar to first
        "Weather patterns are changing globally",
        "Algorithms in machine learning use data to learn",  # Similar to first
        "The financial markets performed well",  # Similar to second
        "Python is a programming language",
    ]
    
    print("\nDocuments:")
    for i, doc in enumerate(documents):
        print(f"  [{i}] {doc}")
    
    print("\nPotential duplicates (distance < 0.3):")
    duplicates = detect_duplicates(documents, threshold=0.3)
    
    if duplicates:
        for i, j, score, t1, t2 in duplicates:
            print(f"\n  Documents [{i}] and [{j}] (distance: {score:.4f})")
            print(f"    [{i}]: {t1}...")
            print(f"    [{j}]: {t2}...")
    else:
        print("  No duplicates found")


def example_semantic_search():
    """Semantic search example."""
    
    print("\n" + "="*50)
    print("Example 4: Semantic Search")
    print("="*50)
    
    # Knowledge base
    knowledge_base = [
        "Python was created by Guido van Rossum in 1991",
        "JavaScript is primarily used for web development",
        "Machine learning requires large amounts of data",
        "Deep learning uses neural networks with many layers",
        "Natural language processing deals with text analysis",
        "Computer vision is used for image recognition",
        "Databases store and organize data efficiently",
        "APIs allow different software systems to communicate",
        "Cloud computing provides on-demand computing resources",
        "Cybersecurity protects systems from attacks",
    ]
    
    queries = [
        "Who invented Python?",
        "What is used for websites?",
        "How do computers understand images?",
        "What protects against hackers?",
    ]
    
    for query in queries:
        print(f"\n🔍 Query: '{query}'")
        results = find_most_similar(query, knowledge_base, top_k=2)
        
        print("   Best matches:")
        for r in results:
            print(f"   • {r['text']} (score: {r['similarity']:.2f})")


def interactive_mode():
    """Interactive similarity testing."""
    
    print("\n" + "="*50)
    print("Interactive Similarity Testing")
    print("="*50)
    print("\nCommands:")
    print("  compare - Compare two texts")
    print("  search  - Search in a list")
    print("  quit    - Exit")
    
    while True:
        cmd = input("\nCommand: ").strip().lower()
        
        if cmd in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        elif cmd == 'compare':
            text1 = input("Text 1: ").strip()
            text2 = input("Text 2: ").strip()
            
            if text1 and text2:
                score = calculate_similarity(text1, text2)
                print(f"\nDistance: {score:.4f}")
                print(f"Similarity: {1/(1+score):.2%}")
        
        elif cmd == 'search':
            query = input("Query: ").strip()
            print("Enter candidates (empty line to finish):")
            candidates = []
            while True:
                c = input(f"  {len(candidates)+1}: ").strip()
                if not c:
                    break
                candidates.append(c)
            
            if query and candidates:
                results = find_most_similar(query, candidates)
                print("\nResults:")
                for r in results:
                    print(f"  #{r['rank']}: {r['text'][:50]}... ({r['similarity']:.2%})")


def main():
    """Run all examples."""
    
    print("="*50)
    print("SmartGenAI - Text Similarity Examples")
    print("="*50)
    
    example_basic_similarity()
    example_find_similar()
    example_duplicate_detection()
    example_semantic_search()
    
    # Uncomment for interactive mode
    # interactive_mode()


if __name__ == "__main__":
    main()

