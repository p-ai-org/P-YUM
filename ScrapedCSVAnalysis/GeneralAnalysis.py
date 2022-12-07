# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import importlib
import AdjectiveAnalysis as aa
import BertProcesses as bp

importlib.reload(bp)
importlib.reload(aa)

fsize = 15
lsize = 10
tdir = 'in'
major = 5.0
minor = 3.0
style = 'default'

plt.style.use(style)
# include to stop breaking dogx
plt.rcParams['font.size'] = fsize
plt.rcParams['legend.fontsize'] = lsize
plt.rcParams['xtick.direction'] = tdir
plt.rcParams['ytick.direction'] = tdir
plt.rcParams['xtick.major.size'] = major
plt.rcParams['xtick.minor.size'] = minor
plt.rcParams['ytick.major.size'] = major
plt.rcParams['ytick.minor.size'] = minor
# %%
dir = "C:\\Users\\tyxia\\OneDrive - Pomona College\\Pomona\\pai\\P-YUM\\ChannelCsvs\\clean\\"
# %%
pred_sentences = ['This was an awesome movie. I watch it twice my time watching this beautiful movie if I have known it was this good',
                  'One of the worst movies of all time. I cannot believe I wasted two hours of my life for this movie','I am doing ok']


# %%
def time_text_to_sec(text_in):
    time_ints = [int(i) for i in text_in.split() if i.isdigit()]
    return 60 * (time_ints[0]) + time_ints[-1]
# %%
def time_text_to_min(text_in):
    time_ints = [int(i) for i in text_in.split() if i.isdigit()]
    return time_ints[0] + time_ints[-1] / 60
# %%
def return_timing_info(df_in, outname='', save = False):
    df_in["length (m)"] = df_in["length"].apply(time_text_to_min)
    ax = df_in.hist(column='length (m)', bins=25, grid=False, figsize=(12,8), color='#86bf91', zorder=2, rwidth=0.9)
    ax = ax[0]
    
    for x in ax:
        # Despine
        x.spines['right'].set_visible(False)
        x.spines['top'].set_visible(False)
        x.spines['left'].set_visible(False)

        # Switch off ticks
        x.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")
        # Draw horizontal axis lines
        vals = x.get_yticks()
        for tick in vals:
            x.axhline(y=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)
        # Remove title
        x.set_title("")
        # Set x-axis label
        x.set_xlabel("Video length (Minutes)", labelpad=20, weight='bold', size=12)
        # Set y-axis label
        x.set_ylabel("Frequency", labelpad=20, weight='bold', size=12)
    if save == True:
        plt.savefig(outname + '.png')
    plt.show()
        
    return df_in["length (m)"].mode()[0]
# %%
def fetch_transcript_list(df_in):
    return list(df_in['transcript'])
# %%
def fetch_wpm(df_in, outname = '', save= False):
    df_in = df_in[df_in['transcript'].apply(lambda x: isinstance(x,str))]
    df_in["length (m)"] = df_in["length"].apply(time_text_to_min)
    df_in["num_words"] = df_in['transcript'].str.split().apply(len).value_counts()
    df_in["wpm"] = df_in["num_words"] / df_in["length (m)"]
    ax = df_in.hist(column='wpm', bins=25, grid=False, figsize=(12,8), color='#86bf91', zorder=2, rwidth=0.9)
    ax = ax[0]
    
    for x in ax:
        # Despine
        x.spines['right'].set_visible(False)
        x.spines['top'].set_visible(False)
        x.spines['left'].set_visible(False)

        # Switch off ticks
        x.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")
        # Draw horizontal axis lines
        vals = x.get_yticks()
        for tick in vals:
            x.axhline(y=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)
        # Remove title
        x.set_title("")
        # Set x-axis label
        x.set_xlabel("Words per minute", labelpad=20, weight='bold', size=12)
        # Set y-axis label
        x.set_ylabel("Frequency", labelpad=20, weight='bold', size=12)
    if save == True:
        plt.savefig(outname + '.png')
    plt.show()

# %%
def fetch_sponsor_rag(string_in):
    words = string_in.split(' ')
    
    for i in range(len(words)):
        if 'sponsor' in words[i].lower():
            return words[i-2]
    return ''


# %%
def partition_transcript(text):
    part_size = 40
    word_arr = text.split(' ')
    text_chunk_arr = []
    for i in range(0, len(word_arr), part_size):
        text_chunk_arr.append(' '.join(word_arr[i:i+part_size]))
    return text_chunk_arr
    


# %%
def bert_sentiment(df_in, transcript_bool = True):
    if transcript_bool:
        list_trans = df_in['transcript'].tolist()
        trans_sent = []
        for transcript in list_trans:
            try:
                partitioned_transcript = partition_transcript(transcript)
                sentiments = bp.make_pred(partitioned_transcript)
                trans_sent.append(np.mean(sentiments))
            except:
                trans_sent.append(None)
        return pd.Series(trans_sent, index = ['Transcript Sentiments']) 
    else:
        vid_names = df_in['Video Name'].tolist()
        preds = bp.make_pred(vid_names)
        
        return pd.Series(preds, index = ['Video Name Sentiments'])


# %%
def perform_analysis(df_in):
    


# %%
ramsay_df = pd.read_csv(dir + "GordonRamsayVideos.csv")
fetch_wpm(ramsay_df)
# %%
aa.gen_wordcloud(text)
# %%
