# Text Analyzer

In this class you will build a text analyzer, starting from scratch and adding more and more functionality as the course goes on. This repository contains the instructions for the first step. For later assignments you will be given additional instructions, data and code that can be added to this repository.

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


## Reading source data

There are three data sources in the `data` directory:

```
grail.txt  -  Monty Python and the Holy Grail
emma.txt   -  Emma by Jane Austen
wsj/*      -  the first 25 documents of the Wall Street Journal corpus
```

You need to finish the `read_text()` method so that it returns an instance of `nltk.text.Text`.

```
>>> read_text('data/emma.txt')
<Text: Emma by Jane Austen 1816>
```

Hint: use `os.path.isdir()` and `os.path.isfile()` to test whether the input is a directory or file.


## Generate simple statistics

For the text find the total number of word tokens, word types and sentences. Do this by finishing `token_count()`, `type_count()` and `sentence_count()`.

```
>>> emma = read_text('../data/emma.txt')
>>> token_count(emma)
191673
>>> type_count(emma)
8467
>>> sentence_count(emma)
8039
```

Note that your counts may differ from the ones above, they should be in the same ball park though. This holds for all following examples.

In addition, edit and complete the following two functions:

`most_frequent_content_words()`. Return a list with the 25 most frequent content words and their frequencies. The list should have (word, frequency) pairs and be ordered on the frequency. You should use the stop word list in `nltk.corpus.stopwords` in your definition of what a content word is.

```
>>> most_frequent_content_words(emma)[:5]
[('I', 3164), ('Mr.', 1089), ('Emma', 855), ('could', 824), ('would', 813)]
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

A vocabulary is an object that contains a list (or set) of all words in a text. In addition,it allows you to look up some very minimal information for that word like the frequency in the text, the most likely part of speech and the most likely meaning (WordNet gloss).

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

Your vocabulary should be restricted to words in the NLTK Words corpus (see section 4.1 in https://www.nltk.org/book/ch02.html). For this assignment, you do not need to normalize words beyond owercasing them (further normalization will be done in a later assignment). For finding the part of speech and the WordNet gloss you can simply take the first synset of a word, and return None if there are no synsets.


##  Comparing the text to the Brown corpus

The last part of the assignment is to turn the text into a vector and compare it to the vectors for five categories in the Brown corpus: *adventure*, *fiction*, *government*, *humor* and *news*. Compare using the cosine to get the similarity of two vectors. For the vector components you can just use the raw frequency, no need to calculate the tf-idf.

Note that you will have to decide on how many dimensions to use. Here it is probably best to take the union of the vocabularies for the five Brown categories, but you are allowed to take another approach. It is also probably a good idea to reuse and extend the `Vocabulary` class.

```
>>> grail = read_text('data/grail.txt')
>>> compare_to_brown(grail)
adventure    0.84
fiction      0.83
government   0.79
humor        0.87
news         0.82
```

The similarity measure of the grail text and the Brown categories should be printed to the standard output. Run the same comparison with Emma and the Wall Street Journal data. Are you comfortable with the similarity measures that you get?
