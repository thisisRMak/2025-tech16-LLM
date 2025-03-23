import streamlit as st
import os
import yt_rss_reader
import pandas as pd
from datetime import datetime, timedelta, tzinfo
from get_summary import get_summary

# set page to full width
st.set_page_config(layout="wide")
st.title("AI News Summarizer")

st.write("Here are links to the 15 most recent videos from our favorite YouTube channels about AI.")




if 'openai_api_key' not in st.session_state:    

    st.sidebar.header("API Keys")

    openai_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")
    if openai_key:
        st.session_state['openai_api_key'] = openai_key
        # os.environ['OPENAI_API_KEY'] = st.session_state['openai_api_key']

    # Warn if keys not provided
    if 'openai_api_key' not in st.session_state:
        st.warning('Please enter your API keys in the sidebar to continue')
        # st.stop()







all_channel_ids = [
    "UCKelCK4ZaO6HeEI1KQjqzWA", # AI Daily Brief
    "UC-yRDvpR99LUc5l7i7jLzew", # Bg2 Pod
    "UCXl4i9dYBrFOabk0xGmbkRA", # DwarkeshPatel
    "UCSI7h9hydQ40K5MJHnCrQvw", # No Priors
    "UCSHZKyawb77ixDdsGog4iWA", # Lex Fridman
]

all_rss_feeds = {}

for channel_id in all_channel_ids:
    
    df = yt_rss_reader.get_channel_rss_feed(channel_id)
    all_rss_feeds[channel_id] = df

channel_names = [all_rss_feeds[channel_id].iloc[0]['channel_name'] for channel_id in all_channel_ids]

tabs = st.tabs(channel_names)

for tab_idx in range(len(tabs)):
    with tabs[tab_idx]:
        st.header(channel_names[tab_idx])

        videos_df = all_rss_feeds[all_channel_ids[tab_idx]]

        for index, row in videos_df.iterrows():

            video_published_date = pd.to_datetime(row['published_date'])

            video_url = row['link']
            video_id = row['video_id']
            video_title = row['title']
            video_description = row['description']

            st.markdown("""---""")

            col1,col2 = st.columns([1, 2])
            
            col1.video(video_url)

            try:
                video_published_date = pd.to_datetime(row['published_date'])
                now = datetime.now(video_published_date.tzinfo)
                time_diff = now - video_published_date
                days_diff = time_diff.days
                hours_diff = time_diff.seconds // 3600
                
                if days_diff >= 7:
                    weeks = days_diff // 7
                    relative_time = f"{weeks} week{'s' if weeks != 1 else ''} ago"
                elif days_diff > 0:
                    relative_time = f"{days_diff} day{'s' if days_diff != 1 else ''} ago"
                else:
                    relative_time = f"{hours_diff} hour{'s' if hours_diff != 1 else ''} ago"
                
                relative_time = f"{relative_time} ({video_published_date.strftime('%Y-%m-%d')})"
            except:
                relative_time = str(row['published_date'])  # fallback to original date string
                
            col2.header(video_title)
            col2.write(f"Published: {relative_time}")
            
            summary_tab, description_tab = col2.tabs(["AI Summary", "Video Description"])
            
            with description_tab:
                container = st.container(border=True)
                container.write(video_description)

            with summary_tab:

                if 'openai_api_key' not in st.session_state:
                    st.warning('Please enter your API keys in the sidebar to enable summary generation')
                    

                elif col2.button("Generate Summary", key=f"summary_{video_id}"):

                    
                    summary = get_summary(video_id, video_url)
                    
                    container = st.container(border=True)
                    container.write(summary)

            
