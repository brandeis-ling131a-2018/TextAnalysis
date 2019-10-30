# Text Analyzer

In this class you will build a text analyzer, starting from scratch and adding more and more functionality as the course goes on. This repository contains the instructions for the first step. For later assignments you will be given additional instructions, data and code that can be added to this repository.

[ [assignment 3](extensions/a3-search.md)
| [assignment 4](extensions/a4-tags.md)
| assignment 5
]

We start of with this readme file, a `data` directory and a `main.py` script. Your mission is to edit the main script and add the following functionality:

1. Read source data from a file or a set of files in a directory
2. Generate some simple statistics for the source data
3. Generate a vocabulary for the source data
4. Compare the source data to categories in the Brown corpus

In general, unless specifically stated otherwise, you are allowed to:

- use any standard Python module
- use any class or function from the nltk package

You are not allowed to use any other third party module.

Some code is already given to you in `main.py`, most notably some import statements and empty function definitions. Do not change the names of those functions, doing so will break our tests.

This repository also includes a file `test.py` with unit tests, which will be the same test file that we will use. We expect those tests to pass and will deduct points if they do not. However, there may be cases where you feel that the issue is not with your code but with the test, for example, and for the sake of argument, the test for `type_count()` might test whether your answer is between 7900 and 8100 (it doesn't, it is more liberal) and you have 7500 because you do some extra normalization. In that case, leave a comment at the top of your `main.py` file.


## Reading source data

There are three data sources in the `data` directory:

```
grail.txt  -  Monty Python and the Holy Grail
emma.txt   -  Emma by Jane Austen
wsj/*      -  the first 25 documents of the Wall Street Journal corpus
```

You need to finish the `read_text()` method so that it returns an instance of `nltk.text.Text`. Note that the function takes the file name as an argument, take care not to use a hard-coded file name in the function.

```
>>> read_text('data/emma.txt')
<Text: Emma by Jane Austen 1816>
```

Hints:

- Use `os.path.isdir()` and `os.path.isfile()` to test whether the input is a directory or file.
- [Chapter 2](https://www.nltk.org/book/ch02.html) of the NLTK book shows how to load a corpus.



## Generate simple statistics

For the text find the total number of word tokens, word types and sentences. Do this by finishing `token_count()`, `type_count()` and `sentence_count()`. For the type count, you should at least normalize case so that 'the' and 'The' are counted as the same type. You do not need to lemmatize, but it would make for better code and this will probably be part of a later assignment. You will note that the choice to have `read_text()` return a Text influences what you can do here. For example, you do not have access to the raw text anymore and can therefore not use something like `nltk.sent_tokenize()`. Instead you should think about how to recognize those tokens in the Text that indicate sentence boundaries.

When you have finished the three functions we should be able to do something like the following:

```
>>> emma = read_text('data/emma.txt')
>>> token_count(emma)
191673
>>> type_count(emma)
8000
>>> sentence_count(emma)
8039
```

Your counts may differ from the ones above since your code may be slightly different from mine, but they should be in the same ball park though. This holds for all following examples.

In addition, edit and complete the following two functions:

`most_frequent_content_words()`. Return a list with the 25 most frequent content words and their frequencies. The list should have (word, frequency) pairs and be ordered on the frequency. You should use the stop word list in `nltk.corpus.stopwords` in your definition of what a content word is.

```
>>> most_frequent_content_words(emma)[:5]
[('Mr.', 1089), ('Emma', 855), ('could', 824), ('would', 813), ('Mrs.', 668)]
```

`most_frequent_bigrams()`. Return a list with the 25 most frequent bigrams that only contain content words. The list returned should have pairs where the first element in the pair is the bigram and the second the frequency, as in ((word1, word2), frequency), these should be ordered on frequency.

```
>>> most_frequent_bigrams(emma)[:5]
[(('Mr.', 'Knightley'), 271),
 (('Mrs.', 'Weston'), 246),
 (('Mr.', 'Elton'), 211),
 (('Miss', 'Woodhouse'), 168),
 (('Mr.', 'Weston'), 158)]
````


## Generate a vocabulary for the text

A vocabulary is an object that we here create from scratch and that allows us to do a couple of things. You create it from an instance of Text and it should contain a list (or set) of all words in a text and maybe some other information, but how you store that (for example, in what instance variables and in what form) is up to you. The important thing is that you set up your class in such a way that you can easily find some minimal information on a word and print a concordance.

The minimal information for the word are the frequency in the text, the most likely part of speech and a description of the word's most likely meaning (that is, the WordNet gloss).

```
>>> vocab = Vocabulary(read_text('data/grail.txt'))
>>> vocab.frequency('swallow'))
10
>>> vocab.pos('swallow'))
'n'
>>> vocab.gloss('swallow'))
'a small amount of liquid food'
```

In addition, it should allow you to print a concordance for a word.

```
>>> vocab.kwic('swallow')
Displaying 10 of 10 matches:
 is a temperate zone . ARTHUR : The swallow may fly south with the sun or the h
