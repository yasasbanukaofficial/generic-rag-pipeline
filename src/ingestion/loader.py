import os

from pathlib import Path

from langchain_docling.loader import DoclingLoader
from langchain_core.documents import Document

# Constants
DOCS_PATH = "docs"


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
