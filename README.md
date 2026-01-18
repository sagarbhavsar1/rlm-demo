# RLM Demo

A simplified, free-to-run demonstration of **Recursive Language Models (RLMs)**.

This repository implements a lightweight version of the RLM concept: an LLM that can generate code, execute it in a local REPL, and observe the results to solve complex tasks.

Cited, inspired and derived from: https://github.com/alexzhang13/rlm

## Features
- **Free to Run**: Designed to work with [Ollama](https://ollama.com/) locally (no API keys required).
- **Lightweight**: Minimal dependencies (`litellm`, `rich`).
- **Code Execution**: Real Python code execution in a local sandbox.
- **Recursive-ready**: The RLM instance is injected into the sandbox, allowing the model to technically call itself (though the demo focuses on the REPL loop).

## Prerequisites
1. **Python 3.10+**
2. **Ollama** (for local models):
   - Install from [ollama.com](https://ollama.com/).
   - Pull a model: `ollama pull llama3` (or `mistral`, `gemma`, etc.).

## Installation

```bash
# Install dependencies
pip install -e .
```

## Usage

Run the demo script:

```bash
python demo.py
```

### Configuration
By default, it tries to use `ollama/llama3`. You can change the model by setting the `RLM_MODEL` environment variable:

```bash
# Use a different local model
RLM_MODEL=ollama/mistral python demo.py

# Use Gemini (requires GOOGLE_API_KEY env var)
RLM_MODEL=gemini/gemini-pro python demo.py
```

## Structure
- `simple_rlm/core.py`: The main RLM loop (Thought -> Code -> Observation).
- `simple_rlm/sandbox.py`: The local Python REPL executor.
- `demo.py`: Example script.
