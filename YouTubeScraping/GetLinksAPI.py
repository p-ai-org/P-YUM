# %%
import scrapetube
import pickle

# %%
ragusea_vids = scrapetube.get_channel(channel_url="https://www.youtube.com/@aragusea")
# %%
vid_lim = 0
rag_video_arr = []
for video in ragusea_vids:
    if vid_lim == 200:
        break
    rag_video_arr.append(video)
    vid_lim += 1

# %%
import datetime
def rel_date_to_dt(rel_date):
    parsed_s = [rel_date.split()[:2]]
    parsed_s[0][1] = 'days'
    time_dict = dict((fmt,float(amount)) for amount,fmt in parsed_s)
    dt = datetime.timedelta(**time_dict)
    past_time = datetime.datetime.now() - dt
    
    return past_time
# %%
def raw_vid_to_dict(sample_vid):
    videoid = (sample_vid['videoId'])
    thumbnail_url = sample_vid['thumbnail']['thumbnails'][0]['url']
    title = sample_vid['title']['runs'][0]['text']
    length = sample_vid['lengthText']['accessibility']['accessibilityData']['label']
    upload_date = sample_vid['publishedTimeText']['simpleText']
    dt = rel_date_to_dt(upload_date)
    description_snip = sample_vid['descriptionSnippet']['runs'][0]['text']
    vid_dict = {'Video Name': title, 'Thumbnail URL': thumbnail_url, 'Video ID': videoid,
        'length' : length, 'description snippet': description_snip, 'date published': dt}
    return vid_dict

# %%
import pandas as pd
dict_list = []
for video in rag_video_arr:
    dict_list.append(raw_vid_to_dict(video))
rag_df = pd.DataFrame(dict_list, index = False)
# %%
rag_df.to_csv("RaguseaChannelVideos.csv")
# %%
def url_to_id(vid_url):
    url_data = urlparse.urlparse(vid_url)
    query = urlparse.parse_qs(url_data.query)
    video = query["v"][0]