import os

from dotenv import load_dotenv

load_dotenv()

# Constants
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
OPENAI_API_URL = os.environ["OPENAI_API_URL"]
EMBEDDING_MODEL = os.environ["EMBEDDING_MODEL"]

CHROMA_API_KEY = os.environ["CHROMA_API_KEY"]
CHROMA_TENANT = os.environ["CHROMA_TENANT"]
CHROMA_DATABASE = os.environ["CHROMA_DATABASE"]
CHROMA_COLLECTION_NAME = os.environ["CHROMA_COLLECTION_NAME"]
