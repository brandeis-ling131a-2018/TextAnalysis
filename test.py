import sys
import unittest
import warnings
from io import StringIO

from main import read_text, token_count, type_count, sentence_count
from main import most_frequent_content_words, most_frequent_bigrams
from main import Vocabulary


def ignore_warnings(test_func):
    """Catching warnings via a decorator."""
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            test_func(self, *args, **kwargs)
    return do_test


class BasicTests(unittest.TestCase):

    """For testing basic functionality like loading the file or corpus into a Text
    and the basic statistics.

    Note the use of setUpClass, which loads some data that can be used in each
    individual test. Each method that starts with 'test' will run when you do
    unittest.main(). You may use as many other as you want.

    """

    @classmethod
    def setUpClass(cls):
        cls.grail = read_text('data/grail.txt')
        cls.emma = read_text('data/emma.txt')
        cls.wsj = read_text('data/wsj')

    def test_read_text_class(self):
        """Class of instance returned by read_text() is Text.""" 
        self.assertEqual(self.grail.__class__.__name__, 'Text')
        
    def test_read_text_non_empty1(self):
        """Text returned by read_text() is not empty."""
        self.assertTrue(len(self.grail) > 0)

    def test_read_text_non_empty2(self):
        """Text returned by read_text() is not empty (but now for the wsj corpus)."""
        self.assertTrue(len(self.wsj) > 0)

    def test_read_text_relative_lengths(self):
        """Check wether emma is larger than grail and grail is larger than wsj."""
        self.assertTrue(len(self.emma) > len(self.grail) > len(self.wsj))

    def test_token_count(self):
        """Number of tokens returned by token_count() is in the ballpark."""
        self.assertTrue(180000 < token_count(self.emma) < 200000)
        
    def test_type_count(self):
        """Number of types returned by type_count() is in the ballpark."""
        self.assertTrue(7000 < type_count(self.emma) < 9000)
        
    def test_sentence_count(self):
        """Number of sentences returned by sentence_count() is in the ballpark."""
        self.assertTrue(7000 < sentence_count(self.emma) < 9000)

    def test_most_frequent_content_words_overlap(self):
        """Content words overlap 60% with the example solution."""
        example_content_words = {
            'Elton', 'Emma', 'Harriet', 'Jane', 'Knightley', 'Miss', 'Mr.',
            'Mrs.', 'Weston', 'Woodhouse', 'could', 'every', 'good', 'know',
            'little', 'might', 'much', 'must', 'never', 'one', 'said', 'say',
            'thing', 'think', 'would'}
        example_content_words = set([w.lower() for w in example_content_words])
        content_words = [w[0].lower() for w in most_frequent_content_words(self.emma)]
        overlap = len(example_content_words.intersection(set(content_words)))
        self.assertTrue(overlap > 15)

    def test_most_frequent_content_words_minimal_frequency(self):
        """Least frequent content word occurs at least 100 times."""
        frequencies = [w[1] for w in most_frequent_content_words(self.emma)]
        self.assertTrue(min(frequencies) > 100)

    def test_most_frequent_bigrams_overlap(self):
        """Bigrams overlap 60% with the first example solution or 45% with the second
        example solution (which cuts out all the Mr. X and Mrs. X examples but
        takes in a few more bigrams)."""
        example_bigrams1 = {
            'Emma could', 'Frank Churchill', 'Jane Fairfax', 'John Knightley',
            'Miss Bates', 'Miss Fairfax', 'Miss Smith', 'Miss Taylor',
            'Miss Woodhouse', 'Mr. Elton', 'Mr. Frank', 'Mr. Knightley',
            'Mr. Martin', 'Mr. Weston', 'Mr. Woodhouse', 'Mrs. Churchill',
            'Mrs. Elton', 'Mrs. Goddard', 'Mrs. Weston', 'dare say',
            'every body', 'every thing', 'great deal', 'said Emma', 'said Mr.'}
        example_bigrams2 = {
            'Box Hill', 'Colonel Campbell', 'Emma could', 'Emma felt',
            'Every body', 'Frank Churchill', 'Harriet Smith', 'Jane Fairfax',
            'John Knightley', 'Maple Grove', 'Miss Bates', 'Miss Fairfax',
            'Miss Hawkins', 'Miss Smith', 'Miss Taylor', 'Miss Woodhouse',
            'Robert Martin', 'body else', 'cried Emma', 'dare say', 'dear Emma',
            'every body', 'every day', 'every thing', 'good deal', 'great deal',
            'said Emma', 'said Mr.', 'said Mrs.', 'would never', 'would rather',
            'young lady', 'young woman'}
        example_bigrams1 = set(w.lower() for w in example_bigrams1)
        example_bigrams2 = set(w.lower() for w in example_bigrams2)
        bigrams = set(["%s %s" % (x[0].lower(), x[1].lower()) for x in
                       [w[0] for w in most_frequent_bigrams(self.emma)]])
        overlap1 = len(example_bigrams1.intersection(set(bigrams)))
        overlap2 = len(example_bigrams2.intersection(set(bigrams)))
        self.assertTrue(overlap1 > 15 or overlap2 > 15)

    def test_most_frequent_bigrams_minimal_frequency(self):
        """Least frequent bigram occurs at least 20 times."""
        frequencies = [w[1] for w in most_frequent_bigrams(self.emma)]
        self.assertTrue(min(frequencies) > 20)


