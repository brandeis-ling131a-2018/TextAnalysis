"""main_a3.py


"""

import re
import os
import math

import nltk
from nltk.corpus import brown
from nltk.corpus import wordnet as wn
from nltk.corpus import PlaintextCorpusReader

from fsa import FSA


# NLTK stoplist with 3136 words (multilingual)
STOPLIST = set(nltk.corpus.stopwords.words())

# Vocabulary with 234,377 English words from NLTK
ENGLISH_VOCABULARY = set(w.lower() for w in nltk.corpus.words.words())

# The five categories from Brown that we are using
BROWN_CATEGORIES = ('adventure', 'fiction', 'government', 'humor', 'news')

# Global place to store Brown vocabularies so you calculate them only once
BROWN_VOCABULARIES = None


def is_content_word(word):
    """A content word is not on the stoplist and its first character is a letter."""
    return word.lower() not in STOPLIST and word[0].isalpha()


class Text(object):
    
    def __init__(self, path, name=None):
        """Takes a file path, which is assumed to point to a file or a directory, 
        extracts and stores the raw text and also stores an instance of nltk.text.Text."""
        self.name = name
        if os.path.isfile(path):
            self.raw = open(path).read()
        elif os.path.isdir(path):
            corpus = PlaintextCorpusReader(path, '.*.mrg')
            self.raw = corpus.raw()
        self.text = nltk.text.Text( nltk.word_tokenize(self.raw))

    def __len__(self):
        return len(self.text)

    def __getitem__(self, i):
        return self.text[i]

    def __str__(self):
        name = '' if self.name is None else " '%s'" % self.name 
        return "<Text%s tokens=%s>" % (name, len(self))

    def token_count(self):
        """Just return the length of the text."""
        return len(self)

    def type_count(self):
        """Returns the type count, with minimal normalization by lower casing."""
        # an alternative would be to use the method nltk.text.Text.vocab()
        return len(set([w.lower() for w in self.text]))

    def sentence_count(self):
        """Return number of sentences, using the simplistic measure of counting period,
        exclamation marks and question marks."""
        # could also use nltk.sent.tokenize on self.raw
        return len([t for t in self.text if t in '.!?'])

    def most_frequent_content_words(self):
        """Return a list with the 25 most frequent content words and their
        frequencies. The list has (word, frequency) pairs and is ordered
        on the frequency."""
        dist = nltk.FreqDist([w for w in self.text if is_content_word(w.lower())])
        return dist.most_common(n=25)

    def most_frequent_bigrams(self, n=25):
        """Return a list with the 25 most frequent bigrams that only contain
        content words. The list returned should have pairs where the first
        element in the pair is the bigram and the second the frequency, as in
        ((word1, word2), frequency), these should be ordered on frequency."""
        filtered_bigrams = [b for b in list(nltk.bigrams(self.text))
                            if is_content_word(b[0]) and is_content_word(b[1])]
        dist = nltk.FreqDist([b for b in filtered_bigrams])
        return dist.most_common(n=n)

    def concordance(self, word):
        self.text.concordance(word)

    ## new methods for search part of assignment 3
    
    def search(self, pattern):
        return re.finditer(pattern, self.raw)

    def find_sirs(self):
        answer = set()
        for match in self.search(r"\bSir \S+\b"):
            answer.add(match.group())
        return sorted(answer)

    def find_brackets(self):
        answer = set()
        # use a non-greedy match on the characters between the brackets
        for match in self.search(r"([\(\[\{]).+?([\)\]\}])"):
            brackets = "%s%s" % (match.group(1), match.group(2))
            # this tests for matching pairs
            if brackets in ['[]', '{}', '()']:
                answer.add(match.group())
        return sorted(answer)

    def find_roles(self):
        answer = set()
        for match in re.finditer(r"^([A-Z]{2,}[^\:]+): ", self.raw, re.MULTILINE):
            answer.add(match.group(1))
        return sorted(answer)

    def find_repeated_words(self):
        answer = set()
        for match in self.search(r"(\w{3,}) \1 \1"):
            answer.add(match.group())
        return sorted(answer)

    def apply_fsa(self, fsa):
        i = 0
        results = []
        while i < len(self):
            match = fsa.consume(self.text[i:])
            if match:
                results.append((i, match))
                i += len(match)
            else:
                i += 1
        return results


class Vocabulary():

    """Class to store all information on a vocabulary, where a vocabulary is created
    from a text. The vocabulary includes the text, a frequency distribution over
    that text, the vocabulary items themselves (as a set) and the sizes of the
    vocabulary and the text. We do not store POS and gloss, for those we rely on
    WordNet. The vocabulary is contrained to those words that occur in a
    standard word list. Vocabulary items are not normalized, except for being in
    lower case."""

    def __init__(self, text):
        self.text = text.text
        # keeping the unfiltered list around for statistics
        self.all_items = set([w.lower() for w in text])
        self.items = self.all_items.intersection(ENGLISH_VOCABULARY)
        # restricting the frequency dictionary to vocabulary items
        self.fdist = nltk.FreqDist(t.lower() for t in text if t.lower() in self.items)
        self.text_size = len(self.text)
        self.vocab_size = len(self.items)

    def __str__(self):
        return "<Vocabulary size=%d text_size=%d>" % (self.vocab_size, self.text_size)

    def __len__(self):
        return self.vocab_size

    def frequency(self, word):
        return self.fdist[word]

    def pos(self, word):
        # do not volunteer the pos for words not in the vocabulary
        if word not in self.items:
            return None
        synsets = wn.synsets(word)
        # somewhat arbitrary choice to make unknown words nouns, returning None
        # or 'UNKNOWN' would have been fine too.
        return synsets[0].pos() if synsets else 'n'
    
    def gloss(self, word):
        # do not volunteer the gloss (definition) for words not in the vocabulary
        if word not in self.items:
            return None
        synsets = wn.synsets(word)
        # make a difference between None for words not in vocabulary and words
        # in the vocabulary that do not have a gloss in WordNet
        return synsets[0].definition() if synsets else 'NO DEFINITION'

    def kwic(self, word):
        self.text.concordance(word)
        


