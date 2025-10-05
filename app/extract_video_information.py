from youtube_transcript_api import YouTubeTranscriptApi
import requests
from bs4 import BeautifulSoup
import re
import json

def youtube_parser(url: str):
    reg_exp = re.compile(r"^.*((youtu\.be/)|(v/)|(/u/\w/)|(embed/)|(watch\?))\??v?=?([^#&?]*).*")
    match = reg_exp.match(url or "")

    return match.group(7) if (match and len(match.group(7)) == 11) else False

def get_video_title(video_url):
    r = requests.get(video_url)
    soup = BeautifulSoup(r.text, "html.parser")

    # Title + source (your logic, just slightly cleaned)
    title = soup.title.get_text(strip=True) if soup.title else None
    source = "youtube" if title and title.endswith(" - YouTube") else "web"
    if source == "youtube":
        title = title[:-len(" - YouTube")]

    return title, source

# def get_channel_name(video_url):
#     r = requests.get(video_url)
#     soup = BeautifulSoup(r.text, "html.parser")
#
#     # 1) JSON-LD VideoObject → author.name
#     for s in soup.find_all("script", {"type": "application/ld+json"}):
#         try:
#             data = json.loads(s.string or "")
#             items = data if isinstance(data, list) else [data]
#             for d in items:
#                 if isinstance(d, dict) and d.get("@type") == "VideoObject":
#                     author = d.get("author")
#                     if isinstance(author, list) and author:
#                         author = author[0]
#                     if isinstance(author, dict):
#                         name = author.get("name")
#                         if name:
#                             return name
#         except Exception:
#             pass  # keep it minimal

def extract_transcript(video_id):
    ytt_api = YouTubeTranscriptApi()

    fetched_transcript = ytt_api.fetch(video_id, languages=['en'])
    transcript_text = "\n".join(i.text for i in fetched_transcript if i.text)
    duration_sec = int(round(sum(float(i.duration) for i in fetched_transcript if i.duration))) if fetched_transcript else None
    language = (fetched_transcript.language_code or "en")

    return language, transcript_text, duration_sec

def write_subtitles_file(transcript_text, path="subtitles.txt"):
    with open(path, "w", encoding="utf-8") as f:
        f.write(transcript_text)

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=Rv8fKGvGzbc&t"
    video_id = youtube_parser(video_url)
    # channel = get_channel_name(video_url)
    title, source = get_video_title(video_url)
    lang, transcript, duration = extract_transcript(video_id)
    write_subtitles_file(transcript)