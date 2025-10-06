from youtube_transcript_api import YouTubeTranscriptApi
import requests, re
from bs4 import BeautifulSoup

def get_video_id(url):
    reg_exp = re.compile(r"^.*((youtu\.be/)|(v/)|(/u/\w/)|(embed/)|(watch\?))\??v?=?([^#&?]*).*")
    match = reg_exp.match(url or "")

    return match.group(7) if (match and len(match.group(7)) == 11) else False

def get_title_and_source(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    title = soup.title.get_text(strip=True) if soup.title else None
    source = "youtube" if title and title.endswith(" - YouTube") else "web"
    if source == "youtube":
        title = title[:-len(" - YouTube")]

    return title, source

def get_channel_name(url):
    html = requests.get(url).text
    patterns = [
        r'href="/(?:channel|c|user)/[^"]+"\s*>([^<]+)</a>',
        r'"ownerChannelName"\s*:\s*"([^"]+)"',
        r'"ownerText"\s*:\s*\{\s*"runs"\s*:\s*\[\s*\{\s*"text"\s*:\s*"([^"]+)"',
        r'"videoDetails"\s*:\s*\{.*?"author"\s*:\s*"([^"]+)"',
        r'"author"\s*:\s*\{\s*"simpleText"\s*:\s*"([^"]+)"',
        r'<link\s+itemprop="name"\s+content="([^"]+)"',
    ]
    for pattern in patterns:
        match = re.search(pattern, html)
        if match:
            return match.group(1)
    return None

def get_publish_date(url):
    r = requests.get(url)
    match = re.search(r'(?<=itemprop="datePublished" content=")\d{4}-\d{2}-\d{2}', r.text)
    return match.group(0) if match else None

def get_transcript(id):
    ytt_api = YouTubeTranscriptApi()

    fetched_transcript = ytt_api.fetch(id, languages=['en'])
    transcript_text = "\n".join(i.text for i in fetched_transcript if i.text)
    duration_sec = (
        int(round(max(s.start + s.duration for s in fetched_transcript.snippets)))
    )
    language = (fetched_transcript.language_code or "en")

    return language, transcript_text, duration_sec

def write_subtitles_file(transcript_text, path="data/subtitles.txt"):
    with open(path, "w", encoding="utf-8") as f:
        f.write(transcript_text)

# if __name__ == "__main__":
#     video_url = "https://www.youtube.com/watch?v=Rv8fKGvGzbc&t"
#     video_id = get_video_id(video_url)
#     print(video_id)
#     print(get_channel_name(video_url))
#     print(get_publish_date(video_url))
#     # channel = get_channel_name(video_url)
#     video_title, video_source = get_title_and_source(video_url)
#     lang, transcript, duration = get_transcript(video_id)
#     write_subtitles_file(transcript)