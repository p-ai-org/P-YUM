# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import importlib
import AdjectiveAnalysis as aa

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
ramsay_df = pd.read_csv(dir + "GordonRamsayVideos.csv")
fetch_wpm(ramsay_df)
# %%
aa.gen_wordcloud(text)
# %%
