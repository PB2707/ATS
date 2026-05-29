from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Agentic ATS")

app.include_router(router)