be carried . SOLDIER # 1 : What ? A swallow carrying a coconut ? ARTHUR : It co
 to maintain air-speed velocity , a swallow needs to beat its wings forty-three
: It could be carried by an African swallow ! SOLDIER # 1 : Oh , yeah , an Afri
OLDIER # 1 : Oh , yeah , an African swallow maybe , but not a European swallow
 swallow maybe , but not a European swallow . That 's my point . SOLDIER # 2 :
 and Sir Bedevere , not more than a swallow 's flight away , had discovered som
something . Oh , that 's an unladen swallow 's flight , obviously . I mean , th
he air-speed velocity of an unladen swallow ? ARTHUR : What do you mean ? An Af
o you mean ? An African or European swallow ? BRIDGEKEEPER : Huh ? I -- I do n'
```

Your vocabulary should be restricted to words in the NLTK Words corpus (see section 4.1 in https://www.nltk.org/book/ch02.html). For this assignment, you do not need to normalize words beyond lowercasing them (further normalization will be done in a later assignment). For finding the part of speech and the WordNet gloss you can simply take the first synset of a word, which is the most frequent meaning of the word, and return None if there are no synsets.


##  Comparing the text to the Brown corpus

The last part of the assignment is to turn a Text into a vector and compare it to the vectors for five categories in the Brown corpus: *adventure*, *fiction*, *government*, *humor* and *news* (the words for these categories you can get using NLTK). Compare the text vector to the category vector using the cosine measure to get the similarity of the two vectors. For the vector components you can just use the raw frequency, no need to calculate the tf-idf.

Note that your vectors need to have the same number of dimensions. You might think you could do the following:

- For a text, take all the words in the text, create a frequency dictionary and use it to create a vector.
- For a category, take all the words in the category and do the same as above.

The problem with this is that these vectors have different dimensions and you cannot directly compare them. You will have to decide on how many dimensions to use. Here it is probably easiest to take the union of the vocabularies for the five Brown categories, but you are allowed to take another approach for example by taking a smaller set.

It is probably a good idea to reuse and/or extend the `Vocabulary` class.

```
>>> grail = read_text('data/grail.txt')
>>> compare_to_brown(grail)
adventure    0.84
fiction      0.83
government   0.79
humor        0.87
news         0.82
```

The similarity measure of the grail text and the Brown categories should be printed to the standard output. Run the same comparison with Emma and the Wall Street Journal data. Are you comfortable with the similarity measures that you get? You may (but don't have to) leave a comment with your code where you expand a bit on this.

This may be the part of the assignment that has the slowest running time (although the orinial imports and pinging WordNet for the first time also take several seconds). However, it should not require more running time than a few dozen second or maybe up to a minute on a slower machine.

We will not use a unit test on this, we just want to be able to write a mini script and in it import your code and run it:

```python
from main import compare_to_brown, read_text

emma = read_text('data/emma.txt')
compare_to_brown(emma)
```
