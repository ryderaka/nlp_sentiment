# Created by thoughtchimp on 27/12/17
# -*- coding: utf-8 -*-
import googletrans
translator = googletrans.Translator()


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
