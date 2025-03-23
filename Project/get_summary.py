import get_transcript
import os
import streamlit as st
from openai import OpenAI
from caching import get_cache_filename, does_cache_exist, load_dict_from_file, save_dict_to_file


def get_summary(video_id, video_url):
    cache_filename = get_cache_filename(f"summary_{video_id}", today=False)

    if does_cache_exist(cache_filename):
        return load_dict_from_file(cache_filename)
    
    summary = _get_summary(video_url)
    save_dict_to_file(summary, cache_filename)
    return summary

def _get_summary(video_url):
    

    transcript = get_transcript.get_yt_transcript([video_url])
    transcript_text = transcript[0].text

    openai_api_key = st.session_state['openai_api_key']
    client = OpenAI(api_key=openai_api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that produces a concise summary of youtube transcripts that are one liner conversation starters. Keep your responses short and concise. Use markdown formatting."},
            {"role": "user", "content": f"What are the 3 most important takeaways from this transcript?: {transcript_text}"}
        ]
    )

    return response.choices[0].message.content


