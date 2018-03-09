# Created by thoughtchimp on 22/12/17
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

    def text_translation(self, sentence, dest='en'):
        sentence = translator.translate(sentence, dest=dest).text
        return sentence

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
                pol_sum += polarity_set[char]
                if pol_sum > 5:
                    pol_sum = 5
                elif pol_sum < -5:
                    pol_sum = -5

        print({string: pol_sum})
        return {string: pol_sum}

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

        train_pos = pd.read_csv('positive_sentences.csv', header=0, delimiter=",", quoting=3, error_bad_lines=False)
        train_neg = pd.read_csv('negative_sentences.csv', header=0, delimiter=",", quoting=3, error_bad_lines=False)
        train_neu = pd.read_csv('neutral_sentences.csv', header=0, delimiter=",", quoting=3, error_bad_lines=False)

        pos_feature = [(self.cleaned_data(line, featured=True), 'positive') for line in train_pos["text"]]
        neg_feature = [(self.cleaned_data(line, featured=True), 'negative') for line in train_neg["text"]]
        neu_feature = [(self.cleaned_data(line, featured=True), 'neutral') for line in train_neu["text"]]
        # print(train_neg["text"])

        train_set = pos_feature + neg_feature + neu_feature
        # print(train_set)

        classifier = NaiveBayesClassifier.train(train_set)

        sentence = "A great day in New Hampshire and Maine. Fantastic crowds and energy! #MAGA"
        sentence = self.text_translation(sentence)

        cleaned_text = list(self.cleaned_data(sentence))
        print(cleaned_text)

        classresult = classifier.classify(self.cleaned_data(sentence))
        return classresult

print(Sentiment('name').string_polarity())
