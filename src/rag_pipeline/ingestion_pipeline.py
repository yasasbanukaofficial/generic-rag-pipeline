import os

from dotenv import load_dotenv
from pathlib import Path

from langchain_docling.loader import DoclingLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
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


# Load documents
def load_documents(path="docs"):
    """Loading all the documents"""
    print(f"Loading documents from the path {path}")

    if not os.path.exists(path):
        raise FileNotFoundError(f"The directory {path} doesn't exist. Please try again by creating it!")

    files = [f for f in Path(DOCS_PATH).iterdir() if f.is_file()]

    loaded_docs = DoclingLoader(
        file_path=files,
    ).load()

    docs = [Document(page_content=d.page_content, metadata={"source": str(d.metadata.get("source", ""))}) for d in loaded_docs]

    if len(docs) == 0:
        raise FileNotFoundError(f"No .txt files are found at the path of {path}. Please add the relevant documents before proceeding!")


    for i, doc in enumerate(docs[:2]):
        print(f"\nDocument {i+1}:")
        print(f"  Source: {doc.metadata['source']}")
        print(f"  Content length: {len(doc.page_content)} characters")
        print(f"  Content preview: {doc.page_content[100:130]}...")
        print(f"  metadata: {doc.metadata}")

    return docs


# Split documents into chunks
def split_documents(docs, chunk_size=1000, chunk_overlap=0):
    """Splitting document into chunks"""
    print(f"Splitting document into chunks")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(docs)

    if chunks:
    
        for i, chunk in enumerate(chunks[:2]):
            print(f"\n--- Chunk {i+1} ---")
            print(f"Source: {chunk.metadata['source']}")
            print(f"Length: {len(chunk.page_content)} characters")
            print(f"Content:")
            print(chunk.page_content)
            print("-" * 50)
        
        if len(chunks) > 5:
            print(f"\n... and {len(chunks) - 5} more chunks")
    
    return chunks
    
    

# Create embeddings and add to a vector DB
def create_vector_store(chunks, persist_directory=PERSISTENT_DIR):
    """Create and persist ChromaDB vector DB"""
    print(f"Creating embeddings and storing it in Chroma DB")

    embedding_model = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        base_url=OPENAI_API_URL,
        api_key=OPENAI_API_KEY,
        check_embedding_ctx_length=False
    )

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



def main():
    """Ingestion Pipeline"""
    print("Running ingestion Pipeline")

    if os.path.exists(PERSISTENT_DIR):
        print("Vector DB already exists. No need to re-process documents")
        embedding_model = OpenAIEmbeddings(
            model=EMBEDDING_MODEL,
            base_url=OPENAI_API_URL,
            api_key=OPENAI_API_KEY,
            check_embedding_ctx_length=False
        )

        vector_store = Chroma(
            persist_directory=PERSISTENT_DIR,
            embedding_function=embedding_model,
            collection_metadata={"hnsw:space": "cosine"}
        )

        return vector_store
    

    # Loading docs
    docs = load_documents(DOCS_PATH)

    # Splitting into chunks
    chunks = split_documents(docs, chunk_overlap=200)

    # Create embeddings and store in vector db
    vector_store = create_vector_store(chunks)

if __name__ == "__main__":
    main()