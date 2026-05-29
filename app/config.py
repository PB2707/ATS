import os
from dotenv import load_dotenv
load_dotenv()
POSTGRES_DSN = os.getenv("POSTGRES_DSN")
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = int(os.getenv("QDRANT_PORT"))
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")