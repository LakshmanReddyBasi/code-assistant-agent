# 🧠 Code Assistant Agent

A smart coding assistant that **explains, debugs, and refactors your code** using AI.  
Built with **LangChain**, **Groq**, and real developer tools.

---

## ✅ Features

- 📝 **Explain code in plain English**  
- 🐛 **Debug runtime errors and logic bugs**  
- ✨ **Refactor for readability and best practices**  
- 🔧 **Runs real tools**:  
  - Linter (`pylint`)  
  - Code executor  
  - File reader  
- 🧠 **Remembers past fixes** using a local vector database  
- ❓ **Answer questions like**:  
  - *“What does this function do?”*

---

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/your-username/code-assistant-agent.git
cd code-assistant-agent
pip install -r requirements.txt


2. Add Your Groq API Key

Create a .env file in the project root:

GROQ_API_KEY=your_groq_api_key_here


👉 Get your key at: https://console.groq.com/keys

3. Run It

Run the assistant with different tasks:

# Debug a file
python main.py sample_code/buggy.py debug

# Ask a question
python main.py sample_code/buggy.py "Why does find_max return 0 for negative numbers?"

🛠️ Supported Tasks

debug → Finds and fixes bugs

explain → Describes what the code does

refactor → Improves code style and structure

✅ Supports: .py, .js, .java files.

🤖 How It Works

You give it a code file and a task

The agent uses real tools:

Reads the file

Runs pylint to check style

Executes code to catch errors

AI analyzes results and returns:

✅ Summary

🔍 Steps taken

🐞 Issues found

🛠️ Fixed code

All fixes are saved locally in a vector database (FAISS) for future questions.

📦 Requirements

Python 3.9+

Groq API key

Install dependencies:

pip install langchain-groq langchain-huggingface faiss-cpu sentence-transformers pylint python-dotenv

💡 Why This Works

Uses openai/gpt-oss-120b on Groq — a model that supports tool calling

🔒 No cloud storage — vector DB is local and private

🗂️ Simple, single-file design for easy submission

📜 License

MIT License © 2025 [B Lakshman Reddy]


