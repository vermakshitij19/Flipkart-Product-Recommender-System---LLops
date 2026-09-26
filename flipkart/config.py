import os
from dotenv import load_dotenv

load_dotenv()

class config:
    ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
    ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    ASTRA_DB_KEY_SPACE = os.getenv("ASTRA_DB_KEY_SPACE")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"
    RAG_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


Config = config