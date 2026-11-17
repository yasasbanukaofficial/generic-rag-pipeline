from langchain_chroma import Chroma

from config import (
    CHROMA_API_KEY,
    CHROMA_COLLECTION_NAME,
    CHROMA_DATABASE,
    CHROMA_TENANT,
)
from embeddings import build_embedding_model

# Constants
PERSISTENT_DIR = "db/chroma_db"


# Create embeddings and add to a vector DB
def create_vector_store(chunks, persist_directory=PERSISTENT_DIR):
    """Create and persist ChromaDB vector DB"""
    print(f"Creating embeddings and storing it in Chroma DB")

    embedding_model = build_embedding_model()

    print("Adding Embeddings to the vector db")

    # For Cloud Integration
    # vector_store = Chroma.from_documents(
    #     documents=chunks,
    #     embedding=embedding_model,
    #     collection_name=CHROMA_COLLECTION_NAME,
    #     chroma_cloud_api_key=CHROMA_API_KEY,
    #     tenant=CHROMA_TENANT,
    #     database=CHROMA_DATABASE,
    #     collection_metadata={"hnsw:space": "cosine"}
    # )

    # For Local Storage
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        collection_name=CHROMA_COLLECTION_NAME,
        persist_directory=persist_directory,
        collection_metadata={"hnsw:space": "cosine"}
    )

    print("Finish adding embeddings to DB")
    return vector_store


def open_vector_store(persist_directory=PERSISTENT_DIR):
    """Open an existing ChromaDB vector store"""
    embedding_model = build_embedding_model()

    # For Local Storage
    vector_store = Chroma(
        embedding_function=embedding_model,
        collection_name=CHROMA_COLLECTION_NAME,
        persist_directory=persist_directory,
        collection_metadata={"hnsw:space": "cosine"}
    )

    return vector_store
