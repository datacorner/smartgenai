"""
Simple LLM Prompt Example
=========================

This example shows how to use SmartGenAI for simple LLM interactions
without the full RAG pipeline.

Supported LLMs:
- Ollama (local)
- AWS Bedrock (Claude, Mistral, Titan)
- Hugging Face Inference API
"""

from smartgenai.ragWrapper import ragWrapper
import json
import os


def prompt_ollama(question: str):
    """Send a prompt to Ollama (local LLM)."""
    
    config = json.dumps({
        "pclass": "smartgenai.connectors.llms.ollama",
        "url": "http://localhost:11434/api",
        "model": "tinydolphin",
        "temperature": 0.7,
        "contextwindow": 2048
    })
    
    rag = ragWrapper()
    response, outputs = rag.prompt(config, question)
    return response


def prompt_aws_claude(question: str):
    """Send a prompt to AWS Bedrock Claude."""
    
    # Requires AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env vars
    config = json.dumps({
        "pclass": "smartgenai.connectors.llms.AWSModels.Claude",
        "region": "us-east-1",
        "model": "anthropic.claude-3-sonnet-20240229-v1:0",
        "temperature": 0.7,
        "max_tokens": 1024
    })
    
    rag = ragWrapper()
    response, outputs = rag.prompt(config, question)
    return response


def prompt_aws_mistral(question: str):
    """Send a prompt to AWS Bedrock Mistral."""
    
    config = json.dumps({
        "pclass": "smartgenai.connectors.llms.AWSModels.Mistral",
        "region": "us-east-1",
        "model": "mistral.mistral-7b-instruct-v0:2",
        "temperature": 0.7,
        "max_tokens": 1024
    })
    
    rag = ragWrapper()
    response, outputs = rag.prompt(config, question)
    return response


def prompt_huggingface(question: str):
    """Send a prompt to Hugging Face Inference API."""
    
    # Requires HUGGINGFACE_API_KEY env var
    config = json.dumps({
        "pclass": "smartgenai.connectors.llms.huggingFace",
        "model": "mistralai/Mistral-7B-Instruct-v0.1"
    })
    
    rag = ragWrapper()
    response, outputs = rag.prompt(config, question)
    return response


def main():
    """Interactive prompt example."""
    
    print("="*50)
    print("SmartGenAI - Simple LLM Prompt Example")
    print("="*50)
    print("\nSelect LLM provider:")
    print("1. Ollama (local)")
    print("2. AWS Bedrock - Claude")
    print("3. AWS Bedrock - Mistral")
    print("4. Hugging Face")
    print("q. Quit")
    
    providers = {
        '1': ('Ollama', prompt_ollama),
        '2': ('AWS Claude', prompt_aws_claude),
        '3': ('AWS Mistral', prompt_aws_mistral),
        '4': ('Hugging Face', prompt_huggingface)
    }
    
    while True:
        choice = input("\nSelect provider (1-4, q to quit): ").strip()
        
        if choice.lower() == 'q':
            print("Goodbye!")
            break
        
        if choice not in providers:
            print("Invalid choice. Please select 1-4.")
            continue
        
        provider_name, prompt_func = providers[choice]
        print(f"\nUsing {provider_name}")
        
        while True:
            question = input(f"\n[{provider_name}] Your question (or 'back'): ").strip()
            
            if question.lower() == 'back':
                break
            
            if not question:
                continue
            
            print("\n⏳ Getting response...")
            try:
                response = prompt_func(question)
                print(f"\n💬 Response:\n{response}")
            except Exception as e:
                print(f"\n❌ Error: {e}")


# Example with different temperatures
def temperature_comparison():
    """Compare responses at different temperature settings."""
    
    question = "Write a short poem about coding."
    temperatures = [0.1, 0.5, 0.9]
    
    print("\n" + "="*50)
    print("Temperature Comparison")
    print("="*50)
    print(f"\nQuestion: {question}")
    
    for temp in temperatures:
        config = json.dumps({
            "pclass": "smartgenai.connectors.llms.ollama",
            "url": "http://localhost:11434/api",
            "model": "tinydolphin",
            "temperature": temp,
            "contextwindow": 2048
        })
        
        rag = ragWrapper()
        response, _ = rag.prompt(config, question)
        
        print(f"\n--- Temperature: {temp} ---")
        print(response)


if __name__ == "__main__":
    main()
    
    # Uncomment to run temperature comparison
    # temperature_comparison()

