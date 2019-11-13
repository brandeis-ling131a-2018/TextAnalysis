"""test_a4.py

Tests for the first two parts of assignment 4.

"""


import sys
import unittest
import warnings

from main_a4 import Text
import brown


def ignore_warnings(test_func):
    """Catching warnings via a decorator."""
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            test_func(self, *args, **kwargs)
    return do_test


class ExploreTaggedCorpusTests(unittest.TestCase):

    """Note the use of setUpClass, which loads some data that can be used in each
    individual test. Each method that starts with 'test' will run when you do
    unittest.main(). You may use as many other as you want."""

    @classmethod
    @ignore_warnings
    def setUpClass(cls):
        # this takes a while...
        cls.bc = brown.BrownCorpus()
        cls.nouns_more_common_in_plural = brown.nouns_more_common_in_plural_form(cls.bc)
        cls.most_tags = brown.which_word_has_greatest_number_of_distinct_tags(cls.bc)
        cls.frequent_tags = brown.tags_in_order_of_decreasing_frequency(cls.bc)
        cls.tags_after_nouns = brown.tags_that_nouns_are_most_commonly_found_after(cls.bc)
        cls.ambiguous_types = brown.proportion_ambiguous_word_types(cls.bc)
        cls.ambiguous_tokens = brown.proportion_ambiguous_word_tokens(cls.bc)

    def test_nouns_more_common_in_plural(self):
        """There are about 3400 of them."""
        self.assertTrue(3000 < len(self.nouns_more_common_in_plural) < 3800)

    def test_most_tags(self):
        """The word with the most tags is 'that'."""
        self.assertEqual(self.most_tags[0][0], 'that')

    def test_frequent_tags1(self):
        """The most frequent Brown tag is NN and it occurs 152470 times."""
        self.assertEqual(self.frequent_tags[0][0], 'NN')
        self.assertTrue(150000 < self.frequent_tags[0][1], 155000)

    def test_frequent_tags2(self):
        """Get the 20 most frequent tags and make sure the overlap is greater than 18."""
        most_frequent_tags = {'TO', 'NNS', 'RB', ',', 'NP', 'CD', 'VBD', 'CS', 'VBG', 'JJ',
                              'VBN', 'NN', 'PPSS', 'VB', 'IN', 'PP$', 'CC', 'AT', 'PPS', '.'}
        most_frequent_tags_found = set(t[0] for t in self.frequent_tags[:20])
        self.assertTrue(len(most_frequent_tags & most_frequent_tags_found) > 18)

    def test_noun_tags1(self):
        """Overlap of found set and example set is at least 8."""
        tags = [('AT', 59656), ('JJ', 40864), ('IN', 24012), ('NN', 17789), ('PP$', 12241),
                ('CC', 6610), ('CD', 5264), ('AP', 5112), ('DT', 4540), ('VBG', 4407)]
        self.assertTrue(len(set([t[0] for t in tags])
                            & set([t[0] for t in self.tags_after_nouns])) > 8)

    def test_noun_tags2(self):
        """Most frequent tag before a noun occurs at least 50k times."""
        self.assertTrue(self.tags_after_nouns[0][1] > 50000)

    def test_ambiguous_types(self):
        self.assertTrue(0.15 < self.ambiguous_types < 0.25)

    def test_ambiguous_tokens(self):
        self.assertTrue(0.78 < self.ambiguous_tokens < 0.88)


class ExploreTextTests(unittest.TestCase):

    @classmethod
    @ignore_warnings
    def setUpClass(cls):
        cls.grail = Text('data/grail.txt')
        cls.tags_after_nouns = cls.grail.tags_that_nouns_are_most_commonly_found_after()
        cls.ambiguous_types = cls.grail.proportion_ambiguous_word_types()
        cls.ambiguous_tokens = cls.grail.proportion_ambiguous_word_tokens()

    def test_noun_tags1(self):
        """Overlap of found set and example set is at least 6."""
        # Here the target was lowered from 8 since potentially there was a
        # different tag set used.
        tags = [('.', 1198), ('NNP', 588), (':', 576), ('DT', 527), ('JJ', 443),
                ('NN', 426), ('IN', 167), ('PRP$', 125), (',', 115), ('CC', 49)]
        self.assertTrue(len(set([t[0] for t in tags])
                            & set([t[0] for t in self.tags_after_nouns])) > 6)

    def test_noun_tags2(self):
        """Most frequent tag before a noun occurs at least 1000 times."""
        self.assertTrue(self.tags_after_nouns[0][1] > 1000)

    def test_ambiguous_types(self):
        self.assertTrue(0.14 < self.ambiguous_types < 0.25)

    def test_ambiguous_tokens(self):
        self.assertTrue(0.35 < self.ambiguous_tokens < 0.50)


if __name__ == '__main__':

    unittest.main()
