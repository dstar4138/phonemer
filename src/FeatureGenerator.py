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

class FeatureGenerator:
    
    START_OF_WORD_CHAR = "^"
    END_OF_WORD_CHAR = "$"

    def __init__(self, datafile):
        self.__datafile = datafile

    def features():
        """ A Generator that returns the feature-phoneme pairs for a whole
        phonemedatafile.
        """
        for (w,p) in self.__datafile.readWordSplit():
            for i in range(0,len(w)-1):
                f = self.__gen_features(i,w)
                yield (f,p[i])

    def __gen_features(self, index, characters):
        """ Returns a dictionary of the features for a current index in a 
        word.
        """
        ret = {}

        if index==0: ret["before_char"]=FeatureGenerator.START_OF_WORD_CHAR
        else: ret["before_char"]=w[index-1]
    
        if index==len(w)-1: ret["after_char"]=FeatureGenerator.END_OF_WORD_CHAR
        else: ret["after_char"]=w[index+1]

        #TODO: add more features!


        return ret
