from datetime import datetime
from app.dependencies import db

def save_job(job_id, title, description):

    with db.cursor() as cur:
        cur.execute(
            """
            INSERT INTO jobs
            (id, title, description, created_at)
            VALUES (%s,%s,%s,%s)
            """,
            (
                job_id,
                title,
                description,
                datetime.utcnow()
            )
        )

        db.commit()


def get_job(job_id):

    with db.cursor() as cur:
        cur.execute(
            """
            SELECT title, description
            FROM jobs
            WHERE id=%s
            """,
            (job_id,)
        )

        return cur.fetchone()