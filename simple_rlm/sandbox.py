import sys
import io
import traceback
from typing import Any, Dict

class LocalREPL:
    """
    A simple local REPL environment that executes Python code using `exec`.
    It captures stdout and stderr and maintains a local namespace.
    """
    def __init__(self, globals_dict: Dict[str, Any] | None = None):
        self.globals = globals_dict or {}
        self.locals = {}

    def execute(self, code: str) -> str:
        """
        Executes the provided Python code string and returns the captured stdout/stderr.
        """
        # Capture stdout and stderr
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        redirected_output = io.StringIO()
        
        sys.stdout = redirected_output
        sys.stderr = redirected_output

        try:
            # We execute in a shared namespace to allow state persistence
            exec(code, self.globals, self.locals)
            result = redirected_output.getvalue()
            if not result:
                result = "[No output]"
            return result
        except Exception:
            # Print the traceback if an error occurs
            traceback.print_exc(file=redirected_output)
            return redirected_output.getvalue()
        finally:
            # Restore stdout/stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr
