# Created by thoughtchimp on 27/12/17
# -*- coding: utf-8 -*-

import re
import html
from nltk.classify import NaiveBayesClassifier
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import itertools
from .emojis import polarity_set
from .translator import Translator

import os
dir_path = os.path.dirname(os.path.realpath(__file__))

from nltk.stem.porter import PorterStemmer
porter = PorterStemmer()


class Sentiment:
    _polarity = None

    def __init__(self, sentence):
        self.sentence = sentence

    def get_classifier(self):
        print(self.sentence)
        print('start reading')
        print('pos')
        train_pos = pd.read_csv(os.path.join(dir_path, 'positive_sentences.csv'), header=0, delimiter=",", quoting=3, error_bad_lines=False)
        print('neg')
        train_neg = pd.read_csv(os.path.join(dir_path, 'negative_sentences.csv'), header=0, delimiter=",", quoting=3, error_bad_lines=False)
        print('neu')
        train_neu = pd.read_csv(os.path.join(dir_path, 'neutral_sentences.csv'), header=0, delimiter=",", quoting=3, error_bad_lines=False)
        print('ended reading')

        pos_feature = [(self.cleaned_data(line, featured=True), 'positive') for line in train_pos["text"]]
        neg_feature = [(self.cleaned_data(line, featured=True), 'negative') for line in train_neg["text"]]
        neu_feature = [(self.cleaned_data(line, featured=True), 'neutral') for line in train_neu["text"]]

        train_set = pos_feature + neg_feature + neu_feature

        classifier = NaiveBayesClassifier.train(train_set)
        return classifier

    def emoji_polarity(self):
        neg = pos = neu = 0
        pol_sum = 0
        for char in self.sentence:
            if char in polarity_set:
                pol = polarity_set[char]
                if pol == 0:
                    neu += 1
                pol_sum += abs(polarity_set[char])
                if pol > 0:
                    pos += pol
                if pol < 0:
                    neg += pol
        per_emo = (100/(pol_sum+neu)) if (pol_sum+neu) is not 0 else 0
        positive_pct = pos*per_emo/100
        negative_pct = neg*per_emo/100
        neutral_pct = neu*per_emo/100
        return {'positive': positive_pct, 'negative': negative_pct, 'neutral': neutral_pct}

    @staticmethod
    def word_fetured(text):
        return dict([(word, True) for word in text])

    def cleaned_data(self, input_string, featured=False):
        sentence = html.unescape(input_string.lower())
        # remove URLs
        sentence = re.sub(r'https?:\/\/.*[\r\n]*', '', sentence, flags=re.MULTILINE)
        # Standardizing words
        sentence = ''.join(''.join(s)[:2] for _, s in itertools.groupby(sentence))
        # Tokenize
        tokens = word_tokenize(sentence)
        # is word
        words = [word for word in tokens if word.isalpha()]
        # remove stop words
        stop_words = set(stopwords.words('english'))
        filtered_sentence = [w for w in words if not w in stop_words]
        # Stemming - reducing each word to its root or base.
        stemmed = [porter.stem(word) for word in filtered_sentence]
        if featured:
            stemmed = self.word_fetured(stemmed)
        return stemmed

    def string_polarity(self):

        pos = neg = neu = 0
        classifier = self.get_classifier()
        # sentence = Translator(self.sentence).translate()

        cleaned_text_list = list(self.cleaned_data(self.sentence))

        for word in cleaned_text_list:

            classified = classifier.classify(dict([(word, True)]))
            print(word, classified)
            if classified == 'positive':
                pos += 1
            if classified == 'negative':
                neg += 1
            if classified == 'neutral':
                neu += 1

        positive = (float(pos) / len(cleaned_text_list)) if len(cleaned_text_list) > 0 else 0
        negative = (float(neg) / len(cleaned_text_list)) if len(cleaned_text_list) > 0 else 0
        neutral = (float(neu) / len(cleaned_text_list)) if len(cleaned_text_list) > 0 else 0
        self._polarity = {'positive': positive, 'negative': negative, 'neutral': neutral}
        return self._polarity

    def get_polarity(self):
        print('-'*100)
        emoji_pol = self.emoji_polarity()

        str_pol = self.string_polarity()
        pol_sum = (sum(set(emoji_pol.values())) + sum(set(str_pol.values())))
        pos_pol = (emoji_pol['positive'] + str_pol['positive'])/2 if pol_sum > 1 else (emoji_pol['positive'] + str_pol['positive'])
        neg_pol = (emoji_pol['negative'] + str_pol['negative'])/2 if pol_sum > 1 else (emoji_pol['negative'] + str_pol['negative'])
        neu_pol = (emoji_pol['neutral'] + str_pol['neutral'])/2 if pol_sum > 1 else (emoji_pol['neutral'] + str_pol['neutral'])

        return {'positive': pos_pol, 'negative': neg_pol, 'neutral': neu_pol}

    def get_mood(self):
        mood = self._polarity if self._polarity is not None else self.get_polarity()
        if mood['positive'] > mood['negative']:
            return 'positive'
        elif mood['negative'] > mood['positive']:
            return 'negative'
        return 'neutral'

# Sentiment('The feelings i had for her , the love and hate').get_mood()
# print(Sentiment(' 😘 ').emoji_polarity())
# print(Sentiment(' hello i am also happy ').string_polarity())

