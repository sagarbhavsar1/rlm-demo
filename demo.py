import os
import sys
from dotenv import load_dotenv
from simple_rlm import SimpleRLM
from rich.console import Console

# Load .env if present (useful for API keys if using non-local models)
load_dotenv()

console = Console()

def main():
    # Allow model override via env var, default to a common ollama model
    # Users can change this to "gemini/gemini-pro" or "gpt-4o" if they have keys
    model_name = os.getenv("RLM_MODEL", "ollama/llama3")

    console.print(f"[bold]Starting RLM Demo with model:[/bold] {model_name}")
    console.print("[dim]Ensure you have Ollama running with 'ollama serve' and have pulled the model if using local.[/dim]\n")

    rlm = SimpleRLM(model_name=model_name, verbose=True)

    # Example Query
    query = "Calculate the 10th Fibonacci number. Then, use that number to calculate its square root."
    
    console.print(f"[bold green]User Query:[/bold green] {query}\n")
    
    try:
        result = rlm.completion(query)
        console.print(f"\n[bold purple]Final Result:[/bold purple] {result}")
    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
        console.print("[dim]Tip: If using Ollama, make sure it's running. If using an API, check your keys.[/dim]")

if __name__ == "__main__":
    main()
