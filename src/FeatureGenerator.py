"""
    FeatureGenerator

    Generates features for a phoneme word-pronunciation pair as read in from a 
    PhonemeDataFile. Just pass in a PhonemeDataFile and call featureset(), to
    get the complete list of features.

    The Features returned are:
        - Character Before
        - Character After
        - Character Current
        - Word soundex
        - Is Vowel
        - Character 2 After
    
    The return value is a list of Features-Result pairs, where the result is
    the phoneme that goes with that a character represented by the features.
"""

import string

class FeatureGenerator:
    
    START_OF_WORD_CHAR = "^"
    END_OF_WORD_CHAR = "$"
    ALPHABET = [c for c in string.lowercase]
    ALL_CHARS = ALPHABET + [START_OF_WORD_CHAR, END_OF_WORD_CHAR]

    def __init__(self, datafile):
        self.__datafile = datafile
        self.feature_vals = {
            'before_char': FeatureGenerator.ALL_CHARS,
            'after_char': FeatureGenerator.ALL_CHARS,
            'current_char': FeatureGenerator.ALPHABET
        }

    def features(self):
        """ A Generator that returns the feature-phoneme pairs for a whole
        phonemedatafile.
        """
        for (w,p) in self.__datafile.readWordSplit():
            for i in range(0,len(w)):
                f = self.__gen_features(i,w)
                yield (f,p[i])


    def features_vector(self):
        """ 
        takes input as a dictionary of features
            {'before_char': 'a', 'after_char': 'c'}
        and a dictionary of the possible values for each feature
            {'before_char': ['a', 'b', 'c'], 'after_char': ['a', 'b', 'c']}
        returns a truth vector with one element for each input
            [1 0 0 0 0 1]
        """
        numvals = 0
        offsets = {}
        for f in sorted(self.feature_vals):
            offsets[f] = numvals
            numvals += len(self.feature_vals[f])
        
        for s, t in self.features():
            v = [0] * numvals
            for f in self.feature_vals:
                idx = offsets[f] + self.feature_vals[f].index(s[f])
                v[idx] = 1
            yield v, t

    def __gen_features(self, index, w):
        """ Returns a dictionary of the features for a current index in a 
        word.
        """
        ret = {}

        if index==0: ret["before_char"]=FeatureGenerator.START_OF_WORD_CHAR
        else: ret["before_char"]=w[index-1]
    
        if index==len(w)-1: ret["after_char"]=FeatureGenerator.END_OF_WORD_CHAR
        else: ret["after_char"]=w[index+1]

        ret["current_char"] = w[index]

        #TODO: add more features!


        return ret
