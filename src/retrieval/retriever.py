from vectorstore import open_vector_store


def main(query: str):
    """Retrieval Pipeline"""
    print("Running retrieval pipeline")

    print("Converting user query to vector embedding...")

    vector_store = open_vector_store()

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
