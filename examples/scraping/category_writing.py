'''
FREE GOURDS
TAI XIANG
GUY THAMPAKKUL
SAM MILLETTE
category_writing utilizes the youtube api to return a list of youtube video ids based off a set of parameters.
For this project, we define parameters to be location uploaded, data uploaded, and video category
A video category key is available in this folder
'''

api_key = 'INSERT_YOUR_API_KEY'
from apiclient.discovery import build
import urllib.request
from urllib.request import Request, urlopen
import json

# build our youtube object
youtube = build('youtube', 'v3', developerKey = api_key)

# Get the number of views for a given video ID
def get_num_views(video_id):
    video_url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id='+ video_id + '&key='+ api_key
    response = urllib.request.urlopen(video_url)
    videos = json.load(response)
    for video in videos['items']:
        return video['statistics']['viewCount']
				
print(get_num_views('cGazy4z3eFo'))

# Get the title of a video given its video ID
def get_vid_title(video_id):
    video_url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id='+ video_id + '&key='+ api_key
    response = urllib.request.urlopen(video_url)
    videos = json.load(response)
    for video in videos['items']:
        return video['snippet']['title']
				
print(get_vid_title('cGazy4z3eFo'))

# Gather the most popular videos in the United States uploaded in a certain date range
def gather_vids_US(category, pub_after, pub_before, language):
    '''
    Since YouTube API limits to georeferencing by a 1000km radius, 
    we must gather videos from three regions of the US and aggregate later
    '''
    # region 1: west
    search_response_left = youtube.search().list(
        type = 'video',
        part = 'snippet',
        location = '41.4381, -113.5477',
        locationRadius = '1000km',
        videoCategoryId = category,
        videoCaption = 'closedCaption', 
        order = 'viewCount', 
        publishedAfter = pub_after + 'T00:00:00Z',
        publishedBefore = pub_before + 'T00:00:00Z',
        relevanceLanguage = language,
        regionCode = 'us',
        maxResults = '10',
        ).execute()
    # region 2: central
    search_response_middle = youtube.search().list(
        type = 'video',
        part = 'snippet',
        location = '41.4381, -97.5837',
        locationRadius = '1000km',
        videoCategoryId = category,
        videoCaption = 'closedCaption', 
        order = 'viewCount', 
        publishedAfter = pub_after + 'T00:00:00Z',
        publishedBefore = pub_before + 'T00:00:00Z',
        relevanceLanguage = language,
        regionCode = 'us',
        maxResults = '10',
        ).execute()
    # region 3: east
    search_response_right = youtube.search().list(
        type = 'video',
        part = 'snippet',
        location = '36.7508, -85.5837',
        locationRadius = '1000km',
        videoCategoryId = category,
        videoCaption = 'closedCaption', 
        order = 'viewCount', 
        publishedAfter = pub_after + 'T00:00:00Z',
        publishedBefore = pub_before + 'T00:00:00Z',
        relevanceLanguage = language,
        regionCode = 'us',
        maxResults = '10',
        ).execute()
    search_response_left = search_response_left['items']
    search_response_middle = search_response_middle['items']
    search_response_right = search_response_right['items']
    arr_left_link = []
    arr_middle_link = []
    arr_right_link = []
    # append the video ids for our videos to separate arrays
    for i in search_response_left:
        print(i['id'].get('videoId'), i['snippet'].get('title'))
        arr_left_link.append(i['id'].get('videoId'))
    for i in search_response_middle:
        print(i['id'].get('videoId'), i['snippet'].get('title'))
        arr_middle_link.append(i['id'].get('videoId'))
    for i in search_response_right:
        print(i['id'].get('videoId'), i['snippet'].get('title'))
        arr_right_link.append(i['id'].get('videoId'))
    # combine the arrays and remove the duplicates
    arr_all_link = arr_left_link + arr_middle_link + arr_right_link
	# remove any duplicate items that may have been added due to radius overlap
    arr_all_link = list(dict.fromkeys(arr_all_link))
    # sort the array from least viewed to most viewed
    sorted_arr_all_link = []
    while arr_all_link:
        minimum = arr_all_link[0]
        for i in arr_all_link:
            if get_num_views(i) < get_num_views(minimum):
                minimum = i
        sorted_arr_all_link.append(minimum)
        arr_all_link.remove(minimum)
    print(sorted_arr_all_link)
    # retrieve top 10 most viewed videos from the list
    sorted_arr_all_link = sorted_arr_all_link[-10:]
    # add the videos to a csv
    for items in sorted_arr_all_link:
        with open('/home/txaa2019/free_gourds/Youtube Grab/Categories/' + category + '.csv', 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['https://www.youtube.com/watch?v=' + items, get_vid_title(item)])

