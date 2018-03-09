
# coding: utf-8

# In[18]:


import re
# import nltk
#
# import pandas as pd
# import numpy as np

from bs4 import BeautifulSoup
from nltk.corpus import stopwords


class VecUtility(object):
    
    # Define a method to create bag of words out of tweets
    @staticmethod
    def tweet_to_wordlist( tweet, remove_stopwords=False ):
        
        tweet_text = BeautifulSoup(tweet).get_text()
        tweet_text = re.sub("[^a-zA-Z]"," ", tweet_text)
        
        words = tweet_text.lower().split()
       
        if remove_stopwords:
            stops = set(stopwords.words("english"))
            words = [w for w in words if not w in stops]
        
        return(words)

    # Define a function to split a tweet
    @staticmethod
    def tweet_to_sentences( tweet, tokenizer, remove_stopwords=False ):
       
        raw_sentences = tokenizer.tokenize(tweet.decode('utf8').strip())
        
        sentences = []
        for raw_sentence in raw_sentences:
            
            if len(raw_sentence) > 0:
               
                sentences.append( VecUtility.tweet_to_wordlist( raw_sentence,remove_stopwords ))
        
        return sentences


# In[5]:


import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

if __name__ == '__main__':
    train = pd.read_csv('trainingDatasetProcessed.csv', header=0,delimiter="\t", quoting=3)
    test = pd.read_csv('first_pass_result.csv', header=0, delimiter=",",quoting=3 )



    print('Download text data sets. If you already have NLTK datasets downloaded, just close the Python download window...')
    #nltk.download()  # Download text data sets, including stop words

    # Initialize an empty list to hold the clean tweets
    clean_train_tweets = []

    print("Cleaning and parsing the training set tweets...\n")
    for i in range( 0, len(train["tweet"])):
        clean_train_tweets.append(" ".join(VecUtility.tweet_to_wordlist(train["tweet"][i], True)))
    print(clean_train_tweets)

    print("Creating the bag of words...\n")

    # Initialize the "CountVectorizer" object, which is scikit-learn's
    # Kind of document term Matrix
    vectorizer = CountVectorizer(analyzer = "word",tokenizer = None,preprocessor = None, stop_words = None, max_features = 5000)

    train_data_features = vectorizer.fit_transform(clean_train_tweets)

    train_data_features = train_data_features.toarray()
    print(train_data_features)


    print("Training the random forest (this may take a while)...")


    # Initialize a Random Forest classifier with 100 trees
    forest = RandomForestClassifier(n_estimators = 100)

    
    forest = forest.fit( train_data_features, train["sentiment"] )



    # Create an empty list and append the clean tweets one by one
    clean_test_tweets = []

    print("Cleaning and parsing the test set movie tweets...\n")
    for i in range(0,len(test['0'])):
        clean_test_tweets.append(" ".join(VecUtility.tweet_to_wordlist(test['0'][i], True)))

    # Get a bag of words for the test set, and convert to a numpy array
    test_data_features = vectorizer.transform(clean_test_tweets)
    test_data_features = test_data_features.toarray()

    # Use the random forest to make sentiment label predictions
    print("Predicting test labels...\n")
    result = forest.predict(test_data_features)

    # Copy the results to a pandas dataframe with an "id" column and
    # a "sentiment" column
    output = pd.DataFrame( data={"id":test["id"], "sentiment":result} )

    # Use pandas to write the comma-separated output file
    output.to_csv('predict.csv', index=False, quoting=3)
    print("Wrote results to predict.csv")
