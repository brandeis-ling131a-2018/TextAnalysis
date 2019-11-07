# Assignment 4 - Parts of Speech

This assignment has three parts and an optional extra credit fourth part. The first two parts are on exploring a tagged corpus and a Text and the third and fourth parts are on training and evaluating a part-of-speech tagger. Your code will be created in three new files: `main_a4.py`, `brown.py` and `postag.py`. You will be given skeleton versions of those files, You will need to add existing code from `main_a3.py` to `main_a4.py` (you may also do this from the example answer to assignment 3, included in this repository). The goal is for most of your code to end up in `brown.py` and `postag.py`, but at the same time we will be calling some of the functionality via `main_a4.py`.

Submit by committing your changes and pushing them up to your GitHub repository. Deadline is November 15th around noon.


## Part 1 - Exploring a Tagged Corpus

This is partially based on exercises 15 and 18 from chapter 5 of the NLTK Book and also motivated by a "Your Turn" section in that chapter.

Write code to process the Brown Corpus and find answers to the following questions:

1. Which nouns are more common in their plural form, rather than their singular form? (Only consider regular plurals, formed with the -s suffix.)

2. Which word has the greatest number of distinct tags? What tags are those? Note that you may have more than one word for this.

3. List tags in order of decreasing frequency.

4. Which tags are nouns most commonly found after?

In addition, generate some statistics for tagged data to answer the following questions:

1. What proportion of word types are always assigned the same part-of-speech tag?

2. What proportion of word tokens are always assigned the same part-of-speech tag?

Do this by adding code to the `brown.py` module. Use the code scaffolding as given and do not change the names of methods or the kinds of arguments handed in.  When we look at your code, we will expect that we can import the `brown` module and do the following (some of the answers are truncated for space reasons):

```
>>> bc = brown.BrownCorpus()
>>> brown.nouns_more_common_in_plural_form(bc)
['irregularitie', 'presentment', 'thank', 'term', 'voter', ...]
>>> brown.which_word_has_greatest_number_of_distinct_tags(bc)
[('that', ['DT', 'QL', 'NIL', 'WPS-TL', 'WPO', ...])]
>>> brown.tags_in_order_of_decreasing_frequency(bc)
[('NN', 152470), ('IN', 120557), ('AT', 97959), ('JJ', 64028), ('.', 60638)]
>>> brown.tags_that_nouns_are_most_commonly_found_after(bc)
[('AT', 59656), ('JJ', 40864), ('IN', 24012), ('NN', 17789), ('PP$', 12241), ...]
>>> brown.proportion_ambiguous_word_types(bc)
0.19231155274515707
>>> brown.proportion_ambiguous_word_tokens(bc)
0.8414586046063011
```

You may add as many methods, functions and classes as you see fit. You may use any standard module (ones that do not show up when doing "pip list) or any method or class from nltk. You will be given a set of unit tests for each function.

While doing this you may want to scan ahead to the second part and think about how the task there informs how you would do this one.


## Part 2 - Exploring a Text

This builds on the Text class you created before and generalizes over the work in the previous part. The goal is to make sure all the methods in `postag` can be applied to Texts as well. We want to be able to do the following:

```
import main_a4

grail = main_a4.Text('data/grail.txt')
grail.nouns_more_common_in_plural_form()
grail.which_word_has_greatest_number_of_distinct_tags()
grail.tags_in_order_of_decreasing_frequency()
grail.tags_that_nouns_are_most_commonly_found_after()
grail.proportion_ambiguous_word_types()
grail.proportion_ambiguous_word_tokens()
```

Answers are not shown here but the results should be in the same format as for the previous part (the actual results will differ of course).

Think about what changes you need to make to Text to make this possible. The most obvious changes are that you need to add tags and the methods named above. You can use the NLTK `pos_tag` method for adding the tags. For the methods, you do not want to write them all from scratch but you want to somehow reuse the module level functions that you created for part 1.

You will again be given unit tests for some of these methods. But you will need to write unit tests for the first three of these:

```
nouns_more_common_in_plural_form()
which_word_has_greatest_number_of_distinct_tags()
tags_in_order_of_decreasing_frequency()
```

Add those test to `main_a4.py` and set it up so that they run each time you run `main_a4.py`. For these unit tests you should aim for 3-5 test for each function and you should try to test for some boundary conditions (like an empty Text). You may also want to create a small test file with tagged content.


## Part 3 - Training and Evaluating Taggers

The third part of this assignment is to write your own tagger. This sounds much harder than it is because the nltk module gives you almost everything you need. You should train this tagger on the news category of the Brown Corpus. Create the tagger in `postag.py`. Your tagger script should be able to:

1. Train a POS tagging model on the "news" portion of the Brown corpus and pickle the model.
1. Run on a sentence and print the result to the standard output (`sys.stdout`)
1. Print how well this tagger evaluates on sentences from the Brown "news" category
1. Print how well this tagger evaluates on sentences from the Brown "reviews" category

For pickling, you inevitably need to hard-code the path of the pickle jar and re-use the path in test/evaluate functions, but make sure the path is a relative path so we can run it on our machines.

We give you some skeleton code in `main_a4.py`.

When we you look at your code, we would expect to be able to run

```
$ python main_a4.py --tagger-train
$ python main_a4.py --tagger-run "some sentence to be tagged"
$ python main_a4.py --tagger-test news
$ python main_a4.py --tagger-test reviews
```

You need some code to deal with the arguments. You could access the `sys.argv` variable directly or you could use the `getopt` or `argparse` modules.


## Part 4 - Extra credit

This is like the one above, but now add code to work with a limited tag set (universal parts of speech). You should create a file `main_a4_extra.py` with documentation on top explaining what you did and how the evaluation compares to the one above. And we should be able to do the first two invocations above:

```
$ python main_a4_extra.py --tagger-train
$ python main_a4_extra.py --tagger-run "some sentence to be tagged"
```

For mappings from a long list of tags to universal tags see
https://github.com/slavpetrov/universal-pos-tags/blob/master/en-brown.map.


## How will this be graded?

You can get 10 points for part 1, 10 points for part 2, 5 points for part 3 and 5 points for the extra credit.

For parts 1 and 2 we will run both pep8 and the unit tests (you will get access to the full set of tests we will use). With pep8 we will allow you some idiosyncracies in case you hate some of the things tested and we will run it with a line length of 100. If you get more than two different types of warning we deduct a point, if your code gives a very long list of warnings we deduct another point. Failing unit tests gets you up to 3 points deducted. Again, if you feel that failing a test is a problem with the test you should document this in the documentation string at the top of the module, no deductions if we agree.

The other five point are assigned by the TA by looking at the general quality of your code. When you pass all tests you should get 3 or 4, if you have no code you get a 0, if you go the extra mile with good structure and good comments you get 5 points. It is possible to fail the tests and still get a good score here.

Parts 3 and 4 are graded by the TA by looking at the code and running it. There are no tests and we won't pep8 you on this. Scores are assigned on a 0-5 scale much like laid out in the paragraph above, except that instead of looking at tests we will look at wether your results make sense.
