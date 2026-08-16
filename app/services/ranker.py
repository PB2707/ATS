import ollama
from app.config import OLLAMA_MODEL

def rank_resume(jd, resume):
    prompt = f"""
    Compare JD and resume.
    Return score and reason.

    JD:
    {jd}

    Resume:
    {resume[:5000]}
    """

    result = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[{"role":"user","content":prompt}]
    )

    return result["message"]["content"]