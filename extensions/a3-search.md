# Text Analyzer - Refactoring and Search

For assignment 2 you did the following:

1. Created a function that reads a file or directory and created an instance of nltk.text.Text.
2. Wrote a few functions that take an instance of nltk.text.Text and generated some simple statistics.
3. Created a class called Vocabulary that allowed you to extract basic information for lexical entries, including the contexts it occurs in.
4. Compared texts to five categories from the Brown corpus.

For assignment 3 we are going to add some simple search functionality, but we will first tinker a bit with your original code and do some refactoring. In addition, you can earn extra credit by building a finite state machine. The part for the extra credit will be more time-consuming than the refactoring and search.

Apart from these instructions, you will be given a new test file and example answers for assignment 2 since you will be building on that code. You do not need to adopt the example answers, you may use your own code, but in cases where your code was not working you can update it.

The deadline for this assignment is October 22nd.


## Part 1 - Refactoring

Refactoring is the process of restructuring code without changing its behavior. This is an integral part of code development and it is usually done to reduce complexity, improve readability or improve extensibility. For example, some of you noticed that when you created an instance of nltk.text.Text and needed to write a function to count sentences you were unable to use nltk.sent_tokenize() because that function needed the raw text and you did not have that text anymore. One way to deal with this is to extend the functionality of nltk.text.Text and change how it is created. However, we do not want to change the NLTK code so instead we create a new class that implements the behavior of nltk.text.Text but also gives access to the raw text.

The refactoring will focus on items 1, 2 and 3 above, that is, reading a text, printing simple statistics and creating a vocabulary for that text. We will not overwrite `main.py`, but instead create a new file `main_a3.py` that starts off as an exact copy of `main.py`. A skeleton version of `main_a3.py` is included, all it contains are empty Text and Vocabulary classes with a signature for the __init__() method since we will rely on being able to use those.

Recall that for for assignment 2 you were asked to provide the following functionality for text and vocabulary:

```
>>> from main import read_text, Vocabulary
>>> emma = read_text('data/emma.txt')
>>> token_count(emma)
191673
>>> type_count(emma)
8000
>>> sentence_count(emma)
8039
>>> most_frequent_content_words(emma)[:5]
[('Mr.', 1089), ('Emma', 855), ('could', 824), ('would', 813), ('Mrs.', 668)]
>>> most_frequent_bigrams(emma)[:5]
[(('Mr.', 'Knightley'), 271),
 (('Mrs.', 'Weston'), 246),
 (('Mr.', 'Elton'), 211),
 (('Miss', 'Woodhouse'), 168),
 (('Mr.', 'Weston'), 158)]
>>> grail = read_text('data/grail.txt')
>>> vocab = Vocabulary(grail)
>>> vocab.frequency('swallow'))
10
>>> vocab.pos('swallow'))
'n'
>>> vocab.gloss('swallow'))
'a small amount of liquid food'
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

The first part of the assignment is to change your code so that we can get the same behavior using somewhat different code (note that this is not  pure refactoring since we do change the interface a little bit). We will not use read_text() for getting a text and instead use the new Text class:

```
>>> from main_a3 import Text
>>> emma = Text('data/emma.txt')
```

Statistics now come directly from the instance of the new Text class:

```
>>> emma.token_count()
191673
>>> emma.type_count()
8000
>>> emma.sentence_count()
8039
>>> emma.most_frequent_content_words()[:5]
[('Mr.', 1089), ('Emma', 855), ('could', 824), ('would', 813), ('Mrs.', 668)]
>>> emma.most_frequent_bigrams()[:5]
[(('Mr.', 'Knightley'), 271),
 (('Mrs.', 'Weston'), 246),
 (('Mr.', 'Elton'), 211),
 (('Miss', 'Woodhouse'), 168),
 (('Mr.', 'Weston'), 158)]
````

The Vocabulary class should still be there but have a slightly different interface since it is now created from an instance of Text instead of an instance of nltk.text.Text:

```
>>> from main_a3 import Text, Vocabulary
>>> grail = Text('data/grail.txt')
>>> vocab = Vocabulary(grail)
>>> vocab.gloss('swallow'))
'a small amount of liquid food'
```


## Part 2 - Search

For the second part you need to add four methods to the Text class:

