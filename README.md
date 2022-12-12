# P-YUM
yum

How do we utilize the various ways of audience response to characterize and measure the engagement levels of different food YouTube content creators? **

Recipe content is especially interesting as one of the ultimate goals of the recipe creator is for audiences to replicate their work. 
There is a direct aspect of emulation and reproduction. This opens up avenues for much interesting inspection of how audiences engage with content creators.
Are audiences actively recreating recipes, and if so, are they deeming these to be good recipes? Challenging recipes? Overly convoluted recipes? Are the ingredients
mentioned in the recipes easy to source? There are a myriad of questions that arise when the audience has their own creative output that adds another layer to the usual
comment / social media text analysis.

## Part 1: Data and Metrics

We first need to determine the metrics we will be using and the data we will be collecting. There are a lot of different metrics that we can develop and narrowing
them down to representative and interesting ones to examine will be challenging.

Once we have adequate metrics, we will need data that we can actively perform analysis on. This will involve large amounts of scraping in social avenues such as Instagram,
Twitter, YouTube comments. An additional scraping component involves the use of the YouTube API, which will be used to scrap video data, transcripts, and other characteristics of the YouTube videos posted by creators.

## Part 2: Developing Models

We split our metrics into three parts: commercial, personability and entertainment, recipe quality. We develop models to computationally analyze each.

### Commercial

We analyze whether channels sell their own products and if they have sponsors as well as sponsor frequency. To do this, we scrape descriptions from videos to check for cookbooks and apply pre-built models to check if sponsorships exist in videos. We can see which sponsors most frequently sponsor which channels, how long the sponsorships run for, and when in the video sponsors pop up. This is done through a combination of scraping and existing neural networks that can extract sponsors from video transcripts.

### Personability and Entertainment

We want to know whether channels are purely focused on presenting recipes, or also seek to entertain audiences and market the creator as a central personability in videos. We check this through a couple of ways. We can see how often faces show up and the percentage of the screen a face occupies. We hypothesize that creators who care more about their own "personal brand" will show their face more in videos, whereas creators who purely care about presenting their recipes wil typically show more shots of food and less of their face. We use haar cascade and other CV methods to perform face detection.

We can also check the words-per-minute of videos. Typically videos that are fairly tight and mostly driven by the recipes will have more words per minute and will focus on quickly and compactly presenting the food and how to cook it. We perform this analysis by simply scraping the transcripts of videos, counting the amount of words, and then dividing by total time of video.

Another set of metrics we check are the sentiment scores of video titles and video transcripts. We hypothesize that video titles that are more polarizing tend to trend more towards "clickbait" and video transcripts that are more highly polarized tend to be geared towards entertaining audiences. We utilize a BERT model trained on the IMDB dataset.

### Recipe Quality

We investigate recipe quality through the amount of ingredients and instructions required to complete them. We hypothesize that recipes that are poorly developed and not suitable for the average person tend to be overly convoluted and have lots of ingredients and instructions. We believe this also extends into the "entertainment" part of things, as convoluted recipes can be more fun to watch and allow the creator to disply their technical skill. To accomplish an analysis of recipe complexity, we scrape recipe websites and use CRF, POS tagging, and other methods to grab out number of ingredients and steps.

