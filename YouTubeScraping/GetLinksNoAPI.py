# %%
from bs4 import BeautifulSoup
import requests
import pandas as pd

# %%
def get_source(url):
    return BeautifulSoup(requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, verify=False).text, 'html.parser')
# %%
sources = ["https://www.youtube.com/feeds/videos.xml?user=aragusea",
           "https://www.youtube.com/@JoshuaWeissman/videos",
           "https://www.youtube.com/@gordonramsay/videos",
           "https://www.youtube.com/@foodwishes/videos"]
# %%
def get_urls(source):
    soup = get_source(source)
    entry_dict_list = []
    for entry in soup.find_all("entry"):
        channel = ''
        ref = ''
        vidname = ''
        datepub = ''
        for title in entry.find_all("title"):
            vidname = title.text
        for link in entry.find_all("link"):
            ref = link["href"]
        for name in entry.find_all("name"):
            channel = name.text
        for pub in entry.find_all("published"):
            datepub = pub.text
        entry_dict_list.append({'channel': channel, 'link': ref, 'video name':vidname, 'publication date': datepub})
    return pd.DataFrame.from_dict(entry_dict_list)

# %%
ragusea_df = get_urls(sources[0])
# %%
ragusea_df.info
# %%
