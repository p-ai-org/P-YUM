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
def read_recipe(path_in):
    recipe_file = open(path_in, "r")
    #read whole file to a string
    ingredient_text = [x for x in recipe_file.readlines() if x]
    recipe_file.close()
    
    return ingredient_text

# %%
def get_POS(path_in):
    text = read_recipe(path_in)
    POS_arr = []
    for line in text:
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
    return POS_arr
# %%
def get_adjectives(path_in):
    pos_arr = get_POS(path_in)
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
def make_image(text):
    wc = WordCloud(background_color="white", max_words=10)
    # generate word cloud
    wc.generate_from_frequencies(text)

    # show
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()

# %%
def gen_wordcloud(path_in):
    adj_list = get_adjectives(path_in)
    wordfreq = word_freq(adj_list)
    make_image(wordfreq)
    
# %%
gen_wordcloud('lasagna_sample.txt')
# %%
