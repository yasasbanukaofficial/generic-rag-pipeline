# Constants
TOP_K = 6

# Retrieve the most relevant chunks for a user query
def retrieve_chunks(query: str, vector_store, k: int = TOP_K):
    """Retrieval Pipeline"""
    print(f"Retrieving chunks for the query: {query}")

    if not query.strip():
        raise ValueError("The query cannot be empty. Please provide a search term.")

    print("Converting user query to vector embedding...")

    # Search through the vector DB
    results = vector_store.similarity_search(query, k=k)

    return results
