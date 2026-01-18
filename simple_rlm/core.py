import re
import litellm
from typing import List, Dict, Any, Optional
from rich.console import Console
from .sandbox import LocalREPL

console = Console()

class SimpleRLM:
    """
    A simplified Recursive Language Model.
    
    It runs a loop:
    1. Ask LLM for a response (Thought + Code).
    2. Extract code.
    3. Execute code in LocalREPL.
    4. Feed result back to LLM.
    5. Repeat until a final answer is found.
    """
    def __init__(
        self, 
        model_name: str = "ollama/llama3", 
        max_iterations: int = 10,
        verbose: bool = True
    ):
        self.model_name = model_name
        self.max_iterations = max_iterations
        self.verbose = verbose
        # We pass 'rlm' to the globals so the model can technically call rlm.completion()
        # This enables the "Recursive" part of RLM!
        self.sandbox = LocalREPL(globals_dict={"rlm": self})
        self.history: List[Dict[str, str]] = []

    def completion(self, prompt: str) -> str:
        """
        Main entry point. Takes a prompt and returns the final answer.
        """
        if self.verbose:
            console.print(f"[bold green]RLM Start:[/bold green] {prompt}")

        # Reset history for a new task, but we could keep it if we wanted multi-turn.
        # For this simple demo, we'll treat each completion as a fresh start with a system prompt.
        self.history = [
            {"role": "system", "content": self._get_system_prompt()}
        ]
        self.history.append({"role": "user", "content": prompt})

        for i in range(self.max_iterations):
            if self.verbose:
                console.print(f"\n[bold blue]Iteration {i+1}/{self.max_iterations}[/bold blue]")

            # 1. LLM Generation
            response = litellm.completion(
                model=self.model_name,
                messages=self.history,
                temperature=0.0  # Precise code generation
            )
            response_content = response.choices[0].message.content
            
            if self.verbose:
                console.print(f"[dim]LLM Response:[/dim]\n{response_content}")

            # Add to history
            self.history.append({"role": "assistant", "content": response_content})

            # 2. Check for Final Answer
            # If the model says "Final Answer:", we are done.
            if "Final Answer:" in response_content:
                final_answer = response_content.split("Final Answer:")[-1].strip()
                return final_answer
            
            # 3. Extract and Execute Code
            code = self._extract_code(response_content)
            if code:
                if self.verbose:
                    console.print(f"[yellow]Executing Code:[/yellow]\n{code}")
                
                output = self.sandbox.execute(code)
                
                if self.verbose:
                    console.print(f"[dim]Output:[/dim]\n{output}")
                
                # Feed output back to LLM
                observation = f"Observation:\n{output}"
                self.history.append({"role": "user", "content": observation})
            else:
                # If no code and no final answer, ask it to continue or conclude.
                self.history.append({
                    "role": "user", 
                    "content": "I did not see any code to execute or a 'Final Answer'. Please write python code or provide a Final Answer."
                })

        return "Max iterations reached without a Final Answer."

    def _extract_code(self, text: str) -> Optional[str]:
        """
        Finds the first python code block in the text.
        """
        match = re.search(r"```python(.*?)```", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None

    def _get_system_prompt(self) -> str:
        return """You are a Recursive Language Model (RLM).
You can solve tasks by writing Python code.
You have access to a REPL environment. 
Execute code by wrapping it in ```python ... ``` blocks.
The output of your code will be returned to you as an "Observation".

IMPORTANT:
1. You can use the variable `rlm` in your python code to call `rlm.completion("sub-task")`. 
   This allows you to recursively solve sub-problems!
2. When you have the answer, output it clearly starting with "Final Answer:".
3. If you need to print something to see it, use `print()`.
"""
