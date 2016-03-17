import unittest
import util
from ctypes import *

class Wordlist:

    def __init__(self, words):

        util.bind_all(self, util.wordlist_funcs)

        self.wl = self.wordlist_init(words)
        self.lookup_word = lambda w: self.wordlist_lookup_word(self.wl, w)
        self.lookup_index = lambda i: self.wordlist_lookup_index(self.wl, i)

    def free(self):
        if self.is_valid():
            self.wordlist_free(self.wl)
            self.wl = None

    def is_valid(self):
        return self.wl is not None



class WordlistTests(unittest.TestCase):

    words_list = None

    def setUp(self):
        if self.words_list is None:
            self.words_list, _ = util.load_words('english')


    def test_wordlist(self):

        for n in xrange(17):
            # Build a wordlist of n words
            test_list = self.words_list[0 : n]

            wl = Wordlist(' '.join(test_list))
            self.assertTrue(wl.is_valid())

            for idx, word in enumerate(test_list):
                # Verify lookup by word and index
                self.assertEqual(idx + 1, wl.lookup_word(word))
                self.assertEqual(wl.lookup_word(self.words_list[n + 1]), 0)
                self.assertEqual(wl.lookup_index(idx), word)
                # Lookup of a non-present word
                self.assertIsNone(wl.lookup_index(n + 1))

            wl.free()


if __name__ == '__main__':
    unittest.main()
