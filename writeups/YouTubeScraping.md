## YouTube Scraping

### Part 1: Getting acquainted
- Register a Google development account for use with the YouTube API. Some info can be found here: https://developers.google.com/youtube
- Look through documentation and examples and try and get a basic pipeline working
- Explore some basic parameters and mess around with what data can be queried
- Useful links:
  - https://developers.google.com/youtube/v3/quickstart/python
  - https://medium.com/mcd-unison/youtube-data-api-v3-in-python-tutorial-with-examples-e829a25d2ebd
  - https://towardsdatascience.com/tutorial-using-youtubes-annoying-data-api-in-python-part-1-9618beb0e7ea
  - I have also pushed two examples on using the YouTube API, found in examples/scraping. They are from a few years ago so there may be some major deprecation

### Part 2: Getting the data we want

- Figure out how to query the YouTube API to get some data that might be interesting for us to study
- Develop a robust and extendable pipeline that allows us to query mass amounts of data and tweak parameters
- Make sure that this pipeline gets the data and writes it to a csv or json in a scalable manner so we can get mass amounts of data that we can then easily read in
- Write up any concerns, limitations, or notes that may be useful that you come across on the journey