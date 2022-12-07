'''
sort videos for youtubers into file:
we want adam ragusea, joshua weissman, gordon ramsay, foodwishes
'''
# %%
import scrapetube
import pickle
import pandas as pd
import datetime

# %%
def rel_date_to_dt(rel_date):
    parsed_s = [rel_date.split()[:2]]
    parsed_s[0][1] = 'days'
    time_dict = dict((fmt,float(amount)) for amount,fmt in parsed_s)
    dt = datetime.timedelta(**time_dict)
    past_time = datetime.datetime.now() - dt
    
    return past_time

print(rel_date_to_dt("34 days"))
# %%
def raw_vid_to_dict(sample_vid):
    videoid = (sample_vid['videoId'])
    thumbnail_url = sample_vid['thumbnail']['thumbnails'][0]['url']
    title = sample_vid['title']['runs'][0]['text']
    length = sample_vid['lengthText']['accessibility']['accessibilityData']['label']
    upload_date = sample_vid['publishedTimeText']['simpleText']
    description_snip = sample_vid['descriptionSnippet']['runs'][0]['text']
    vid_dict = {'Video Name': title, 'Thumbnail URL': thumbnail_url, 'Video ID': videoid,
        'length' : length, 'description snippet': description_snip, 'date published': upload_date}
    return vid_dict

# %%
def channel_to_df(channel_in, identifier_string):
    channel_vids = scrapetube.get_channel(channel_url=channel_in)
    vid_lim = 0
    video_array = []

    for video in channel_vids:
        if vid_lim == 300:
            break
        video_array.append(video)
        vid_lim += 1

    dict_list = []
    for video in video_array:
        dict_list.append(raw_vid_to_dict(video))
    video_df = pd.DataFrame(dict_list)
    video_df.to_csv(identifier_string + ".csv")

    return video_df

# %%
channel_url="https://www.youtube.com/@aragusea"
channel_to_df(channel_url, "AdamRaguseaVideos")

# %%
