from langchain_openai import ChatOpenAI
from rag_pipeline.config import AI_MODEL, OPENAI_API_KEY, OPENAI_API_URL

def build_ai_model():
    """Build AI Model"""
    return ChatOpenAI(
        model=AI_MODEL,
        base_url=OPENAI_API_URL,
        api_key=OPENAI_API_KEY
    )