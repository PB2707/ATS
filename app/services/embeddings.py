from app.dependencies import embedder

def embed(text):
    return embedder.encode(text).tolist()