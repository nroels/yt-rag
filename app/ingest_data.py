import os, psycopg2
from datetime import datetime
from extract_video_information import get_video_id, get_transcript, get_publish_date, get_channel_name, get_title_and_source
import sys

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

def build_video_row_from_url(url: str) -> dict:
    title, source = get_title_and_source(url)                  # title, "youtube"/"web"
    channel = get_channel_name(url)                            # channel name
    published_date = get_publish_date(url)                     # "YYYY-MM-DD" or None
    video_id = get_video_id(url)                               # 11-char id or False
    lang, transcript, duration_sec = get_transcript(video_id) if video_id else (None, None, None)

    # Your videos table expects an ISO-like timestamp; your extractor returns just the date.
    published_at = f"{published_date}T00:00:00Z" if published_date else None

    return {
        "title": title,
        "channel": channel,
        "published_at": published_at,
        "lang": lang,
        "transcript": transcript,
        "url": url,
        "source": source,
        "duration_sec": duration_sec,
        "fetched_at": None,          # let insert_video default to now()
        "file_id": None,
        "vector_store_id": None,
    }

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
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python ingest_data.py <youtube_url>")
    url = sys.argv[1]

    conn = get_connection()
    try:
        row = build_video_row_from_url(url)
        vid_id = insert_video(conn, row)  # uses your existing insert_video()  :contentReference[oaicite:5]{index=5}
        conn.commit()
        print("Inserted video:", vid_id)
    finally:
        conn.close()