import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


load_dotenv()

DOCS_PATH = "docs"

# Load documents
def load_documents(path="docs"):
    """Loading all the documents"""
    print(f"Loading documents from the path {path}")

    if not os.path.exists(path):
        raise FileNotFoundError(f"The directory {path} doesn't exist. Please try again by creating it!")

    loader = DirectoryLoader(
        path,
        glob="*.txt",
        loader_cls=TextLoader,
        show_progress=True
    )

    docs = loader.load()

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
    
    

# Add to a vector DB


def main():
    """Main ingestion Pipeline"""
    print("Running Main Pipeline")

    # Loading docs
    docs = load_documents(DOCS_PATH)

    # Splitting into chunks
    chunks = split_documents(docs)

if __name__ == "__main__":
    main()