from langchain_core.prompts import ChatPromptTemplate

def get_prompt_template():
    return ChatPromptTemplate.from_template("""
You are an expert software engineer.

Task: {task}

Code:
{code}

Respond ONLY in valid JSON with these keys:
- "summary": brief overview
- "steps": list of actions taken or issues analyzed
- "issues_found": list of bugs or improvements
- "refactored_code": corrected/refactored code

Do not add any other text.
""")