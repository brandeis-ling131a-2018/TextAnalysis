"""main.py

Example Text Analysis code after assignment 2.

"""

import os
import math

import nltk
from nltk.corpus import brown
from nltk.corpus import wordnet as wn
from nltk.corpus import PlaintextCorpusReader
from nltk.probability import FreqDist
from nltk.text import Text


# NLTK stoplist with 3136 words (multilingual)
STOPLIST = set(nltk.corpus.stopwords.words())

# Vocabulary with 234,377 English words from NLTK
ENGLISH_VOCABULARY = set(w.lower() for w in nltk.corpus.words.words())

# The five categories from Brown that we are using
BROWN_CATEGORIES = ('adventure', 'fiction', 'government', 'humor', 'news')

# Global place to store Brown vocabularies so you calculate them only once
BROWN_VOCABULARIES = None


### PART 1: reading source data

def read_text(path):
    """Takes a file path, which is assumed to point to a file or a directory,
    and returns a Text instance."""
    if os.path.isfile(path):
        with open(path) as fh:
            return Text(nltk.word_tokenize(fh.read()))
    elif os.path.isdir(path):
        # restrict to files with the mrg extension, avoiding hidden files like .DS_Store
        # that can cause trouble
        corpus = PlaintextCorpusReader(path, '.*.mrg')
        return Text(nltk.word_tokenize(corpus.raw()))


### PART 2: simple statistics

# Total number of sentences, word types and word tokens

def token_count(text):
    """Just return all tokens."""
    return len(text)

def type_count(text):
    """Returns the type count, with minimal normalization by lower casing."""
    # an alternative would be to use the method nltk.text.Text.vocab()
    return len(set([w.lower() for w in text]))

def sentence_count(text):
    """Return number of sentences, using the simplistic measure of counting period,
    exclamation marks and question marks."""
    return len([t for t in text if t in ('.', '!', '?')])

def is_content_word(word):
    """A content word is not on the stoplist and its first character is a letter."""
    return word.lower() not in STOPLIST and word[0].isalpha()

def most_frequent_content_words(text):
    """Return a list with the 25 most frequent content words and their
    frequencies. The list has (word, frequency) pairs and is ordered on the
    frequency."""
    dist = FreqDist([w for w in text if is_content_word(w)])
    return dist.most_common(n=25)

def most_frequent_bigrams(text):
    """Return a list with the 25 most frequent bigrams that only contain
    content words. The list returned should have pairs where the first
    element in the pair is the bigram and the second the frequency, as in
    ((word1, word2), frequency), these should be ordered on frequency."""
    filtered_bigrams = [b for b in list(nltk.bigrams(text))
                        if is_content_word(b[0]) and is_content_word(b[1])]
    dist = nltk.FreqDist([b for b in filtered_bigrams])
    return dist.most_common(n=25)


### PART 3: Vocabulary

class Vocabulary():

    """Class to store all information on a vocabulary, where a vocabulary is created
    from a text. The vocabulary includes the text, a frequency distribution over
    that text, the vocabulary items themselves (as a set) and the sizes of the
    vocabulary and the text. We do not store POS and gloss, for those we rely on
    WordNet. The vocabulary is contrained to those words that occur in a
    standard word list. Vocabulary items are not normalized, except for being in
    lower case."""

    def __init__(self, text):
        self.text = text
        # keeping the unfiltered list around for statistics
        self.all_items = set([w.lower() for w in text])
        self.items = self.all_items.intersection(ENGLISH_VOCABULARY)
        # restricting the frequency dictionary to vocabulary items
        self.fdist = FreqDist(t.lower() for t in text if t.lower() in self.items)
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


### PART 4: comparison to Brown

def get_category_vocabs(categories):
    """Returns a dictionary of vocabularies indexed on category names."""
    vocabs = {}
    for cat in categories:
        words = brown.words(categories=[cat])
        vocabs[cat] = Vocabulary(Text(words))
    return vocabs

def get_text_vocabs():
    """Returns a dictionary of vocabularies indexed on category names."""
    return {
        'grail': Vocabulary(read_text('data/grail.txt')),
        'emma': Vocabulary(read_text('data/emma.txt')),
        'wsj': Vocabulary(read_text('data/wsj')) }

