# import subprocess
# import tempfile
# import os

# def run_pylint_on_code(code):
#     with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
#         f.write(code)
#         path = f.name

#     try:
#         result = subprocess.run(
#             ['pylint', '--reports=no', path],
#             capture_output=True, text=True
#         )
#         return result.stdout.strip() or "No pylint issues."
#     finally:
#         os.unlink(path)

import subprocess
import tempfile
import os
import sys

def read_file(filename: str) -> str:
    """Read a code file."""
    with open(filename, 'r') as f:
        return f.read()

def lint_code(code: str, language: str = "python") -> str:
    """Run linter based on language."""
    if language == "python":
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            path = f.name
        try:
            result = subprocess.run([sys.executable, '-m', 'pylint', '--reports=no', path],
                                  capture_output=True, text=True, timeout=10)
            return result.stdout or "No lint issues."
        finally:
            os.unlink(path)
    return "Linter not implemented for this language."

def run_code_safely(code: str, language: str = "python") -> str:
    """Safely execute code and return output or error."""
    if language != "python":
        return "Execution only supported for Python."
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        path = f.name
    try:
        result = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return f"Output: {result.stdout.strip()}"
        else:
            return f"Error: {result.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return "Error: Code timed out (infinite loop?)"
    finally:
        os.unlink(path)