- find_sirs(): returns a sorted list of all sirs.
- find_brackets(): returns a sorted list of all bracketed expressions.
- find_roles(): returns a sorted list of all the roles.
- find_repeated_words(): returns a sorted list of words repeated three times.

For all of them you need to use Python's `re` module as part of your solution. With the exception of the second one, these methods are all focussed on searching 'data/grail.txt'. The first search method is to find occurrence of "Sir X" in the text

```
>>> from main_a3 import Text
>>> grail = Text('data/grail.txt')
>>> grail.find_sirs()
['Sir Bedevere', 'Sir Galahad', 'Sir Gallahad', 'Sir Knight', 'Sir Lancelot',
 'Sir Launcelot', 'Sir Not-appearing-in-this-film', 'Sir Robin']
```

The second is to find text between brackets. The brackets should match and the text itself should not contain any brackets.

```
>>> grail.find_brackets()[:5]
['(Fetchez la vache!)',
 '(Fetchez la vache.)',
 '(I told him we already got one.)',
 '[... cough cough]',
 "[ARTHUR chops the BLACK KNIGHT's last leg off]"]
```

The format of 'data/grails.txt' is one where the beginning of each line either gives you a scene number or the name of the person speaking:

```
SCENE 1: [wind] [clop clop clop]
KING ARTHUR: Whoa there!  [clop clop clop]
SOLDIER #1: Halt!  Who goes there?
```

Your goal is to extract all the speakers:

```
>>> grail.find_roles()[:8]
['ALL HEADS',
 'AMAZING',
 'ANIMATOR',
 'ARMY OF KNIGHTS',
 'ARTHUR',
 'ARTHUR and BEDEVERE',
 'ARTHUR and BLACK KNIGHT',
 'ARTHUR and PARTY']
```

Finally, you are to find repeated words in the text (only include words with at least 3 characters).

```
>>> grail.find_repeated_words()
['boom boom boom',
 'clap clap clap',
 'clop clop clop',
 'giggle giggle giggle',
 'haw haw haw',
 'hee hee hee',
 'heh heh heh',
 'mumble mumble mumble',
 'pound pound pound',
 'quack quack quack',
 'rrrr rrrr rrrr',
 'saw saw saw',
 'scribble scribble scribble',
 'squeak squeak squeak',
 'thud thud thud']
```

The test file in `test_a3.py` has tests for both the refactoring and the search methods.


## Part 3 - Finite State Processing (extra credit)

For this part you create an FSA class that implements a simple Deterministic Finite State Automaton. You build it by defining a set of states (where 'S0' is by definition the start state), a set of final states and a set of transitions:

```
>>> from main_a3 import FSA
>>> states = ['S0', 'S1', 'S2']
>>> final_states = ['S2']
>>> transitions = [ ('S0', 'a', 'S1'), ('S1', 'b', 'S1'), ('S1', 'c', 'S2') ]
>>> fsa = FSA('test', states, final_states, transitions)
```

It would be nice to have a pretty print method:

```
>>> fsa.pp()
<State S0>
   a --> S1
<State S1>
   b --> S1
   c --> S2
<State S2 f>
```

More importantly, it should accept strings that are members of the language yet reject strings that aren't:

```
>>> fsa.accept('abbc')
True
>>> fsa.accept('abca')
False
```

The next step here is to use this FSA to find sub sequences in the text. You would define an FSA for some pattern:

```
>>> states = ['S0', 'S1', 'S2']
>>> final_states = ['S2']
>>> transitions = [ ('S0', 'Sir', 'S1'), ('S1', 'Galahad', 'S2'), ('S1', 'Lancelot', 'S2') ]
>>> fsa = FSA('test', states, final_states, transitions)
```

```
>>> fsa.pp
<State S0>
   Sir --> S1
<State S1>
   Galahad --> S2
   Lancelot --> S2
<State S2 f>
```

And then use it to find instances of that pattern in the text:

```
>>> grail = Text(/data/grail.txt')
>>> grail.apply_fsa(fsa)
[(3754, 'Sir Lancelot'),
 (6345, 'Sir Galahad'),
 (6609, 'Sir Galahad'),
 (6678, 'Sir Galahad'),
 (7501, 'Sir Galahad'),
 (7585, 'Sir Galahad'),
 (7625, 'Sir Galahad'),
 (7877, 'Sir Galahad'),
 (15487, 'Sir Galahad')]
```

Note how the answer is a list of pairs where each pair consists of the token offset in the text and the text found.