# Gather the most popular videos in the United Kingdom uploaded in a certain date range
def gather_vids_UK(category, pub_after, pub_before, language):
    search_response_left = youtube.search().list(
        type = 'video',
        part = 'snippet',
        location = '54.34428, -3.32285',
        locationRadius = '500km',
        videoCategoryId = category,
        videoCaption = 'closedCaption', 
        order = 'viewCount', 
        publishedAfter = pub_after + 'T00:00:00Z',
        publishedBefore = pub_before + 'T00:00:00Z',
        relevanceLanguage = language,
        regionCode = 'gb',
        maxResults = '10',
        ).execute()
    search_response_left = search_response_left['items']
    arr_left_link = []
    # append the video ids for our videos to separate arrays
    for i in search_response_left:
        print(i['id'].get('videoId'), i['snippet'].get('title'))
        arr_left_link.append(i['id'].get('videoId'))
    # retrieve top 10 most viewed videos from the list
    # add the videos to a csv
    for items in arr_left_link:
        with open('/home/txaa2019/free_gourds/Youtube Grab/Categories/United Kingdom/' + category + '.csv', 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([pub_after + '-' + pub_before, 'https://www.youtube.com/watch?v=' + items, get_vid_title(items)])
            print('done writing')

# Gather the most popular videos in Canada uploaded in a certain date range
def gather_vids_canada(category, pub_after, pub_before, language):
    '''
    Since YouTube API limits to georeferencing by a 1000km radius, 
    we must gather videos from three regions of Canada and aggregate later
    '''
    # region 1: west
    search_response_left = youtube.search().list(
        type = 'video',
        part = 'snippet',
        location = '58.4569, -117.4693',
        locationRadius = '1000km',
        videoCategoryId = category,
        videoCaption = 'closedCaption', 
        order = 'viewCount', 
        publishedAfter = pub_after + 'T00:00:00Z',
        publishedBefore = pub_before + 'T00:00:00Z',
        relevanceLanguage = language,
        regionCode = 'ca',
        maxResults = '10',
        ).execute()
    # region 2: central
    search_response_middle = youtube.search().list(
        type = 'video',
        part = 'snippet',
        location = '58.7512, -105.7974',
        locationRadius = '1000km',
        videoCategoryId = category,
        videoCaption = 'closedCaption', 
        order = 'viewCount', 
        publishedAfter = pub_after + 'T00:00:00Z',
        publishedBefore = pub_before + 'T00:00:00Z',
        relevanceLanguage = language,
        regionCode = 'ca',
        maxResults = '10',
        ).execute()
    # region 3: east
    search_response_right = youtube.search().list(
        type = 'video',
        part = 'snippet',
        location = '54.9181, -76.4334',
        locationRadius = '1000km',
        videoCategoryId = category,
        videoCaption = 'closedCaption', 
        order = 'viewCount', 
        publishedAfter = pub_after + 'T00:00:00Z',
        publishedBefore = pub_before + 'T00:00:00Z',
        relevanceLanguage = language,
        regionCode = 'ca',
        maxResults = '10',
        ).execute()
    search_response_left = search_response_left['items']
    search_response_middle = search_response_middle['items']
    search_response_right = search_response_right['items']
    arr_left_link = []
    arr_middle_link = []
    arr_right_link = []
    # append the video ids for our videos to separate arrays
    for i in search_response_left:
        print(i['id'].get('videoId'), i['snippet'].get('title'))
        arr_left_link.append(i['id'].get('videoId'))
    for i in search_response_middle:
        print(i['id'].get('videoId'), i['snippet'].get('title'))
        arr_middle_link.append(i['id'].get('videoId'))
    for i in search_response_right:
        print(i['id'].get('videoId'), i['snippet'].get('title'))
        arr_right_link.append(i['id'].get('videoId'))
    # combine the arrays and remove the duplicates
    arr_all_link = arr_left_link + arr_middle_link + arr_right_link
    print(arr_all_link)
	# remove any duplicate items that may have been added due to radius overlap
    arr_all_link = list(dict.fromkeys(arr_all_link))
    '''
    sort the array from least viewed to most viewed
    this odd flow is necessary or else we end up filling up youtube request quota
    far too quickly if we call get_num_views too many times
    ''' 
    view_num_array = []
    for i in arr_all_link:
        view_num_array.append(get_num_views(i))
    sorted_arr_all_link = []
    for x in range(len(view_num_array)):
        minimum = view_num_array[0]
        for i in view_num_array:
            print('checking...')
            if i < minimum:
                minimum = i
        minimum_vid_code = arr_all_link[view_num_array.index(minimum)]
        sorted_arr_all_link.append(minimum_vid_code)
        arr_all_link.remove(minimum_vid_code)
        view_num_array.remove(minimum)
    print(sorted_arr_all_link)
    # retrieve top 10 most viewed videos from the list
    sorted_arr_all_link = sorted_arr_all_link[-10:]
    print(sorted_arr_all_link)
    # add the videos to a csv
    for items in sorted_arr_all_link:
        with open('/home/txaa2019/free_gourds/Youtube Grab/Categories/Canada/' + category + '.csv', 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([pub_after + '-' + pub_before, 'https://www.youtube.com/watch?v=' + items, get_vid_title(items)])
            print('done writing')

# Gather the most popular videos in Australia uploaded in a certain date range
def gather_vids_australia(category, pub_after, pub_before, language):
    '''
    Since YouTube API limits to georeferencing by a 1000km radius, 
    we must gather videos from three regions of Australia and aggregate later
    '''
    # region 1: west
    search_response_left = youtube.search().list(
        type = 'video',
        part = 'snippet',
        location = '-24.6398, 123.8774',
        locationRadius = '1000km',
        videoCategoryId = category,
        videoCaption = 'closedCaption', 
        order = 'viewCount', 
        publishedAfter = pub_after + 'T00:00:00Z',
        publishedBefore = pub_before + 'T00:00:00Z',
        relevanceLanguage = language,
        regionCode = 'au',
        maxResults = '10',
        ).execute()
    # region 2: central
    search_response_middle = youtube.search().list(
        type = 'video',
        part = 'snippet',
        location = '-24.6398, 143.3149',
        locationRadius = '1000km',
        videoCategoryId = category,
        videoCaption = 'closedCaption', 
        order = 'viewCount', 
        publishedAfter = pub_after + 'T00:00:00Z',
        publishedBefore = pub_before + 'T00:00:00Z',
        relevanceLanguage = language,
        regionCode = 'au',
        maxResults = '10',
        ).execute()
    # region 3: east
    search_response_right = youtube.search().list(
        type = 'video',
        part = 'snippet',
        location = '-31.2922, 145.0148',
        locationRadius = '1000km',
        videoCategoryId = category,
        videoCaption = 'closedCaption', 
        order = 'viewCount', 
        publishedAfter = pub_after + 'T00:00:00Z',
        publishedBefore = pub_before + 'T00:00:00Z',
        relevanceLanguage = language,
        regionCode = 'au',
        maxResults = '10',
        ).execute()
    search_response_left = search_response_left['items']
    search_response_middle = search_response_middle['items']
    search_response_right = search_response_right['items']
    arr_left_link = []
    arr_middle_link = []
    arr_right_link = []
    # append the video ids for our videos to separate arrays
    for i in search_response_left:
        print(i['id'].get('videoId'), i['snippet'].get('title'))
        arr_left_link.append(i['id'].get('videoId'))
    for i in search_response_middle:
        print(i['id'].get('videoId'), i['snippet'].get('title'))
        arr_middle_link.append(i['id'].get('videoId'))
    for i in search_response_right:
        print(i['id'].get('videoId'), i['snippet'].get('title'))
        arr_right_link.append(i['id'].get('videoId'))
    # combine the arrays and remove the duplicates
    arr_all_link = arr_left_link + arr_middle_link + arr_right_link
    print(arr_all_link)
	# remove any duplicate items that may have been added due to radius overlap
    arr_all_link = list(dict.fromkeys(arr_all_link))
    '''
    sort the array from least viewed to most viewed
    this odd flow is necessary or else we end up filling up youtube request quota
    far too quickly if we call get_num_views too many times
    ''' 
    view_num_array = []
    for i in arr_all_link:
        view_num_array.append(get_num_views(i))
    sorted_arr_all_link = []
    for x in range(len(view_num_array)):
        minimum = view_num_array[0]
        for i in view_num_array:
            print('checking...')
            if i < minimum:
                minimum = i
        minimum_vid_code = arr_all_link[view_num_array.index(minimum)]
        sorted_arr_all_link.append(minimum_vid_code)
        arr_all_link.remove(minimum_vid_code)
        view_num_array.remove(minimum)
    print(sorted_arr_all_link)
    # retrieve top 10 most viewed videos from the list
    sorted_arr_all_link = sorted_arr_all_link[-10:]
    print(sorted_arr_all_link)
    # add the videos to a csv
    for items in sorted_arr_all_link:
        with open('/home/txaa2019/free_gourds/Youtube Grab/Categories/Australia/' + category + '.csv', 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([pub_after + '-' + pub_before, 'https://www.youtube.com/watch?v=' + items, get_vid_title(items)])
            print('done writing')

# Gather the most popular videos in India uploaded in a certain date range
def gather_vids_india(category, pub_after, pub_before, language):
    '''
    We only need to georeference two regions from India
    '''
    # region 1: south
    search_response_left = youtube.search().list(
        type = 'video',
        part = 'snippet',
        location = '17.2835, 78.0768',
        locationRadius = '1000km',
        videoCategoryId = category,
        videoCaption = 'closedCaption', 
        order = 'viewCount', 
        publishedAfter = pub_after + 'T00:00:00Z',
        publishedBefore = pub_before + 'T00:00:00Z',
        relevanceLanguage = language,
        regionCode = 'in',
        maxResults = '10',
        ).execute()
    # region 2: north
    search_response_middle = youtube.search().list(
        type = 'video',
        part = 'snippet',
        location = '24.7817, 79.4963',
        locationRadius = '800km',
        videoCategoryId = category,
        videoCaption = 'closedCaption', 
        order = 'viewCount', 
        publishedAfter = pub_after + 'T00:00:00Z',
        publishedBefore = pub_before + 'T00:00:00Z',
        relevanceLanguage = language,
        regionCode = 'in',
        maxResults = '10',
        ).execute()
    search_response_left = search_response_left['items']
    search_response_middle = search_response_middle['items']
    arr_left_link = []
    arr_middle_link = []
    # append the video ids for our videos to separate arrays
    for i in search_response_left:
        print(i['id'].get('videoId'), i['snippet'].get('title'))
        arr_left_link.append(i['id'].get('videoId'))
    for i in search_response_middle:
        print(i['id'].get('videoId'), i['snippet'].get('title'))
        arr_middle_link.append(i['id'].get('videoId'))
    # combine the arrays and remove the duplicates
    arr_all_link = arr_left_link + arr_middle_link
    print(arr_all_link)
    arr_all_link = list(dict.fromkeys(arr_all_link))
    '''
    sort the array from least viewed to most viewed
    this odd flow is necessary or else we end up filling up youtube request quota
    far too quickly if we call get_num_views too many times
    ''' 
    view_num_array = []
    for i in arr_all_link:
        view_num_array.append(get_num_views(i))
    sorted_arr_all_link = []
    for x in range(len(view_num_array)):
        minimum = view_num_array[0]
        for i in view_num_array:
            print('checking...')
            if i < minimum:
                minimum = i
        minimum_vid_code = arr_all_link[view_num_array.index(minimum)]
        sorted_arr_all_link.append(minimum_vid_code)
        arr_all_link.remove(minimum_vid_code)
        view_num_array.remove(minimum)
    print(sorted_arr_all_link)
    # retrieve top 10 most viewed videos from the list
    sorted_arr_all_link = sorted_arr_all_link[-10:]
    print(sorted_arr_all_link)
    # add the videos to a csv
    for items in sorted_arr_all_link:
        with open('/home/txaa2019/free_gourds/Youtube Grab/Categories/India/' + category + '.csv', 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([pub_after + '-' + pub_before, 'https://www.youtube.com/watch?v=' + items, get_vid_title(items)])
            print('done writing')
	
start_date = "2019-11-01"
stop_date = "2020-05-01"

start = datetime.strptime(start_date, "%Y-%m-%d")
start = start.date()
stop = datetime.strptime(stop_date, "%Y-%m-%d")
stop = stop.date()

# Gather the most popular videos in the United States uploaded in a certain date range regardless of category
def gather_vids_US_all(pub_after, pub_before, language):
    '''
    Since YouTube API limits to georeferencing by a 1000km radius, 
    we must gather videos from three regions of the US and aggregate later
    '''
    # region 1: west
    search_response_left = youtube.search().list(
        type = 'video',
        part = 'snippet',
        location = '41.4381, -113.5477',
        locationRadius = '1000km',
        videoCaption = 'closedCaption', 
        order = 'viewCount', 
        publishedAfter = pub_after + 'T00:00:00Z',
        publishedBefore = pub_before + 'T00:00:00Z',
        relevanceLanguage = language,
        regionCode = 'us',
        maxResults = '10',
        ).execute()
    # region 2: central
    search_response_middle = youtube.search().list(
        type = 'video',
        part = 'snippet',
        location = '41.4381, -97.5837',
        locationRadius = '1000km',
        videoCaption = 'closedCaption', 
        order = 'viewCount', 
        publishedAfter = pub_after + 'T00:00:00Z',
        publishedBefore = pub_before + 'T00:00:00Z',
        relevanceLanguage = language,
        regionCode = 'us',
        maxResults = '10',
        ).execute()
    # region 3: east
    search_response_right = youtube.search().list(
        type = 'video',
        part = 'snippet',
        location = '36.7508, -85.5837',
        locationRadius = '1000km',
        videoCaption = 'closedCaption', 
        order = 'viewCount', 
        publishedAfter = pub_after + 'T00:00:00Z',
        publishedBefore = pub_before + 'T00:00:00Z',
        relevanceLanguage = language,
        regionCode = 'us',
        maxResults = '10',
        ).execute()
    search_response_left = search_response_left['items']
    search_response_middle = search_response_middle['items']
    search_response_right = search_response_right['items']
    arr_left_link = []
    arr_middle_link = []
    arr_right_link = []
    # append the video ids for our videos to separate arrays
    for i in search_response_left:
        print(i['id'].get('videoId'), i['snippet'].get('title'))
        arr_left_link.append(i['id'].get('videoId'))
    for i in search_response_middle:
        print(i['id'].get('videoId'), i['snippet'].get('title'))
        arr_middle_link.append(i['id'].get('videoId'))
    for i in search_response_right:
        print(i['id'].get('videoId'), i['snippet'].get('title'))
        arr_right_link.append(i['id'].get('videoId'))
    # combine the arrays and remove the duplicates
    arr_all_link = arr_left_link + arr_middle_link + arr_right_link
    print(arr_all_link)
    arr_all_link = list(dict.fromkeys(arr_all_link))
    # sort the array from least viewed to most viewed
    view_num_array = []
    for i in arr_all_link:
        view_num_array.append(get_num_views(i))
    sorted_arr_all_link = []
    for x in range(len(view_num_array)):
        minimum = view_num_array[0]
        for i in view_num_array:
            print('checking...')
            if i < minimum:
                minimum = i
        minimum_vid_code = arr_all_link[view_num_array.index(minimum)]
        sorted_arr_all_link.append(minimum_vid_code)
        arr_all_link.remove(minimum_vid_code)
        view_num_array.remove(minimum)
    print(sorted_arr_all_link)
    # retrieve top 10 most viewed videos from the list
    sorted_arr_all_link = sorted_arr_all_link[-10:]
    print(sorted_arr_all_link)
    # add the videos to a csv
    for items in sorted_arr_all_link:
        with open('/home/txaa2019/free_gourds/Youtube Grab/Categories/All/united_states_nocat.csv', 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([pub_after + '-' + pub_before, 'https://www.youtube.com/watch?v=' + items, get_vid_title(items)])
            print('done writing')

# Gather the most popular videos in the United Kingdom uploaded in a certain date range regardless of category
def gather_vids_UK_all(pub_after, pub_before, language):
    search_response_left = youtube.search().list(
        type = 'video',
        part = 'snippet',
        location = '54.34428, -3.32285',
        locationRadius = '500km',
        videoCaption = 'closedCaption', 
        order = 'viewCount', 
        publishedAfter = pub_after + 'T00:00:00Z',
        publishedBefore = pub_before + 'T00:00:00Z',
        relevanceLanguage = language,
        regionCode = 'gb',
        maxResults = '10',
        ).execute()
    search_response_left = search_response_left['items']
    arr_left_link = []
    # append the video ids for our videos to separate arrays
    for i in search_response_left:
        print(i['id'].get('videoId'), i['snippet'].get('title'))
        arr_left_link.append(i['id'].get('videoId'))
    # retrieve top 10 most viewed videos from the list
    # add the videos to a csv
    for items in arr_left_link:
        with open('/home/txaa2019/free_gourds/Youtube Grab/Categories/All/united_kingdom_nocat.csv', 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([pub_after + '-' + pub_before, 'https://www.youtube.com/watch?v=' + items, get_vid_title(items)])
            print('done writing')

# Gather the most popular videos in the Canada uploaded in a certain date range regardless of category
def gather_vids_canada_all(pub_after, pub_before, language):
    '''
    Since YouTube API limits to georeferencing by a 1000km radius, 
    we must gather videos from three regions of Canada and aggregate later
    '''
    # region 1: west
    search_response_left = youtube.search().list(
        type = 'video',
        part = 'snippet',
        location = '58.4569, -117.4693',
        locationRadius = '1000km',
        videoCaption = 'closedCaption', 
        order = 'viewCount', 
        publishedAfter = pub_after + 'T00:00:00Z',
        publishedBefore = pub_before + 'T00:00:00Z',
        relevanceLanguage = language,
        regionCode = 'ca',
        maxResults = '10',
        ).execute()
    # region 2: central
    search_response_middle = youtube.search().list(
        type = 'video',
        part = 'snippet',
        location = '58.7512, -105.7974',
        locationRadius = '1000km',
        videoCaption = 'closedCaption', 
        order = 'viewCount', 
        publishedAfter = pub_after + 'T00:00:00Z',
        publishedBefore = pub_before + 'T00:00:00Z',
        relevanceLanguage = language,
        regionCode = 'ca',
        maxResults = '10',
        ).execute()
    # region 3: east
    search_response_right = youtube.search().list(
        type = 'video',
        part = 'snippet',
        location = '54.9181, -76.4334',
        locationRadius = '1000km',
        videoCaption = 'closedCaption', 
        order = 'viewCount', 
        publishedAfter = pub_after + 'T00:00:00Z',
        publishedBefore = pub_before + 'T00:00:00Z',
        relevanceLanguage = language,
        regionCode = 'ca',
        maxResults = '10',
        ).execute()
    search_response_left = search_response_left['items']
    search_response_middle = search_response_middle['items']
    search_response_right = search_response_right['items']
    arr_left_link = []
    arr_middle_link = []
    arr_right_link = []
    # append the video ids for our videos to separate arrays
    for i in search_response_left:
        print(i['id'].get('videoId'), i['snippet'].get('title'))
        arr_left_link.append(i['id'].get('videoId'))
    for i in search_response_middle:
        print(i['id'].get('videoId'), i['snippet'].get('title'))
        arr_middle_link.append(i['id'].get('videoId'))
    for i in search_response_right:
        print(i['id'].get('videoId'), i['snippet'].get('title'))
        arr_right_link.append(i['id'].get('videoId'))
    # combine the arrays and remove the duplicates
    arr_all_link = arr_left_link + arr_middle_link + arr_right_link
    print(arr_all_link)
    arr_all_link = list(dict.fromkeys(arr_all_link))
    '''
    sort the array from least viewed to most viewed
    this odd flow is necessary or else we end up filling up youtube request quota
    far too quickly if we call get_num_views too many times
    ''' 
    view_num_array = []
    for i in arr_all_link:
        view_num_array.append(get_num_views(i))
    sorted_arr_all_link = []
    for x in range(len(view_num_array)):
        minimum = view_num_array[0]
        for i in view_num_array:
            print('checking...')
            if i < minimum:
                minimum = i
        minimum_vid_code = arr_all_link[view_num_array.index(minimum)]
        sorted_arr_all_link.append(minimum_vid_code)
        arr_all_link.remove(minimum_vid_code)
        view_num_array.remove(minimum)
    print(sorted_arr_all_link)
    # retrieve top 10 most viewed videos from the list
    sorted_arr_all_link = sorted_arr_all_link[-10:]
    print(sorted_arr_all_link)
    # add the videos to a csv
    for items in sorted_arr_all_link:
        with open('/home/txaa2019/free_gourds/Youtube Grab/Categories/All/canada_nocat.csv', 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([pub_after + '-' + pub_before, 'https://www.youtube.com/watch?v=' + items, get_vid_title(items)])
            print('done writing')

# Gather the most popular videos in Australia uploaded in a certain date range regardless of category
def gather_vids_australia_all(pub_after, pub_before, language):
    '''
    Since YouTube API limits to georeferencing by a 1000km radius, 
    we must gather videos from three regions of Canada and aggregate later
    '''
    # region 1: west
    search_response_left = youtube.search().list(
        type = 'video',
        part = 'snippet',
        location = '-24.6398, 123.8774',
        locationRadius = '1000km',
        videoCaption = 'closedCaption', 
        order = 'viewCount', 
        publishedAfter = pub_after + 'T00:00:00Z',
        publishedBefore = pub_before + 'T00:00:00Z',
        relevanceLanguage = language,
        regionCode = 'au',
        maxResults = '10',
        ).execute()
    # region 2: central
    search_response_middle = youtube.search().list(
        type = 'video',
        part = 'snippet',
        location = '-24.6398, 143.3149',
        locationRadius = '1000km',
        videoCaption = 'closedCaption', 
        order = 'viewCount', 
        publishedAfter = pub_after + 'T00:00:00Z',
        publishedBefore = pub_before + 'T00:00:00Z',
        relevanceLanguage = language,
        regionCode = 'au',
        maxResults = '10',
        ).execute()
    # region 3: east
    search_response_right = youtube.search().list(
        type = 'video',
        part = 'snippet',
        location = '-31.2922, 145.0148',
        locationRadius = '1000km',
        videoCaption = 'closedCaption', 
        order = 'viewCount', 
        publishedAfter = pub_after + 'T00:00:00Z',
        publishedBefore = pub_before + 'T00:00:00Z',
        relevanceLanguage = language,
        regionCode = 'au',
        maxResults = '10',
        ).execute()
    search_response_left = search_response_left['items']
    search_response_middle = search_response_middle['items']
    search_response_right = search_response_right['items']
    arr_left_link = []
    arr_middle_link = []
    arr_right_link = []
    # append the video ids for our videos to separate arrays
    for i in search_response_left:
        print(i['id'].get('videoId'), i['snippet'].get('title'))
        arr_left_link.append(i['id'].get('videoId'))
    for i in search_response_middle:
        print(i['id'].get('videoId'), i['snippet'].get('title'))
        arr_middle_link.append(i['id'].get('videoId'))
    for i in search_response_right:
        print(i['id'].get('videoId'), i['snippet'].get('title'))
        arr_right_link.append(i['id'].get('videoId'))
    # combine the arrays and remove the duplicates
    arr_all_link = arr_left_link + arr_middle_link + arr_right_link
    print(arr_all_link)
    arr_all_link = list(dict.fromkeys(arr_all_link))
    '''
    sort the array from least viewed to most viewed
    this odd flow is necessary or else we end up filling up youtube request quota
    far too quickly if we call get_num_views too many times
    ''' 
    view_num_array = []
    for i in arr_all_link:
        view_num_array.append(get_num_views(i))
    sorted_arr_all_link = []
    for x in range(len(view_num_array)):
        minimum = view_num_array[0]
        for i in view_num_array:
            print('checking...')
            if i < minimum:
                minimum = i
        minimum_vid_code = arr_all_link[view_num_array.index(minimum)]
        sorted_arr_all_link.append(minimum_vid_code)
        arr_all_link.remove(minimum_vid_code)
        view_num_array.remove(minimum)
    print(sorted_arr_all_link)
    # retrieve top 10 most viewed videos from the list
    sorted_arr_all_link = sorted_arr_all_link[-10:]
    print(sorted_arr_all_link)
    # add the videos to a csv
    for items in sorted_arr_all_link:
        with open('/home/txaa2019/free_gourds/Youtube Grab/Categories/All/australia_nocat.csv', 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([pub_after + '-' + pub_before, 'https://www.youtube.com/watch?v=' + items, get_vid_title(items)])
            print('done writing')

# Gather the most popular videos in India uploaded in a certain date range regardless of category
def gather_vids_india_all(pub_after, pub_before, language):
    '''
    Since YouTube API limits to georeferencing by a 1000km radius, 
    we must gather videos from three regions of Canada and aggregate later
    '''
    # region 1: south
    search_response_left = youtube.search().list(
        type = 'video',
        part = 'snippet',
        location = '17.2835, 78.0768',
        locationRadius = '1000km',
        videoCaption = 'closedCaption', 
        order = 'viewCount', 
        publishedAfter = pub_after + 'T00:00:00Z',
        publishedBefore = pub_before + 'T00:00:00Z',
        relevanceLanguage = language,
        regionCode = 'in',
        maxResults = '10',
        ).execute()
    # region 2: north
    search_response_middle = youtube.search().list(
        type = 'video',
        part = 'snippet',
        location = '24.7817, 79.4963',
        locationRadius = '800km',
        videoCaption = 'closedCaption', 
        order = 'viewCount', 
        publishedAfter = pub_after + 'T00:00:00Z',
        publishedBefore = pub_before + 'T00:00:00Z',
        relevanceLanguage = language,
        regionCode = 'in',
        maxResults = '10',
        ).execute()
    search_response_left = search_response_left['items']
    search_response_middle = search_response_middle['items']
    arr_left_link = []
    arr_middle_link = []
    # append the video ids for our videos to separate arrays
    for i in search_response_left:
        print(i['id'].get('videoId'), i['snippet'].get('title'))
        arr_left_link.append(i['id'].get('videoId'))
    for i in search_response_middle:
        print(i['id'].get('videoId'), i['snippet'].get('title'))
        arr_middle_link.append(i['id'].get('videoId'))
    # combine the arrays and remove the duplicates
    arr_all_link = arr_left_link + arr_middle_link
    print(arr_all_link)
    arr_all_link = list(dict.fromkeys(arr_all_link))
    '''
    sort the array from least viewed to most viewed
    this odd flow is necessary or else we end up filling up youtube request quota
    far too quickly if we call get_num_views too many times
    ''' 
    view_num_array = []
    for i in arr_all_link:
        view_num_array.append(get_num_views(i))
    sorted_arr_all_link = []
    for x in range(len(view_num_array)):
        minimum = view_num_array[0]
        for i in view_num_array:
            print('checking...')
            if i < minimum:
                minimum = i
        minimum_vid_code = arr_all_link[view_num_array.index(minimum)]
        sorted_arr_all_link.append(minimum_vid_code)
        arr_all_link.remove(minimum_vid_code)
        view_num_array.remove(minimum)
    print(sorted_arr_all_link)
    # retrieve top 10 most viewed videos from the list
    sorted_arr_all_link = sorted_arr_all_link[-10:]
    print(sorted_arr_all_link)
    # add the videos to a csv
    for items in sorted_arr_all_link:
        with open('/home/txaa2019/free_gourds/Youtube Grab/Categories/All/india_nocat.csv', 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([pub_after + '-' + pub_before, 'https://www.youtube.com/watch?v=' + items, get_vid_title(items)])
            print('done writing')

# Gather the most popular videos in the World uploaded in a specific date range regardless of category and location
def gather_vids_global(pub_after, pub_before, language):
    search_response_left = youtube.search().list(
        type = 'video',
        part = 'snippet',
        videoCaption = 'closedCaption', 
        order = 'viewCount', 
        publishedAfter = pub_after + 'T00:00:00Z',
        publishedBefore = pub_before + 'T00:00:00Z',
        relevanceLanguage = language,
        regionCode = 'us',
        maxResults = '10',
        ).execute()
    search_response_left = search_response_left['items']
    arr_left_link = []
    # append the video ids for our videos to separate arrays
    for i in search_response_left:
        print(i['id'].get('videoId'), i['snippet'].get('title'))
        arr_left_link.append(i['id'].get('videoId'))
    # retrieve top 10 most viewed videos from the list
    # add the videos to a csv
    for items in arr_left_link:
        with open('/home/txaa2019/free_gourds/Youtube Grab/Categories/All/global.csv', 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([pub_after + '-' + pub_before, 'https://www.youtube.com/watch?v=' + items, get_vid_title(items)])
            print('done writing')

# iterate through categories
categories = ['10', '19', '22', '24', '25', '26', '27', '28']
from datetime import timedelta
# define time period cycle (2 weeks in this case)
for num in categories:
	while start < stop:
		after = datetime.strftime(start, "%Y-%m-%d")
		start = start + timedelta(days = 14)
		before = datetime.strftime(start, "%Y-%m-%d")
		print(after,before)
		gather_vids_canada(num, after, before, 'en')
