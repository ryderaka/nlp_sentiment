# Created by thoughtchimp on 27/12/17
# -*- coding: utf-8 -*-
import re
import html
from nltk.classify import NaiveBayesClassifier
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import itertools

import googletrans
translator = googletrans.Translator()

from nltk.stem.porter import PorterStemmer
porter = PorterStemmer()


class Translator:
    def __init__(self, sentence):
        self.sentence = sentence

    def languages_code(self):   # to get all supported languages with their code
        return googletrans.LANGUAGES

    def get_language(self):  # detect language of input string
        return translator.detect(self.sentence).lang

    def translate(self, convert_from='auto', convert_to='en'):   # language conversion
        sentence = translator.translate(self.sentence, src=convert_from, dest=convert_to).text
        return sentence


class Sentiment:
    def __init__(self, sentence):
        self.sentence = sentence

    def emoji_polarity(self):
        pol_sum = 0
        for char in self.sentence:
            if char in polarity_set:
                pol_sum += polarity_set[char]
                if pol_sum > 5:
                    pol_sum = 5
                elif pol_sum < -5:
                    pol_sum = -5

        print({string: pol_sum})
        return {string: pol_sum}

