from pydantic import BaseModel

class SearchRequest(BaseModel):
    job_description: str
    top_k: int = 5

class JobRequest(BaseModel):
    title: str
    description: str

class MatchRequest(BaseModel):
    job_id: str
    top_k: int = 5

    