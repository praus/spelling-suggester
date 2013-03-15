# Spelling suggester
This is a simple spelling suggester based on Damerau-Levenshtein distance between words, it corrects these classes of errors:
- Case errors
- Repeated letters
- Incorrect vowels
- Any combination of the above types of error in a single word

The suggester works by reading a dictionary file, normalizing the words from the file by lowercasing them, removing any repeated letters that follow each other and removing vowels. The normalized form of the word will be common for all mistakes formed from the original word. You can think of it as a key in a hash table.

This effectivelly creates a hash table within a hashtable (the python dict we keep the normalized words in). This allows us to avoid searching the whole dictionary each time we want to make a suggestion.

Once the spellchecker found the list of possible candidates it compares them to the original word using Damerau-Levenshtein distance and picks the lowest distance. It can happen that multiple words have lowest distances, in such a case we pick the first. This could be improved by having a frequency statistic of English words and choosing the most probable one. For example, "the" is much more frequent than "thaw" so if both were the best corrections according to the distance, "the" would be better correction.

## How to run spelling suggester
Run ``src/spellsuggester.py <path_to_dictionary_file>``

## Tests
It's best to use nose (https://github.com/nose-devs/nose) for running the tests, run ``nosetests -v`` from the project directory.

``test/mistakegen.py [-c number_of_words] <file>`` generates words with spelling errors from the supplied dictionary.

You can perform a simple test by feeding the mistakes into the suggester, the suggester should always offer a suggestion:

```
test/mistakegen.py /usr/share/dict/words | src/spellsuggester.py /usr/share/dict/words | grep "NO SUGGESTION"
```

Therefore the above command should not output anything.
