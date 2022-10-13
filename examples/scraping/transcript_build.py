'''
FREE GOURDS
TAI XIANG
GUY THAMPAKKUL
SAM MILLETTE
transcript_build takes in a csv of youtube links and iterates through them, outputting the subtitles to
a csv file. If the video is age restricted and the transcript cannot be accessed, then an asterisk is outputted
If a video transcript happens to be in another language, it is automatically translated with google's machine translation library
'''
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


# preprocess_reviews removes non-alphabetical characters, stop words, and lemmatizes dataset
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

# gathers the transcript when given a youtube video id
def get_transcripts(video_id, date_pub, names_in, country_in, category_in):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        trans_all = []
        trans_str = ''
        try:
            transcript = transcript_list.find_transcript(['en', 'en-US'])
            text = transcript.fetch()
            for t in text:
                clean = preprocess_text(t.get('text'))
                trans_all.append(clean)
            for i in trans_all:
                for x in i:
                    trans_str += x + ' '
        except:
            try:
				# if the transcript is not in english, autogenerate english captions from that language
                transcript = transcript_list.find_transcript([
                    'de', 'zh_Hans', 'fr', 'zh-Hant', 'es',
                    'ar', 'hi', 'it', 'ru', 'vi', 'th', 'sv',
                    'fa', 'pt', 'cs', 'na', 'nl', 'el', 'fil', 'zh-TW'
                ])
                translated_transcript = transcript.translate('en')
                text = translated_transcript.fetch()
                for t in text:
                    clean = preprocess_text(t.get('text'))
                    trans_all.append(clean)
                for i in trans_all:
                    for x in i:
                        trans_str += x + ' '
            except:
				# if the video happens to be in a language that was not noted return an empty string
                trans_str = ''
        with open('/home/txaa2019/free_gourds/Youtube Grab/text_files/' + country_in + '/' + category_in + '-text.csv', 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([date_pub, names_in, trans_str])
            print('done writing')
    except Exception as e: 
        print(e)
        with open('/home/txaa2019/free_gourds/Youtube Grab/text_files/' + country_in + '/' + category_in + '-text.csv', 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
			# we cannot easily get the transcript of age restricted videos so we mark that with an asterisk
            csvwriter.writerow([date_pub, names_in, '*'])
            print('done writing')
 
# writes the period published, name, and transcript of a given video to the csv file
def write_transcripts(category_num, country_in):
    file = open('/home/txaa2019/free_gourds/Youtube Grab/Categories/' + country_in + '/' + category_num + '.csv')
    csv_f = csv.reader(file)
    links_in = []
    dates_in = []
    names_in = []
    for column in csv_f:
        links_in.append(column[1][32:])
        dates_in.append(column[0])
        names_in.append(column[2])
    for links, dates, names in zip(links_in, dates_in, names_in):
        get_transcripts(links, dates, names, country_in, category_num)

# gathers the transcript when given a youtube video id but does so for videos that are not filtered by id
def get_transcripts_all(video_id, date_pub, names_in, country_in):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        trans_all = []
        trans_str = ''
        try:
            transcript = transcript_list.find_transcript(['en', 'en-US'])
            text = transcript.fetch()
            for t in text:
                clean = preprocess_text(t.get('text'))
                trans_all.append(clean)
            for i in trans_all:
                for x in i:
                    trans_str += x + ' '
        except:
            try: 
                transcript = transcript_list.find_transcript([
                    'de', 'zh_Hans', 'fr', 'zh-Hant', 'es',
                    'ar', 'hi', 'it', 'ru', 'vi', 'th', 'sv',
                    'fa', 'pt', 'cs', 'na', 'nl', 'el', 'fil', 'zh-TW'
                ])
                translated_transcript = transcript.translate('en')
                text = translated_transcript.fetch()
                for t in text:
                    clean = preprocess_text(t.get('text'))
                    trans_all.append(clean)
                for i in trans_all:
                    for x in i:
                        trans_str += x + ' '
            except:
                trans_str = ''
#         with open('/home/txaa2019/free_gourds/Youtube Grab/text_files/All/' + country_in + '_all_text.csv', 'a') as csvfile:
        with open('/home/txaa2019/free_gourds/Youtube Grab/text_files/All/global_all_text.csv', 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([date_pub, names_in, trans_str])
            print('done writing')
    except Exception as e: 
        print(e)
        with open('/home/txaa2019/free_gourds/Youtube Grab/text_files/All/' + country_in + '_all_text.csv', 'a') as csvfile:
#         with open('/home/txaa2019/free_gourds/Youtube Grab/text_files/All/global_all_text.csv', 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([date_pub, names_in, '*'])
            print('done writing')
	
# writes the transcript to a csv file
def write_transcripts_all(country_in):
    file = open('/home/txaa2019/free_gourds/Youtube Grab/Categories/All/' + country_in + '_nocat.csv')
#     file = open('/home/txaa2019/free_gourds/Youtube Grab/Categories/All/global.csv')
    csv_f = csv.reader(file)
    links_in = []
    dates_in = []
    names_in = []
    for column in csv_f:
        links_in.append(column[1][32:])
        dates_in.append(column[0])
        names_in.append(column[2])
    for links, dates, names in zip(links_in, dates_in, names_in):
        get_transcripts_all(links, dates, names, country_in)
	
# loop through the categories and countries and write the transcripts to a csv file
arr_category_num = ['10', '19', '22', '24', '25', '26', '27', '28']
arr_country_name = ['Australia', 'Canada', 'India', 'United Kingdom', 'United States']
for country in arr_country_name:
    for category in arr_category_num:
        write_transcripts(category, country)
