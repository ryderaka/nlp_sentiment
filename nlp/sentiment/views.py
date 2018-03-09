import re
import html
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import movie_reviews
import itertools


class Sentiment:
    def __init__(self, sentence1):
        self.sentence1 = sentence1

    def get_word_feature(self, words):
        useful_words = [word for word in words if word not in stopwords.words("english")]
        my_dict = dict([(word, True) for word in useful_words])
        return my_dict

    def string_polarity(self):
        print(self.sentence1)
        sentence = self.sentence1.split(" ")
        result = self.get_word_feature(sentence)
        print(result)
        # create a word corpus from traines data and vectorise that

        neg_reviews = []
        for fileid in movie_reviews.fileids('neg'):
            words = movie_reviews.words(fileid)
            neg_reviews.append((self.get_word_feature(words), "negative"))
        print(neg_reviews[0])
        print(len(neg_reviews))

        pos_reviews = []
        for fileid in movie_reviews.fileids('pos'):
            words = movie_reviews.words(fileid)
            pos_reviews.append((self.get_word_feature(words), "positive"))
        print(pos_reviews[0])
        print(len(pos_reviews))
