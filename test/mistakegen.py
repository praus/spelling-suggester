#!/usr/bin/env python

import random
import string
import sys

class MistakeGenerator(object):
    """
    This is a fuzzer that generates classes of errors our spelling
    suggester corrects.
    
    1. Case errors
    2. Repeated letters
    3. Incorrect vowels
    4. Any combination of the above types of error in a single word
    """
    
    # Maximum number of duplications for one letter
    LETTER_MAX_DUPL = 4
    
    # Maximum number of errors in a word as percentage of it's length
    MAX_ERRORS = 0.5 # 50%
    
    VOWELS = set("aeiou")
    
    def __init__(self, dictfile):
        self.dictfile = dictfile
        self.word_list = []
        self.__load_file()
    
    def __load_file(self):
        with open(self.dictfile, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    self.word_list.append(line)

    def apply_error(self, word, error_function):
        """
        Takes word and applies error_function in random places random
        number of times.
        """
        # maximum number of errors we can make in this word
        max_err = max(1, int(len(word) * self.MAX_ERRORS))
        
        # number of errors we will make in this word
        errors = random.randint(1, max_err)
        
        letters = list(word)
        for errpos in random.sample(range(len(word)), errors):
            letters[errpos] = error_function(letters[errpos])
        word = ''.join(letters)
        return word
        
    def get_list(self, error_function, words):
        """
        Applies _error_function_ to the _words_ list, and yields
        pair: (misspelled word, correct word)
        """
        return [ self.apply_error(word, error_function) for word in words ]
    
    def get_mixedcase(self, words):
        return self.get_list(string.upper, words)
    
    def get_duplicated(self, words):
        return self.get_list(self.__duplicate, words)
    
    def get_vowel_change(self, words):
        return self.get_list(self.__vowel_change, words)
    
    def get_unchanged(self, words):
        """Simply return list of random unchanged words"""
        return self.get_list(lambda w: w, words)
    
    def get_mistakes(self, n):
        """Get N words with random mistakes, or no mistakes at all."""
        error_functions = [self.get_mixedcase,
                           self.get_duplicated,
                           self.get_vowel_change,
                           self.get_unchanged]
        # randomly choose which error functions to apply
        to_apply = random.sample(error_functions, random.randint(1, len(error_functions)))
        # pick random word from the word_list
        try:
            words = [ self.word_list[i] for i in random.sample(range(len(self.word_list)), n) ]
        except ValueError:
            sys.stderr.write("You can't select more words than is in your dictionary.\n")
            sys.exit(1)
        # apply functions to the words in a "pipe" manner
        errwords = words
        for func in to_apply:
            errwords = func(errwords)
        return zip(errwords, words)
    
    def __duplicate(self, letter):
        """
        Duplicate the letter at most LETTER_MAX_DUPL times.
        """
        duplications = random.randint(1, self.LETTER_MAX_DUPL)
        letters = []
        for _ in range(duplications):
            letters.append(letter)
        return ''.join(letters)
    
    def __vowel_change(self, letter):
        """
        If the letter is a vowel, change it to some other vowel. This means
        that we'll quite often return the letter unchanged, but that's fine.
        """
        if letter in self.VOWELS:
            letters = list(self.VOWELS - set((letter)))
            letter = random.choice(letters)
        return letter
        

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate spelling mistakes')
    parser.add_argument('dictfile', metavar='file', type=str,
                   help='Dictionary file with one word per line.', default="/usr/share/dict/words")
    parser.add_argument('-c', '--count', metavar='mistakes_count', type=int,
                   help='Number of misspelled words to generate', default=100)
    args = parser.parse_args()
    mg = MistakeGenerator(args.dictfile)
    
    for mistake in mg.get_mistakes(args.count):
        print mistake[0]
