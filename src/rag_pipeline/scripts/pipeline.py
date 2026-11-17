import os

from rag_pipeline.ingestion.loader import DOCS_PATH, load_documents
from rag_pipeline.ingestion.chunker import split_documents

from rag_pipeline.retrieval.retriever import retrieve_chunks
from rag_pipeline.vectorstore import PERSISTENT_DIR, create_vector_store, open_vector_store

from rag_pipeline.generation.llm import build_ai_model
from rag_pipeline.generation.prompt import combine_prompt
from rag_pipeline.generation.answer import get_llm_response


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

    results = retrieve_chunks(query, vector_store)
    print(f"📚 Retrieved {len(results)} chunks")

    prompt = combine_prompt(query, results)
    llm_model = build_ai_model()
    response = get_llm_response(prompt, llm_model)

    return response


if __name__ == "__main__":
    vector_store = build_rag_pipeline()

    query = input("❓ Search:  ")
    resp = ask(vector_store, query)
    print(resp)
