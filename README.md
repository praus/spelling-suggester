# Spelling suggester
This is a simple spelling suggester, it corrects these classes of errors:
1. Case errors
2. Repeated letters
3. Incorrect vowels
4. Any combination of the above types of error in a single word

The suggester works by reading a dictionary file, normalizing the words from the file by lowercasing them, removing any repeated letters that follow each other and removing vowels. The normalized form of the word will be common for all mistakes formed from the original word. You can think of it as a key in a hash table.

This effectivelly creates a hash table within a hashtable (the python dict we keep the normalized words in). This allows us to avoid searching the whole dictionary each time we want to make a suggestion.

## How to run spelling suggester
Run ``src/spellsuggester.py <path_to_dictionary_file>``

## Tests
It's best to use nose (https://github.com/nose-devs/nose) for running the tests, run ``nosetests -v`` from the project directory.

``test/mistakegen.py`` generates words from the supplied dictionary:
Run ``mistakegen.py [-c number_of_words] <file>``

You can perform a simple test by feeding the mistakes into the suggester, the suggester should always offer a suggestion:
```test/mistakegen.py /usr/share/dict/words | src/spellsuggester.py /usr/share/dict/words | grep "NO SUGGESTION"```
Therefore the above command should not output anything.
