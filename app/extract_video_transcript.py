from youtube_transcript_api import YouTubeTranscriptApi

def extract_transcript(video_id):
    ytt_api = YouTubeTranscriptApi()

    fetched_transcript = ytt_api.fetch(video_id, languages=['en'])

    # creating or overwriting a file "subtitles.txt"
    outfile = "/usr/src/app/app/subtitles.txt"
    with open(outfile, "w") as f:
        # iterating through each element of list srt
            for i in fetched_transcript:
                # writing each element of fetched_transcript on a new line
                f.write("{}\n".format(i.text))

if __name__ == "__main__":
    video_id = "RJaHbip4qiw"
    extract_transcript(video_id)