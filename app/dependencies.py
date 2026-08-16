from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
import psycopg2
from app.config import *

embedder = SentenceTransformer("BAAI/bge-large-en-v1.5")
qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
db = psycopg2.connect(POSTGRES_DSN)