# Created by thoughtchimp on 21/12/17
# -*- coding: utf-8 -*-

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import names


def word_feats(words):
    return dict([(word, True) for word in words])

positive_vocab = [ 'awesome', 'outstanding', 'fantastic', 'terrific', 'good', 'nice', 'great', ':)' ]
negative_vocab = [ 'bad', 'terrible','useless', 'hate', ':(' ]
neutral_vocab = [ 'movie','the','sound','was','is','actors','did','know','words','not' ]

positive_features = [(word_feats(pos), 'pos') for pos in positive_vocab]
negative_features = [(word_feats(neg), 'neg') for neg in negative_vocab]
neutral_features = [(word_feats(neu), 'neu') for neu in neutral_vocab]

train_set = positive_features + negative_features + neutral_features
print(train_set)

classifier = NaiveBayesClassifier.train(train_set)

# Predict
neg = 0
pos = 0
sentence = "I hate when she ignores me "
sentence = sentence.lower()
words = sentence.split(' ')
for word in words:
    classResult = classifier.classify(word_feats(word))
    print(classResult)
    if classResult == 'neg':
        neg = neg + 1
    if classResult == 'pos':
        pos = pos + 1
print(pos, neg)
print(len(words))
print('Positive: ' + str(float(pos)/len(words)))
print('Negative: ' + str(float(neg)/len(words)))
