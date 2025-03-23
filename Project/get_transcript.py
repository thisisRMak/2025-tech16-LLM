from llama_index.readers.youtube_transcript import YoutubeTranscriptReader

def get_yt_transcript(youtube_urls):
    youtube_reader = YoutubeTranscriptReader()
    documents = youtube_reader.load_data(ytlinks=youtube_urls)
    return documents


if __name__ == "__main__":
    youtube_urls = [
        "https://www.youtube.com/watch?v=hqPnATmnZmU",
        "https://www.youtube.com/watch?v=tUhZ5PQQtmw",
    ]

    yt_transcript = get_yt_transcript(youtube_urls)

    for transcript in yt_transcript:
        # print(type(transcript))
        print("\nTranscript text:")
        # print(transcript.text)
        # print("\nMetadata:")
        for key, value in transcript.metadata.items():
            print(f"{key}: {len(value)}")
            print(type(value))
            
        print("-" * 80)  # Separator between transcripts
