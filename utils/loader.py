from langchain_community.document_loaders import TextLoader
from pathlib import Path

def load_code_file(file_path):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if path.suffix not in ['.py', '.js', '.java']:
        raise ValueError("Only .py, .js, .java files supported")
    return TextLoader(str(path), encoding="utf-8").load()[0]