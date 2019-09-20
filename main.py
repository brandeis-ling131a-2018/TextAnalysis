"""main.py

Code scaffolding

"""

import os
import nltk
from nltk.corpus import brown
from nltk.corpus import wordnet as wn
from nltk.corpus import PlaintextCorpusReader
from nltk.probability import FreqDist
from nltk.text import Text


def read_text(path):
    pass


def token_count(text):
    pass


def type_count(text):
    pass


def sentence_count(text):
    pass


def most_frequent_content_words(text):
    pass


def most_frequent_bigrams(text):
    pass


class Vocabulary():

    def __init__(self, text):
        pass

    def frequency(self, word):
        pass

    def pos(self, word):
        pass

    def gloss(self, word):
        pass

    def quick(self, word):
        pass


categories = ('adventure', 'fiction', 'government', 'humor', 'news')


def compare_to_brown(text):
    pass



if __name__ == '__main__':

    text = read_text('data/grail.txt')
    token_count(text)
