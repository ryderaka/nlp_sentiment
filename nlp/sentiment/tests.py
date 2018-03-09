from django.test import TestCase

import nltk
from nltk.classify import NaiveBayesClassifier


# def format_sentence(sent):
#     return({word: True for word in nltk.word_tokenize(sent)})

# print(format_sentence("The cat is very cute"))


sample_text = "Since the day I saw her 😍, I drowned 😘 into her eyes 🙈, smell of her hair 👩 is my drug. 😉"
sample_text2 = "THis is so awkward to seeee her like that :( , check her profile here: http://tinyurl.com/ThsSwl/"

from views import Sentiment

# print(Sentiment.emoji_polarity('', sample_text))

print(Sentiment(sample_text2).string_polarity())
