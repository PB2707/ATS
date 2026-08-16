from fastapi import APIRouter, UploadFile, File
import uuid

from app.services.parser import pdf_to_text
from app.services.embeddings import embed
from app.services.vector_store import *
from app.services.database import *
from app.services.ranker import *
from app.models.schemas import SearchRequest
from app.dependencies import db
from app.models.schemas import JobRequest, MatchRequest
from app.services.jobs import *
from qdrant_client.models import PointStruct
router = APIRouter()


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    text = pdf_to_text(await file.read())

    cid = str(uuid.uuid4())
    vec = embed(text)

    save_candidate(cid, file.filename, text)
    upsert_vector(cid, vec, file.filename)

    return {"id": cid}


@router.post("/search")
def search(req: MatchRequest):

    # fetch JD
    job = get_job(req.job_id)

    if not job:
        return {"error": "job not found"}

    title, description = job

    # embed JD
    vec = embed(description)

    # search resumes
    hits = search_vector(vec, req.top_k)

    return [
        {
            "candidate_id": str(hit.id),
            "score": hit.score,
            "filename": hit.payload.get("filename")
        }
        for hit in hits
    ]

    


@router.post("/rank")
def rank(req: SearchRequest):

    job = get_job(req.job_id)

    if not job:
        return {"error": "job not found"}

    title, description = job
    # 1. Embed JD
    vec = embed(req.job_description)

    # 2. Search Qdrant
    hits = search_vector(vec, req.top_k)

    results = []

    # 3. Rank each resume
    for hit in hits:

        candidate_id = str(hit.id)

        # fetch resume text from postgres
        with db.cursor() as cur:
            cur.execute(
                "SELECT raw_resume, filename FROM candidates WHERE id=%s",
                (candidate_id,)
            )

            row = cur.fetchone()

        if not row:
            continue

        resume_text, filename = row

        # LLM ranking
        llm_result = rank_resume(
            description,
            resume_text
)

        results.append({
            "candidate_id": candidate_id,
            "filename": filename,
            "score": hit.score,
            "llm_result": llm_result
        })

    return results

@router.post("/jobs")
def create_job(req: JobRequest):

    job_id = str(uuid.uuid4())

    # embed JD
    vec = embed(req.description)

    # save postgres
    save_job(
        job_id,
        req.title,
        req.description
    )

    # save vector
    qdrant.upsert(
        collection_name="jobs",
        points=[
            PointStruct(
                id=job_id,
                vector=vec,
                payload={
                    "title": req.title
                }
            )
        ]
    )

    return {
        "job_id": job_id,
        "title": req.title
    }