# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import importlib
import AdjectiveAnalysis as aa
import BertProcesses as bp
from sys import platform

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
if platform =="win32":
    dir = "C:\\Users\\tyxia\\OneDrive - Pomona College\\Pomona\\pai\\P-YUM\\ChannelCsvs\\clean\\"
else:
    dir = "ChannelCsvs/clean/"
# %%
def time_text_to_sec(text_in):
    time_ints = [int(i) for i in text_in.split() if i.isdigit()]
    return 60 * (time_ints[0]) + time_ints[-1]
# %%
def time_text_to_min(text_in):
    time_ints = [int(i) for i in text_in.split() if i.isdigit()]
    if len(time_ints) == 3:
        return time_ints[0] * 60 + time_ints[1] + time_ints[-1] / 60
    if len(time_ints) == 2:
        return time_ints[0] + time_ints[-1] / 60
    else:
        return time_ints[-1] / 60
# %%
def return_timing_info(df_in, outname='', save = False):
    df_in = df_in[df_in['length'].apply(lambda x: isinstance(x,str))]
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
        # Remove title
        x.set_title("")
        # Set x-axis label
        x.set_xlabel("Video length (Minutes)", labelpad=20, weight='bold', size=12)
        # Set y-axis label
        x.set_ylabel("Frequency", labelpad=20, weight='bold', size=12)
        plt.xlim(0, 60)
    if save:
        plt.savefig(outname + '_time_info' + '.png')
    plt.show()
        
    return df_in["length (m)"], {"mean": df_in["length (m)"].mode()[0], "mode": df_in["length (m)"].mean()}
# %%
def fetch_transcript_list(df_in):
    return list(df_in['transcript'])
# %%
def fetch_wpm(df_in, outname = '', save= False):
    df_in = df_in[df_in['transcript'].apply(lambda x: isinstance(x,str))]
    df_in["length (m)"] = df_in["length"].apply(time_text_to_min)
    df_in["num_words"] = df_in['transcript'].str.split().apply(len)
    print(df_in.head())
    df_in["wpm"] = df_in["num_words"] / df_in["length (m)"]
    df_in = df_in[df_in['wpm'] < 800]
    ax = df_in.hist(column='wpm', bins=25, grid=False, figsize=(12,8), color='r', zorder=2, rwidth=0.9)
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
        # Remove title
        x.set_title("")
        # Set x-axis label
        x.set_xlabel("Words per minute", labelpad=20, weight='bold', size=12)
        # Set y-axis label
        x.set_ylabel("Frequency", labelpad=20, weight='bold', size=12)
        plt.xlim(100, 350)
    if save:
        plt.savefig(outname + "_wpm_freq" + '.png')
    plt.show()
    print(df_in["wpm"])
    mode = df_in["wpm"].mode()[0]
    mean = df_in["wpm"].mean()
    return {"mode": mode, "mean": mean}

# %%
def fetch_sponsor_rag(string_in):
    # TODO: SOME SPONSORS ARE MORE THAN ONE WORD! CAN'T JUST GO ONE WORD BACK
    words = string_in.split(' ')
    
    for i in range(len(words)):
        if 'sponsor' in words[i].lower():
            sponsor = words[i-3] + ' ' + words[i-2]
            print(sponsor)
            if sponsor.split(' ')[0] == 'to':
                return sponsor.split(' ')[-1]
            else:
                return sponsor
    return ''


# %%
def sponsor_from_df(df_in):
    df_in = df_in[df_in['description snippet'].apply(lambda x: isinstance(x,str))]
    return df_in['description snippet'].apply(fetch_sponsor_rag)


# %%
def sponsor_analysis(df_in, outname = '', save = False):
    init_frame = sponsor_from_df(df_in)
    frame = init_frame.to_frame()
    frame = frame.rename(columns={'description snippet': 'sponsors'})
    frame['sponsors'].str.replace("#", "")
    num_no_sponsor = frame.loc[frame['sponsors'] == ''].count().iloc[0]
    num_sponsor = len(init_frame) - num_no_sponsor
    
    labels = ['Unsponsored videos', 'Sponsored videos']
    fig, ax = plt.subplots()
    ax.pie([num_no_sponsor, num_sponsor], labels = labels)
    if save:
        plt.savefig(outname + "_sponsor_pie" + ".png")
    plt.show()
    
    frame['sponsors'].replace('', np.nan, inplace=True)
    frame.dropna(subset=['sponsors'], inplace=True)
    sponsor_freqs = frame['sponsors'].value_counts().head(20)
    sponsor_freqs.plot.bar()
    plt.xlabel("Sponsors")
    plt.ylabel("Frequency")
    plt.show()
    if save:
        plt.savefig(outname + "_sponsor_bar" + ".png")
    plt.show()
    
    return num_no_sponsor, sponsor_freqs


# %%
def partition_transcript(text):
    part_size = 30
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
        return pd.DataFrame(trans_sent, columns = ["Transcript Sentiments"])
    
    else:
        vid_names = df_in['Video Name'].tolist()
        preds = bp.make_pred(vid_names)
        return pd.DataFrame(preds, columns = ["Title Sentiments"])


# %%
def graph_sentiments(df_in, outname = '', transcript_bool = True, save = False):
    if transcript_bool:
        df_in = bert_sentiment(df_in, transcript_bool = transcript_bool)
        ax = df_in.hist(column='Transcript Sentiments', bins=25, grid=False, figsize=(12,8), color='m', zorder=2, rwidth=0.9)
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
            # Remove title
            x.set_title("")
            # Set x-axis label
            x.set_xlabel("Video Transcript Sentiment Polarity", labelpad=20, weight='bold', size=12)
            # Set y-axis label
            x.set_ylabel("Frequency", labelpad=20, weight='bold', size=12)
            plt.xlim(0, 1)
        if save:
            plt.savefig(outname + "_trans_sents" + '.png')
        plt.show()
    
    else:
        df_in = bert_sentiment(df_in, transcript_bool = transcript_bool)
        ax = df_in.hist(column='Title Sentiments', bins=25, grid=False, figsize=(12,8), color='c', zorder=2, rwidth=0.9)
        ax = ax[0]

        for x in ax:
            # Despine
            x.spines['right'].set_visible(False)
            x.spines['top'].set_visible(False)
            x.spines['left'].set_visible(False)

            # Switch off ticks
            x.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")
            # Draw horizontal axis lines
            # Remove title
            x.set_title("")
            # Set x-axis label
            x.set_xlabel("Video Title Sentiment Polarity", labelpad=20, weight='bold', size=12)
            # Set y-axis label
            x.set_ylabel("Frequency", labelpad=20, weight='bold', size=12)
            plt.xlim(0, 1)
        if save:
            plt.savefig(outname + "_title_sents" + '.png')
        plt.show()


# %%
def perform_analysis(df_in, outname, rag_df = False):
    mean_time_column, time_meanmode = return_timing_info(df_in, outname=outname, save = True)
    wpm_meanmode = fetch_wpm(df_in, outname=outname, save = True)
    graph_sentiments(df_in, outname = outname, transcript_bool = True, save = True)
    graph_sentiments(df_in, outname = outname, transcript_bool = False, save = True)
    if rag_df:
        sponsor_analysis(df_in, outname, save = True)
    aa.gen_wordcloud(fetch_transcript_list(df_in), outname = outname, save = True)
    return time_meanmode, wpm_meanmode


# %%
# cd ..

# %%
df = pd.read_csv(dir + 'JoshuaWeissmanVideosCleaned.csv')
analysis_portion = df.head(112)
perform_analysis(df, outname = dir + 'JoshuaWeissman', rag_df = True)

# %%
