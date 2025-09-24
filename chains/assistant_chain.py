# chains/assistant_chain.py
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from utils.prompt_templates import get_prompt_template
from dotenv import load_dotenv
import os

load_dotenv()

def create_assistant_chain(task):
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    prompt = get_prompt_template()
    parser = JsonOutputParser()
    return prompt | llm | parser

def create_qa_chain():
    """Create a chain for answering questions about code using retrieved context."""
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    prompt = ChatPromptTemplate.from_template("""
You are a helpful code assistant. Answer the question based only on the provided context.

Context:
{context}

Question: {question}

Answer concisely and accurately.
""")
    parser = StrOutputParser()
    return prompt | llm | parser