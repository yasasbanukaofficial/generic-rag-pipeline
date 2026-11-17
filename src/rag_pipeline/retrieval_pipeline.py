import os

from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

# Constants
DOCS_PATH = "docs"
PERSISTENT_DIR = "db/chroma_db"

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
OPENAI_API_URL = os.environ["OPENAI_API_URL"]
EMBEDDING_MODEL = os.environ["EMBEDDING_MODEL"]

CHROMA_API_KEY = os.environ["CHROMA_API_KEY"]
CHROMA_TENANT = os.environ["CHROMA_TENANT"]
CHROMA_DATABASE = os.environ["CHROMA_DATABASE"]
CHROMA_COLLECTION_NAME = os.environ["CHROMA_COLLECTION_NAME"]

def main():
    """Retrieval Pipeline"""
    print("Running retrieval pipeline")

    embedding_model = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        base_url=OPENAI_API_URL,
        api_key=OPENAI_API_KEY,
        check_embedding_ctx_length=False
    )

    # Takes the user input as query   
    query = input("Search:  ")
    print("Converting user query to vector embedding...")

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
    vector_store = Chroma(
        embedding_function=embedding_model,
        collection_name=CHROMA_COLLECTION_NAME,
        persist_directory=PERSISTENT_DIR,
        collection_metadata={"hnsw:space": "cosine"}
    )

    # Search through the vector DB
    results = vector_store.similarity_search(
        query,
        k=6
    )

    # Prints the retreived results
    for res in results:
        print(res.page_content)


if __name__ == "__main__":
    main()