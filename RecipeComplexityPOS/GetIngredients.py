# %%
import spacy
sp = spacy.load('en_core_web_sm')
from quantulum3 import parser

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
        for token in sp_out:
            sent_pos_arr.append(token.pos_)
            sent_tag_arr.append(token.tag_)
        text_pos_dict = {"text": line, "pos": sent_pos_arr, "tags": sent_tag_arr}
        POS_arr.append(text_pos_dict)
    return POS_arr

# %%
def extract_ingredients(path_in):
    ingredient_sents = []
    pos_dict_arr = get_POS(path_in)
    poss_comb = [('NUM', 'NOUN'), ('NUM', 'VERB', 'NOUN'), ('NUM', 'PROPN')]
    bad_tags = ['PRP$', 'PRP']
    for text_dict in pos_dict_arr:
        unit_bool = False
        try:
            units = parser.parse(text_dict['text'])
            if units:
                for unit_meas in units:
                    if unit_meas.unit.name != 'dimensionless':
                        unit_bool = True
                        break
        except:
            continue
        if unit_bool or any(x in poss_comb for x in zip(text_dict['pos'], text_dict['pos'][1:])) or \
            any(x in poss_comb for x in zip(text_dict['pos'], text_dict['pos'][1:], text_dict['pos'][2:])) or \
                ('PRP$' not in text_dict['tags'] and 'PRP' not in text_dict['tags']):
            ingredient_sents.append(text_dict)
            
    return ingredient_sents
# %%
list = extract_ingredients("lasagna_sample.txt")
for item in list:
    print(item['text'])
# %%
