import requests
import pandas as pd
from datetime import datetime, timedelta, timezone
import caching

def _get_channel_rss_feed(channel_id):

    url_prefix = "https://www.youtube.com/feeds/videos.xml?channel_id="

    url = url_prefix + channel_id
    response = requests.get(url)

    if response.status_code == 200:
        # Parse XML content
        import xml.etree.ElementTree as ET
        root = ET.fromstring(response.content)
        
        # Extract video entries
        # XML namespace used in YouTube RSS feeds
        namespace = {'atom': 'http://www.w3.org/2005/Atom', 
                    'media': 'http://search.yahoo.com/mrss/'}
        
        # Extract channel title (which contains the handle)
        channel_title = root.find('atom:title', namespace).text
        # print(f"Channel title: {channel_title}")

        videos = []
        for entry in root.findall('atom:entry', namespace):
            video_data = {
                'title': entry.find('atom:title', namespace).text,
                'link': entry.find('atom:link', namespace).attrib['href'],
                # 'published': entry.find('atom:published', namespace).text,
                # 'updated': entry.find('atom:updated', namespace).text,
                'published_date': datetime.strptime(entry.find('atom:published', namespace).text, '%Y-%m-%dT%H:%M:%S%z'),
                'author': entry.find('.//atom:name', namespace).text,
                'video_id': entry.find('atom:id', namespace).text.split(':')[-1],
                'description': entry.find('media:group/media:description', namespace).text,
                'channel_name': channel_title
            }
            videos.append(video_data)
            
        # Convert to DataFrame for easier handling
        videos_df = pd.DataFrame(videos)
        # st.write(f"Found {len(videos)} videos for channel {channel_id}")
        # st.dataframe(videos_df)
    else:
        st.error(f"Failed to fetch RSS feed for channel {channel_id}")
    
    return videos_df

def get_channel_rss_feed(channel_id, today=True):
    
    cache_filename = caching.get_cache_filename(channel_id, today=today)

    if caching.does_cache_exist(cache_filename):
        videos_df = pd.read_csv(cache_filename)
    else:
        videos_df = _get_channel_rss_feed(channel_id)
        
        videos_df.to_csv(cache_filename, index=False)

    return videos_df

