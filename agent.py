# agent.py
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from utils.tools import read_file, lint_code, run_code_safely
from langchain.tools import tool
from dotenv import load_dotenv
import os

load_dotenv()

@tool
def read_code_file(filename: str) -> str:
    """Read and return the content of a code file (.py, .js, or .java)."""
    return read_file(filename)

@tool
def analyze_with_linter(code: str, language: str = "python") -> str:
    """Analyze code using a linter and return issues or 'No issues'."""
    return lint_code(code, language)

@tool
def execute_code_safely(code: str, language: str = "python") -> str:
    """Safely execute Python code in a sandbox and return output or error."""
    return run_code_safely(code, language)

def create_code_agent():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    
    tools = [read_code_file, analyze_with_linter, execute_code_safely]
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a senior code assistant. Use tools to read, lint, and test code. Then provide a complete analysis."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    
    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

def create_json_formatter():
    """Convert free-form agent output into structured JSON."""
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    prompt = ChatPromptTemplate.from_template("""
Convert the following code analysis into strict JSON with these keys:
- "summary": brief overview
- "steps": list of actions taken
- "issues_found": list of bugs or improvements
- "refactored_code": corrected code (if applicable)

Analysis:
{analysis}

Respond ONLY with valid JSON. No extra text.

""")
    return prompt | llm | JsonOutputParser()