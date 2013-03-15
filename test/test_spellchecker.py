'''
Created on Mar 14, 2013

@author: petr
'''
import unittest

from spellsuggester import SpellSuggester
from mistakegen import MistakeGenerator

class Test(unittest.TestCase):


    def setUp(self):
        self.word_file = "/usr/share/dict/words"
        self.sp = SpellSuggester(self.word_file)


    def tearDown(self):
        pass


    def testNormalize(self):
        self.assertEqual("hj", self.sp.normalize("AAAhhhooooojjjjj"), "Improper normalization")
        self.assertEqual("", self.sp.normalize("A"), "Improper normalization")
    
    def testLoadFromFile(self):
        self.assertItemsEqual(['Belgian', 'Bologna', 'Bulganin', 'bologna'], 
                              self.sp.word_list["blgn"], "Improperly loaded dictionary")
    
    def __check_truth(self, misspelling, correct):
        self.assertEqual(correct, self.sp.get_correction(misspelling),
                         "Wrong spelling correction")
    
    def testCorrectionsManual(self):
        truth = [ # (misspelling, correct word)
                 ("sheeeep", "sheep"),
                 ("jjoobbb", "job"),
                 ("weke", "wake"),
                 ("CUNsperrICY", "conspiracy"),
                 ("sheeple", "NO SUGGESTION"),
                 ("pppeckets", "packets"),
                 ("ieeonCaoire''''s", "encore's")
                 ]
        for pair in truth:
            print pair
            self.__check_truth(pair[0], pair[1])
        
    def testRandomCorrections(self):
        mg = MistakeGenerator(self.word_file)
        MISTAKES_NUM = 10000
        truth = mg.get_mistakes(MISTAKES_NUM)
        for error, _ in truth:
            self.assertNotEqual("NO SUGGESTION", self.sp.get_correction(error),
                                "%s should have a suggestion" % error)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()