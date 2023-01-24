import pickle
import pandas as pd
import datetime
import os
import googleapiclient.discovery
import googleapiclient.errors

# Constants
SAMPLE_VIDEO_ID = 'dT_LaNOhY4s'
SAMPLE_CHANNEL_NAME = 'aragusea'
SAMPLE_CHANNEL_ID = 'UC9_p50tH3WmMslWRWKnM7dQ'
API_KEY = 'AIzaSyDjnmIKC92_ypql6FCvioFn-S1hGwHcjIA'

# Settings
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = API_KEY)

# Search
def search_by_channel_id(channel_id, order='date', maxResults=50):
    request = youtube.search().list(
        part = 'snippet',
        maxResults=maxResults,
        channelId=SAMPLE_CHANNEL_ID,
        order=order
    )
    response = request.execute()
    return response

def search_by_video_id(video_id):
    request = youtube.videos().list(
        part = 'snippet',
        id = video_id,
    )
    response = request.execute()
    print('got response')
    return response

# Extraction
def extract_description_from_response(response):
    try:
        description = response['items'][0]['snippet']['description']
    except:
        description = None
    return description

def extract_published_date_from_response(response):
    try:
        publishedAt = response['items'][0]['snippet']['publishedAt']
    except:
        publishedAt = None
    return publishedAt

def search_extract_description(video_id):
    response = search_by_video_id(video_id)
    description = extract_description_from_response(response)
    publishedAt = extract_published_date_from_response(response)
    return description, publishedAt

# Given a df with video IDs, do the API search & extract description + published date
def update_df(df):
    df['response'] = df['Video ID'].apply(search_by_video_id)
    df['description'] = df['response'].apply(extract_description_from_response)
    df['date published'] = df['response'].apply(extract_published_date_from_response)
    df = df.drop(columns='response')
    df.drop(columns=df.columns[0], axis=1, inplace=True)
    return df

# Given a CSV with Video ID, extract description + published date
# Updates the df with description & published date

def read_update_csv(filepath):
    df = pd.read_csv(filepath)
    update_df(df)
    df.to_csv(filepath)

read_update_csv('/Users/cathychang/Personal/P-YUM/ChannelCsvs/raw/AdamRaguseaVideos.csv')
