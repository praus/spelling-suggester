'''
Created on Mar 14, 2013

@author: petr
'''
import unittest

from spellchecker import SpellChecker

class Test(unittest.TestCase):


    def setUp(self):
        self.sp = SpellChecker("/usr/share/dict/words")


    def tearDown(self):
        pass


    def testNormalize(self):
        self.assertEqual("ahj", self.sp.normalize("AAAhhhooooojjjjj"), "Improper normalization")
        self.assertEqual("a", self.sp.normalize("A"), "Improper normalization")
    
    def testLoadFromFile(self):
        self.assertItemsEqual(['Belgian', 'Bologna', 'Bulganin', 'bologna'], 
                              self.sp.word_dict["blgn"], "Improperly loaded dictionary")
    
    def testCorrections(self):
        truth = [ # (misspelling, correct word)
                 ("sheeeep", "sheep"),
                 ("jjoobbb", "job"),
                 ("weke", "wake"),
                 ("CUNsperrICY", "conspiracy")
                 ]
        for pair in truth:
            self.assertEqual(pair[1], self.sp.get_correction(pair[0]), "Wrong spelling correction")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()