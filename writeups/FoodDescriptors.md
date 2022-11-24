# Getting Food Descriptors
What kind of adjectives do creators use to describe food? Are they more accessible, such as good, bad, flavorful, or more "highbrow", such as silky, umami, unctuous? We want to develop a scheme that allows us to read in a YouTube video transcript and extract out adjectives that describe food.

## Possible Things to Investigate
- We can initially use part of speech tagging and just see what words you get when you extract all adjectives from a text
- This can perhaps be extended to adjectives contained in the same sentence as a food item

## Useful Links and Resources
- https://stackoverflow.com/questions/43909954/extracting-food-items-from-sentences: A thread on extracting food items from sentences
- https://academic.oup.com/database/article/doi/10.1093/database/baz121/5611291: A corpus of foods - can be used to train a NER model for tagging food-entities in text
- https://datascience.stackexchange.com/questions/41285/any-efficient-way-to-find-surrounding-adjective-verbs-with-respect-to-the-target: A thread on finding adjectives corresponding to a target phrase. This can be perhaps used to find adjectives targetting foods.