def print_vocabs(text_vocabs, category_vocabs):
    # helper function so we can see what we did
    print("%-10s  %s" % ('grail', text_vocabs['grail']))
    print("%-10s  %s" % ('emma', text_vocabs['emma']))
    print("%-10s  %s\n" % ('wsj', text_vocabs['wsj']))
    for cat in category_vocabs:
        print("%-10s  %s" % (cat, category_vocabs[cat]))

def get_dimensions(category_vocabs, debug=False):
    """Get the dimensions from the category vocabularies by collecting all elements
    in the vocabularies. Return the dimensions as a sorted list, with fixed
    positions for each dimension (word)."""
    dimensions = set()
    for cat, vocab in category_vocabs.items():
        # add elements from the vocabulary
        dimensions.update(vocab.items)
        if debug:
            print("%-12s %6d %6d" % (cat, len(vocab), len(dimensions)))
    return sorted(dimensions)


class Vector(object):

    """Vector object initialized from an instance of Vocabulary where the weights
    are either raw frequencies or binary. Implements the cosine measure.

    Vectors are created from vocabularies, but that is not the only choice since
    you could also create them from instances of nltk.text.Text or even directly
    from the result of nltk.word_tokenize(). It is also quite alright to
    implement vectors simply as lists and hand lists to the cosine method."""

    def __init__(self, dimensions, vocabulary, weight="frequency"):
        """Initialize from a Vocabulary instance."""
        self.weight = weight
        self.data = [0] * len(dimensions)
        for i, word in enumerate(dimensions):
            if weight == 'frequency':
                self.data[i] = vocabulary.fdist[word]
            elif weight == 'binary':
                self.data[i] = 1 if vocabulary.fdist[word] > 0 else 0
        self.length = len(self.data)
        self.sum = sum(self.data)

    def __str__(self):
        return "<Vector weight=%s dimensions=%d sum=%d>" % (self.weight, self.length, self.sum)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def cosine(self, other, debug=False):
        dot_product = sum([w1 * w2 for  w1, w2 in zip(self, other)])
        magnitude_v1 = math.sqrt(sum([c**2 for c in self]))
        magnitude_v2 = math.sqrt(sum([c**2 for c in other]))
        if debug:
            print("%.2f %.2f %.2f" % (dot_product, magnitude_v1, magnitude_v2))
        cosine = dot_product / (magnitude_v1 * magnitude_v2)
        return cosine


def create_category_vectors(dimensions, category_vocabs, weight='frequency'):
    category_vectors = {}
    for cat, vocab in category_vocabs.items():
        vector = Vector(dimensions, vocab, weight=weight)
        #print(vocab, vector)
        category_vectors[cat] = vector
    return category_vectors

def create_text_vectors(dimensions, text_vocabs, weight='frequency'):
    vectors = {}
    for text_name in text_vocabs:
        vectors[text_name] = Vector(dimensions, text_vocabs[text_name], weight)
    return vectors

def print_vectors(text_vectors, category_vectors):
    for name in text_vectors:
        print("%-7s %s" % (name, text_vectors[name]))
    print()
    for name in category_vectors:
        print("%-12s %s" % (name, category_vectors[name]))


def compare_to_brown(text):
    """Compare the text to the five categories from Brown and print the similarity
    scores using the cosine measure."""

    # Get the vocabularies for the text and the Brown categories and calculate
    # the dimensions from the category vocabularies. This uses a global variable
    # so we only need to calculate the vocabularies once.
    global BROWN_VOCABULARIES
    vocab = Vocabulary(text)
    if BROWN_VOCABULARIES is None:
        BROWN_VOCABULARIES = get_category_vocabs(BROWN_CATEGORIES)
    dimensions = get_dimensions(BROWN_VOCABULARIES)

    # Get the vectors for all texts and categories
    weight = 'frequency'
    text_vector = Vector(dimensions, vocab, weight)
    category_vectors = create_category_vectors(dimensions, BROWN_VOCABULARIES, weight)

    # print the similarities for the text relative to all categories
    for cat in category_vectors:
        catvec = category_vectors[cat]
        cosine = text_vector.cosine(catvec)
        print("   %-12s %.2f" % (cat, cosine))
