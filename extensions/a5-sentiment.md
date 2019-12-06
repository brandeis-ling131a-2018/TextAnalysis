# Assignment 5 - Sentiment Analysis

In this assignment you will use a data set of movie reviews and experiment with the Naïve Bayes and decision tree classifiers in Scikit Learn.

Deadline: December 10th.

Put your code in a file named `main_a5.py`. You could put all your code in there, but you may also use as many auxiliary files as you want.  

We should be able to use your code to train classifiers as follows:

```
$ python3 main_a5.py --train
```

Your code should create a bunch of classifiers and write them to the `classifiers` directory, again using Python's `pickle` module or the `joblib` module, which is better with large numpy arrays (sklearn makes heavy use of numpy). Write progress notes and time elapsed to generate your model. Also write for each classifier what accuracy it operates at. So we would see something like:

```
$ python3 main_a5.py --train
Creating Bayes classifier in classifiers/bayes-all-words.jbl
    Elapsed time: 4s
    Accuracy: 0.89
Creating Bayes classifier in classifiers/bayes-sentiwordnet.jbl
    Elapsed time: 6s
    Accuracy: 0.84
.
.
.
```

We should also be able to run your code on a file that we provide:

```
$ python3 main_a5.py --run 'bayes'|'tree' <filename>
```

 Here, your code should ask what classifier model to use and then run the classifier over the given file, which will be a file in the same format as the data used to train your model. We do not care that much whether your code gives the right answer, we just want to see it run and we want it to print `pos` or `neg` to the standard output. Here is an example exchange:

 ```
 $ python3 main_a5.py --run bayes data/review-example.txt
 Choose a model:
 1 - all words raw counts
 2 - all words binary
 3 - SentiWordNet words
 4 - Subjectivity Lexicon words
 5 - all words plus Negation
 Type a number:
 $
 ```

Now we would type a number from 1 through 5 and your code would print the result:

```
$ 3
pos
```

## Data Handling

As our sentiment data we use version 2.0 of the polarity dataset compiled by Pang and Lee, available at http://www.cs.cornell.edu/people/pabo/movie-review-data/. This data set contains 1000 positive reviews and 1000 negative reviews that are tokenized and lower cased. Follow the link to the readme file for more information. You should use NLTK to get access to those data (see chapter 6 for how to do this).

Once you have the data, you first have to prepare it for the classifiers. Data preparation includes two steps:

1. generating the features
2. encoding the features

You should experiment with the following feature sets:

1. All words with raw counts or tf-idf scores
2. All words but just as binary features
3. Only the words from SentiWordNet with positive or negative scores over 0.5
4. Only the words from the MPQA Subjectivity Lexicon

SentiWordNet is available in WordNet and can be used as follows:

```
>>> from nltk.corpus import sentiwordnet as swn
>>> happy = list(swn.senti_synsets('happy', 'a'))[0]
>>> print(happy)
<happy.a.01: PosScore=0.875 NegScore=0.0>
>>> print("pos:%s neg:%s obj:%s"
...       % (happy.pos_score(), happy.neg_score(), happy.obj_score()))
pos:0.875 neg:0.0 obj:0.125
```

The MPQA Subjectivity lexicon will be part of the repository. It has about 8000 words associated with parts of speech and a subjectivity score. The lexicon is stored in `data/subjectivity_clues_hltemnlp05` which has both a readme file and a data file. Lines in the data file look like:

```
type=weaksubj len=1 word1=abandoned pos1=adj stemmed1=n priorpolarity=negative
type=weaksubj len=1 word1=abandonment pos1=noun stemmed1=n priorpolarity=negative
```


#### Negation

For the first of the above feature sets you should also experiment with a version using the simple heuristic shown in class (slides to be posted). Say we have a vector

```
<door=12 window=6 liked=4>
```

and 'liked' was negated in one of those 4 cases, then the vector should be

```
<door=12 window=6 liked=3 NOT_liked=1>
```


#### Encoding

It is up to you how to encode this, but chances are that you want to use either the OrdinalEncoder or the OneHotEncoder. Encoding examples that were shown in class will be posted.


## Classifier

When you have created your feature sets you should partition them into a training set and a test set. Create the training sets when we do

```
$ python3 main_a4.py --train
```

Load and use the saved model when we do

```
$ python3 main_a4.py --run 'bayes'|'tree' <filename>
```


## How will this be graded?

There are no unit tests. But we will run the code and see whether your classifiers reach a minimum level of accuracy (level to be determined). This will be 50% of your grade. In addition you will be pep8-ed and your code will be graded on a scale from 0-5.
