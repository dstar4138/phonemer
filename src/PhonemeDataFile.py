"""
    PhonemeDataFile

    The PhonemeDataFile reads a file in with a given format:
        
        <Word>
        <Pronuncation>
        ...

    The word is a set of characters separated by spaces and the Pronunciation
    is a set of characters separated by spaces as well, except that multiple
    characters can be grouped under a single pronunciation.
    
    Example:
       s i x
       s i _k_s_
       k r o h
       k r O #
       ...
       
    The set of possible states for pronunciation needs not be standard but must
    be finite.
"""

import fileinput

class PhonemeDataFile:

    def __init__(self, filename, charsep=' '):
        self._filename = filename
        self._sep = charsep
        
    def readWord(self):
        """ A Generator for reading in the words, returns a tuple of (word, pronunciation)."""
        prev=None
        for line in open(self._filename, 'r'):
            if line in [' ','']: continue

            if prev == None:
                prev=line
                continue
            else:
                yield (prev,line)
                prev=None

    def readWordSplit(self):
        """ A Generator for reading in the words as tuples of lists of characters. """
        for (w,p) in self.readWord():
            yield (w.split(), p.split())
        
    def readWordMatched(self):
        """ A Generator for reading in the words as a list of tupled pairings of characters. """
        for (w,p) in self.readWordSplit():
            yield zip(w,p)

