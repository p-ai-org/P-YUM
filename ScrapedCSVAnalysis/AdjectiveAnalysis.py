# %%
import spacy
sp = spacy.load('en_core_web_sm')
import pandas as pd
import matplotlib.pyplot as plt
import multidict as multidict
from wordcloud import WordCloud
import re
import numpy as np

# %%
def get_POS(text):
    POS_arr = []
    for line in text:
        try:
            sent_pos_arr = []
            sent_tag_arr = []
            line = line.replace("\n", "")
            sp_out = sp(line)
            tokenized = []
            for token in sp_out:
                tokenized.append(token)
                sent_pos_arr.append(token.pos_)
                sent_tag_arr.append(token.tag_)
            text_pos_dict = {"text": tokenized, "pos": sent_pos_arr}
            POS_arr.append(text_pos_dict)
        except:
            continue
    return POS_arr
# %%
def get_adjectives(text):
    pos_arr = get_POS(text)
    all_adjectives = []
    for text in pos_arr:
        for i in range(len(text['pos'])):
            if text['pos'][i] == 'ADJ':
                all_adjectives.append(text['text'][i])
                
    return all_adjectives

# %%
def word_freq(words):
    wordfreq = {}
    for word in words:
        word = word.text.lower()
        if word not in wordfreq:
            wordfreq[word] = 0 
        wordfreq[word] += 1
    return wordfreq


# %%
def make_image(text, outname='', save = False):
    wc = WordCloud(background_color="white", max_words=20)
    # generate word cloud
    wc.generate_from_frequencies(text)

    # show
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    if save:
        plt.savefig(outname + 'wordfreq.png')
    plt.show()

# %%
def gen_wordcloud(text, outname = '', save = False):
    adj_list = get_adjectives(text)
    wordfreq = word_freq(adj_list)
    make_image(wordfreq, outname = outname, save = save)
