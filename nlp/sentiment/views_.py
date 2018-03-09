from django.shortcuts import render
from django.utils.lorem_ipsum import sentence

from nltk.corpus import stopwords

import re
import html
import nltk
from nltk import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import movie_reviews
import itertools
from nltk.classify import NaiveBayesClassifier

# from autocorrect import spell

nltk.download('stopwords')
# nltk.download()


class Sentiment:
    def __init__(self):
        pass

    def emoji_polarity(self, string):
        pol_sum = 0
        polarity_set = {'👿': -5, '😾': -5, '😡': -5, '😠': -4, '😧': -4, '😭': -4, '😱': -4, '🙀': -4, '😈': -4,
                        '😟': -4, '😿': -2, '😕': -2, '😖': -2, '😰': -2, '😢': -2, '😞': -2, '😳': -2, '😨': -2,
                        '😬': -2, '😮': -2, '😣': -2, '😫': -2, '😒': -2, '😩': -2, '😵': -1, '😥': -1, '😦': -1,
                        '😁': -1, '😯': -1, '😷': -1, '😔': -1, '😓': -1, '😜': -1, '😑': 0, '😶': 0, '😐': 0, '😴': 0,
                        '😝': 0, '😪': 0, '😆': 1, '😎': 1, '😛': 1, '😲': 3, '😊': 3, '😀': 3, '😽': 3, '😙': 3,
                        '😗': 3, '😚': 3, '☺️': 3, '😌': 3, '😄': 3, '😼': 3, '😸': 3, '😃': 3, '😺': 3, '😅': 3,
                        '😏': 3, '😻': 4, '😍': 4, '😇': 4, '😂': 4, '😹': 4, '😘': 4, '😉': 4, '😋': 4, '🤗': 4,
                        '😤': 5}

        for char in string:
            if char in polarity_set:
                pol_sum+=polarity_set[char]
                if pol_sum > 5:
                    pol_sum = 5
                elif pol_sum < -5:
                    pol_sum = -5

        print({string: pol_sum})
        return {string: pol_sum}

    def get_word_feature(self, sentence1):
        print('inside, ', sentence1)
        # ToDo
        # sentence translation to english

        sentence1 = sentence1.lower()
        sentence1 = html.unescape(sentence1)

        # remove URLs
        sentence1 = re.sub(r'https?:\/\/.*[\r\n]*', '', sentence1, flags=re.MULTILINE)
        print(sentence1)

        # Standardizing words
        sentence1 = ''.join(''.join(s)[:2] for _, s in itertools.groupby(sentence1))
        print('....', sentence1)

        # sentences = sent_tokenize(sentence1)
        # print(sentences)

        # porter_stemmer = nltk.stem.PorterStemmer()
        # print(porter_stemmer.stem(word))

        # Tokenize
        tokens = word_tokenize(sentence1)
        print(tokens)

        # is word
        words = [word for word in tokens if word.isalpha()]
        print(words)

        # remove stop words
        stop_words = set(stopwords.words('english'))
        filtered_sentence = [w for w in words if not w in stop_words]
        print(filtered_sentence)
        my_dict = dict([(word, True) for word in filtered_sentence])
        return my_dict

    def string_polarity(self, sentence1):
        print(sentence1)
        result = self.get_word_feature(sentence1)
        print(result)
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
            print(neg_reviews[0])
            print(len(pos_reviews))




    def string_polarity_temp(self, sentence1):
        # res = [spell(r) for r in filtered_sentence]
        # print('l', res)

        # for item in filtered_sentence:
        #     if item not in stop_words:
        #         list1.append(item)

        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.ensemble import RandomForestClassifier
        import pandas as pd

        clean_train_tweets = []
        train = pd.read_csv('trainingDatasetProcessed.csv', header=0, delimiter="\t", quoting=3)
        vectorizer = CountVectorizer(analyzer="word", tokenizer=None, preprocessor=None, stop_words=None,
                                     max_features=5000)
        train_data_features = vectorizer.fit_transform(clean_train_tweets)

        train_data_features = train_data_features.toarray()

        forest = RandomForestClassifier(n_estimators=100)       # training using random forest with 100 trees

        forest = forest.fit(train_data_features, train["sentiment"])

        print(forest)

        neg_review = []
        for id in movie_reviews.fileids('neg'):
            words = movie_reviews.words(id)
            neg_review.append()