class TestVocabulary(unittest.TestCase):

    """For testing the Vocabulary class. Would have liked to test some of the
    internal structure, like the size of the vocabulary in self.vocab_size, but
    can only test the agreed upon interface.

    """
    
    @classmethod
    def setUpClass(cls):
        cls.text = read_text('data/grail.txt')
        cls.vocab = Vocabulary(cls.text)

    def run_kwic(self, keyword):
        try:
            self.vocab.kwic(keyword)
        except AttributeError:
            # dealing with an error in the original assignment
            self.vocab.quick(keyword)

    def test_vocabulary_class(self):
        self.assertEqual(self.vocab.__class__.__name__, 'Vocabulary')

    def test_vocabulary_frequency1(self):
        """Check frequency of the word 'swallow'."""
        self.assertTrue(8 < self.vocab.frequency('swallow') < 12)

    def test_vocabulary_frequency2(self):
        """Function words should occur too."""
        self.assertTrue(self.vocab.frequency('the') > 200)

    def test_vocabulary_frequency3(self):
        """Unknown words have frequency of 0."""
        self.assertEqual(self.vocab.frequency('dingelhopper'), 0)

    @ignore_warnings
    def test_vocabulary_pos1(self):
        """Check pos of the word 'swallow'."""
        self.assertEqual(self.vocab.pos('swallow'), 'n')

    @ignore_warnings
    def test_vocabulary_pos2(self):
        """Unknown words have pos of None."""
        self.assertEqual(self.vocab.pos('dingelhopper'), None)

    def test_vocabulary_gloss(self):
        """Check gloss of the word 'swallow'."""
        # another way t catch warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.assertEqual(self.vocab.gloss('swallow'), 'a small amount of liquid food')

    def test_vocabulary_kwic1(self):
        """Check whether the KWIC gives you some results."""
        # redirect the standard output into a buffer, to be restored later
        try:
            stdout = sys.stdout
            sys.stdout = StringIO()
            self.run_kwic('swallow')
            kwic = sys.stdout.getvalue()
            keywords = [w for w in kwic.split() if w.lower() == 'swallow']
            self.assertTrue(len(keywords) > 5)
        finally:
            sys.stdout = stdout

    def test_vocabulary_kwic2(self):
        """Check whether a KWIC on a non-existing word gives you no results."""
        # redirect the standard output into a buffer, to be restored later
        try:
            stdout = sys.stdout
            sys.stdout = StringIO()
            self.run_kwic('dingelhopper')
            kwic = sys.stdout.getvalue()
            keywords = [w for w in kwic.split() if w.lower() == 'swallow']
            self.assertTrue(len(keywords) == 0)
        finally:
            sys.stdout = stdout


if __name__ == '__main__':

    unittest.main()
