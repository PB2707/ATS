from qdrant_client.models import (
    PointStruct,
    Distance,
    VectorParams
)

from app.dependencies import qdrant

COLLECTION = "resumes"
JOB_COLLECTION = "jobs"

# -----------------------------
# CREATE COLLECTION IF MISSING
# -----------------------------
collections = qdrant.get_collections().collections
existing = [c.name for c in collections]

if COLLECTION not in existing:
    qdrant.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(
            size=1024,
            distance=Distance.COSINE
        ),
    )

# -----------------------------
# UPSERT
# -----------------------------
def upsert_vector(candidate_id, vector, filename):
    qdrant.upsert(
        collection_name=COLLECTION,
        points=[
            PointStruct(
                id=candidate_id,
                vector=vector,
                payload={"filename": filename}
            )
        ]
    )

# -----------------------------
# SEARCH
# -----------------------------
def search_vector(vec, top_k):
    results = qdrant.query_points(
        collection_name=COLLECTION,
        query=vec,
        limit=top_k
    )

    return results.points

if JOB_COLLECTION not in existing:
    qdrant.create_collection(
        collection_name=JOB_COLLECTION,
        vectors_config=VectorParams(
            size=1024,
            distance=Distance.COSINE
        ),
    )