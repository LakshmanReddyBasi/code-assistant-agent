import os
import json
import sys
from pathlib import Path
from dotenv import load_dotenv
from utils.loader import load_code_file
from utils.splitter import split_code
from chains.assistant_chain import create_assistant_chain
from vectorstore_manager import VectorStoreManager
from agent import create_code_agent
from utils.tools import run_code_safely

load_dotenv()

def detect_language(file_path):
    ext = Path(file_path).suffix
    return {"py": "python", "js": "javascript", "java": "java"}.get(ext[1:], "python")

def code_assistant(file_path, task="explain"):
    doc = load_code_file(file_path)
    lang = detect_language(file_path)
    
    agent = create_code_agent()
    agent_input = f"Analyze this {lang} code for issues: {doc.page_content[:1000]}"
    agent.invoke({"input": agent_input})
    # Process code
    code = doc.page_content if len(doc.page_content) <= 1000 else split_code(doc.page_content)[0]

    # Run LLM chain
    chain = create_assistant_chain(task)
    result = chain.invoke({"task": task, "code": code})

    validation = "Not validated"
    try:
        if task in ["debug", "refactor"] and "refactored_code" in result:
            from utils.tools import run_code_safely  # Ensure import
            validation = run_code_safely(result["refactored_code"], lang)
    except Exception as e:
        validation = f"Validation failed: {str(e)}"

    vsm = VectorStoreManager()
    vsm.add_experience(
        task=task,
        original_code=code,
        refactored_code=result.get("refactored_code", code),
        issues=result.get("issues_found", []),
        validation_result=validation
    )
    
    # Save output (Step 9)
    with open("output.json", "w") as f:
        json.dump(result, f, indent=2)

    return result

from chains.assistant_chain import create_qa_chain  # add this import at top

def ask_question(query, file_path):
    # Ensure code is in vectorstore
    doc = load_code_file(file_path)
    vsm = VectorStoreManager()
    vsm.add_code_and_explanation(doc.page_content, "Original user code")

    # Retrieve relevant context
    context = vsm.retrieve(query, k=2)

    # Use LLM to answer
    qa_chain = create_qa_chain()
    answer = qa_chain.invoke({"context": context, "question": query})
    
    print(f"❓ Question: {query}")
    print(f"💡 Answer: {answer}")
    return answer

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <file> [task|question]")
        sys.exit(1)

    file = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "debug"

    if mode in ["explain", "debug", "refactor"]:
        result = code_assistant(file, mode)
        print(json.dumps(result, indent=2))
    else:
        # Treat as question (Step 7)
        ask_question(mode, file)