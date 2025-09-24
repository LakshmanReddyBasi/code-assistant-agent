from datetime import datetime
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

INDEX_PATH = "code_index"

class VectorStoreManager:
    def __init__(self):
        # Hugging Face embedding model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vectorstore = self._load_or_create()

    def _load_or_create(self):
        if os.path.exists(INDEX_PATH):
            return FAISS.load_local(INDEX_PATH, self.embeddings, allow_dangerous_deserialization=True)
        else:
            empty = FAISS.from_texts([""], self.embeddings)
            empty.save_local(INDEX_PATH)
            return empty

    def add_code_and_explanation(self, code: str, explanation: str):
        text = f"Code:\n{code}\n\nExplanation:\n{explanation}"
        self.vectorstore.add_texts([text])
        self.vectorstore.save_local(INDEX_PATH)

    def retrieve(self, query: str, k=3):
        results = self.vectorstore.similarity_search(query, k=k)
        return "\n\n".join([r.page_content for r in results])
    
    def add_experience(
        self,
        task: str,
        original_code: str,
        refactored_code: str,
        issues: list,
        validation_result: str = "Not tested"
    ):
        experience = f"""
    [Task: {task}]
    [Original Code]
    {original_code}

    [Issues Found]
    - {'\n- '.join(issues) if issues else 'None'}

    [Refactored Code]
    {refactored_code}

    [Validation Result]
    {validation_result}

    [Stored: {datetime.now().strftime('%Y-%m-%d')}]
    """
        self.vectorstore.add_texts([experience])
        self.vectorstore.save_local(INDEX_PATH)