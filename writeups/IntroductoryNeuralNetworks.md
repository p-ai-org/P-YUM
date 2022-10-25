## Introduction to Neural Networks (CNN and Transformers with BERT)

### Convolutional Neural Network Notebook (Example)

This notebook is designed as an example look through. It covers the basic building of a convolutional neural network with pytorch. The first example is a simple baseline example that covers a linear model, while the second example is a bit more complex and goes through the steps to creating a model with more layers and a more interesting architecture.

You should read through the notebook and try and look up info that you think is unclear. I would not worry about trying to figure out what exactly is going on. Just try to get a baseline understanding of the processes and get a very high-level overview of what is going on. I would look through this one before moving on to the exercise.

### Sentiment Analysis Notebook (Exercise)

This notebook is an on-rails exercise to training a sentiment analysis model. It utilizes Transformers and BERT, which are currently the most popular and state-of-the-art models for a lot of NLP tasks. You can opt to run this notebook on a high-performance server if you have access to one, or you can opt to run it in Google Colab, which has cloud GPU support.

We will most likely be using sentiment analysis in this project, though the model you train here probably won't be the optimal model for our use case. Sentiment analysis is basically a method to quantify how positive or negative text is. It is a continuous task, and will typically yield a value from a range of 0 to 1, with 0 being most negative and 1 being most positive.

Throughout this notebook, you will come across the basic pre-processing pipeline used in a lot of NLP-based machine learning tasks, as well as how to work with BERT and Transformers. This may seem incredibly intimidating at first, but I encourage you to fully utilize online resources such as stack overflow, google, etc. You should feel free to copy and paste code from other tutorials and Frankenstein together answers to the questions.

This is an incredibly complex example and you may not be able to answer all the questions or quite understand what exactly you are doing. This is fine. The goal is just to try and go through the motions for training a neural network and understanding some of the steps that go into it.