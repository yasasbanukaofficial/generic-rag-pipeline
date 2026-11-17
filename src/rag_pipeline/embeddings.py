from langchain_openai import OpenAIEmbeddings

from rag_pipeline.config import EMBEDDING_MODEL, OPENAI_API_KEY, OPENAI_API_URL


def build_embedding_model():
    """Build the configured embedding model"""
    return OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        base_url=OPENAI_API_URL,
        api_key=OPENAI_API_KEY,
        check_embedding_ctx_length=False
    )
