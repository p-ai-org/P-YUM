# %%
from youtube_transcript_api import YouTubeTranscriptApi
import nltk
from nltk.tokenize import word_tokenize
import string
import os
import pickle
from nltk.corpus import stopwords
from string import punctuation
from nltk.stem import WordNetLemmatizer
import io
import re
import numpy as np
import csv
import pandas as pd


# %% preprocess_reviews removes non-alphabetical characters, stop words, and lemmatizes dataset
def preprocess_text(reviews):
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(reviews)
    # convert to lower case
    tokens = [w.lower() for w in tokens]
    # remove punctuation
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # remove remaining non-alphabetic words
    words = [word for word in stripped if word.isalpha()]
    stop_words = set(stopwords.words('english')+list(punctuation))
    cleaned = [w for w in words if w not in stop_words]
    super_clean = [lemmatizer.lemmatize(word) for word in cleaned]
    return super_clean
# %%
def fetch_transcripts(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        try:
            full_trans = ''
            transcript = transcript_list.find_transcript(['en', 'en-US'])
            text_list = transcript.fetch()
            for chunk in text_list:
                print(chunk)
                full_trans += ' ' + chunk['text']
            return full_trans
        except Exception as e:
            print(e)
            try:
            # if the transcript is not in english, autogenerate english captions from that language
                transcript = transcript_list.find_transcript([
                    'de', 'zh_Hans', 'fr', 'zh-Hant', 'es',
                    'ar', 'hi', 'it', 'ru', 'vi', 'th', 'sv',
                    'fa', 'pt', 'cs', 'na', 'nl', 'el', 'fil', 'zh-TW'
                ])
                full_trans = ''
                translated_transcript = transcript.translate('en')
                for text in translated_transcript:
                    full_trans += ' ' + text['text']
                return full_trans
            except Exception as e:
                print(e)
                translated_transcript = ''
                return translated_transcript
    except Exception as e:
        print(e)
        return ''

# %%
rag_df = pd.read_csv("AdamRaguseaVideos.csv")
rag_df.head()
# %%
rag_df['transcript'] = rag_df['Video ID'].apply(fetch_transcripts)


# %%
rag_df.head()
rag_df.to_csv("AdamRaguseaVideos.csv")

# %%
