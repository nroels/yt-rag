import os, psycopg2
from datetime import datetime

def get_connection():
    return psycopg2.connect(
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        port=os.environ.get("POSTGRES_PORT", "5432"),
    )

_VIDEO_INSERT_SQL = """
INSERT INTO videos
  (title, channel, published_at, lang, transcript, url, source, duration_sec, fetched_at, file_id, vector_store_id)
VALUES
  (%(title)s, %(channel)s, %(published_at)s, %(lang)s, %(transcript)s, %(url)s, %(source)s, %(duration_sec)s, %(fetched_at)s, %(file_id)s, %(vector_store_id)s)
RETURNING id;
"""
def insert_video(conn, video_row: dict):
    payload = {
        "title": video_row.get("title"),
        "channel": video_row.get("channel"),
        "published_at": video_row.get("published_at"),
        "lang": video_row.get("lang"),
        "transcript": video_row.get("transcript"),
        "url": video_row.get("url"),
        "source": video_row.get("source"),
        "duration_sec": video_row.get("duration_sec"),
        "fetched_at": video_row.get("fetched_at") or datetime.now(),
        "file_id": video_row.get("file_id"),
        "vector_store_id": video_row.get("vector_store_id"),
    }
    with conn.cursor() as cur:
        cur.execute(_VIDEO_INSERT_SQL, payload)
        return cur.fetchone()[0]

if __name__=="__main__":
    con=get_connection()
    vid = insert_video(con, {
        "title": "My Sample Video",
        "channel": "cool_channel",
        "published_at": "2025-10-05T10:00:00Z",
        "lang": "en",
        "transcript": "Full transcript...",
        "url": "https://www.youtube.com/watch?v=RJaHbip4qiw",
        "source": "youtube",
        "duration_sec": 1234,
        # fetched_at omitted -> set to now()
        "file_id": None,
        "vector_store_id": None,
    })
    con.commit()
    con.close()
    print("Inserted video:", vid)
