#!/usr/bin/env python

from dameraulevenshtein import dameraulevenshtein

class SpellChecker(object):
    VOWELS = list("aeiou")
    
    def __init__(self, dictfile):
        self.word_dict = {}
        self.load_dict_from_file(dictfile)

    def normalize(self, word):
        """
        Normalizes the word by: 
        1. lowercasing
        2. removing repeated letters
        3. removing vowels
        """
        word = word.lower()
        norm = [word[0]]
        for letter in word[1:]:
            if letter != norm[-1] and letter not in self.VOWELS:
                norm.append(letter)
        return ''.join(norm)
    
    def load_dict_from_file(self, filename):
        """
        Reads words from file, normalizes them and stores them in memory in dict.
        """
        with open(filename, 'r') as f:
            for line in f:
                word = line.strip()
                if word:
                    normw = self.normalize(word)
                    # Store normalized word in our in-memory processed dictionary
                    if not self.word_dict.get(normw):
                        self.word_dict[normw] = []
                    self.word_dict[normw].append(word)
        return self.word_dict
    
    def get_correction(self, word):
        """
        Select best correction if multiple corrections have the same score.
        In this case, we just return the first correction but we could also improve
        this by having a frequency statistic of English words and choosing the most
        probable one. For example, "the" is much more frequent than "thaw" so if both
        were the best corrections according to the distance, the would be better correction.
        """
        print word,
        # 
        correction = self.get_corrections(word)[0]
        return correction[1]
    
    def get_corrections(self, word):
        norm = self.normalize(word)
        candidates = self.word_dict.get(norm)
        if not candidates:
            return [(0, "NO CANDIDATES")]
        def rank_candidates():
            for cand in candidates:
                yield dameraulevenshtein(cand, word), cand
        
        ranked = list(rank_candidates())
        best_score = min(ranked, key=lambda x: x[0])[0]
        return [ c for c in ranked if c[0] == best_score ]
        
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Check spelling')
    parser.add_argument('dictfile', metavar='file', type=str,
                   help='Dictionary file with one word per line.', default="/usr/share/dict/words")
    
    args = parser.parse_args()
    
    sp = SpellChecker(args.dictfile)
    print sp.get_correction("sheeep")
    print sp.get_correction("sheeeep")
    print sp.get_correction("jjoobbb")
    print sp.get_correction("weke")
    print sp.get_correction("CUNsperrICY")
    print sp.get_correction("sheeple")
    