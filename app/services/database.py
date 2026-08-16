from app.dependencies import db
from datetime import datetime

def save_candidate(id, filename, text):
    with db.cursor() as cur:
        cur.execute(
            "INSERT INTO candidates VALUES (%s,%s,%s,%s)",
            (id, filename, text, datetime.utcnow())
        )
        db.commit()