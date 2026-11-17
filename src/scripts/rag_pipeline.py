import os
from pathlib import Path

from ingestion.loader import DOCS_PATH, load_documents
from ingestion.chunker import split_documents
from vectorstore import PERSISTENT_DIR, create_vector_store, open_vector_store


def build_rag_pipeline():
    """Build the complete RAG pipeline."""
    print("🚀 Running ingestion pipeline...")

    if os.path.exists(PERSISTENT_DIR):
        print("🗄️ Vector DB already exists. No need to re-process documents")
        return open_vector_store()

    print(f"📄 Loading documents from {DOCS_PATH}...")
    docs = load_documents(DOCS_PATH)
    print(f"✅ Loaded {len(docs)} documents")

    print("✂️ Splitting documents into chunks...")
    chunks = split_documents(docs, chunk_overlap=200)
    print(f"✅ Created {len(chunks)} chunks")

    print("🔢 Generating embeddings and building vector store...")
    vector_store = create_vector_store(chunks)
    print("✅ Vector store ready")

    return vector_store


def ask(vector_store, query):
    """Ask a question and retrieve relevant chunks."""
    print("🔍 Searching the vector store...")

    results = vector_store.similarity_search(query, k=6)
    print(f"📚 Retrieved {len(results)} chunks")

    for i, result in enumerate(results, start=1):
        print(f"  [{i}] {result.page_content}")

    return results


if __name__ == "__main__":
    vector_store = build_rag_pipeline()

    query = input("❓ Search:  ")
    ask(vector_store, query)
