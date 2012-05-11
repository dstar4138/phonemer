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
from network import class_to_truth
from numpy import mat, zeros, cov, dot
from numpy.linalg import eigh

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
            'current_char': FeatureGenerator.ALPHABET,
            '2after_char': FeatureGenerator.ALL_CHARS,
            'is_vowel': [True, False]
        }
        self._features = []
        self.phones = set()

    def features(self):
        """ A Generator that returns the feature-phoneme pairs for a whole
        phonemedatafile.
        """
        for (w,p) in self.__datafile.readWordSplit():
#            wf = self.__word_features(w)
            for i in range(0,len(w)):
                f = self.__gen_features(i,w)
#                f.update(wf)
                yield (f,p[i])

    def gen_feature_possibilities(self):
        for w,p in self.features():
            self.phones.add(p)
            self._features.append( (w,p) )

    def features_vector(self, pca=None):
        """ 
        takes input as a dictionary of features
            {'before_char': 'a', 'after_char': 'c'}
        and a dictionary of the possible values for each feature
            {'before_char': ['a', 'b', 'c'], 'after_char': ['a', 'b', 'c']}
        returns a truth vector with one element for each input
            [1 0 0 0 0 1]
        """
        self.gen_feature_possibilities()
        phones = list(self.phones)
        numvals = 0
        offsets = {}
        for f in sorted(self.feature_vals):
            offsets[f] = numvals
            numvals += len(self.feature_vals[f])
       
        features_vector = []
        for s, t in self._features:
            v = [0] * numvals
            for f in self.feature_vals:
                idx = offsets[f] + self.feature_vals[f].index(s[f])
                v[idx] = 1
            features_vector.append((v, class_to_truth(phones.index(t), len(phones))))
        
        if pca:
            feats, truth = samplelist_to_mat(features_vector)
            _, eigvecs = gen_pca(feats)
            feats = run_pca(feats, eigvecs, pca)
            return zip(feats.tolist(), truth.tolist())
        else:
            return features_vector




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

        ret["is_vowel"] = w[index] in "aeiou"

        if index>=len(w)-2: ret["2after_char"]=FeatureGenerator.END_OF_WORD_CHAR
        else: ret["2after_char"]=w[index+2]

        return ret


    def __word_features( self, w ):
        ret = {}

        ret["word_soundex"] = self.__soundex( ''.join(w) )
        ret["word_numvowels"] = len(filter(lambda x:x in 'aeiou',w))
    
        return ret


    def __soundex( self, word ):
        def lcr(word, li, repl):
            return ''.join([ repl if x in li else x for x in word ])
        def lwr(word, li, repl):
            res = word
            for w in li: res=res.replace(w, repl)
            return res

        word = word.upper()
        f = word[0]
        vword = f+''.join([x for x in word[1:] if not(x in "AEIOUY")])
        for (l,r) in [("R", '6'),("MN", '5'),("L", '4'),("DT", '3'),("CGJKQSXZ",'2'),("BFVP",'1')]:
            vword = lcr(vword, l, r)
        for a in ['1','2','3','4','5','6']:
            vword = lwr(vword, [a*2, a+'H'+a, a+'W'+a], a)
        vword = ''.join([x for x in vword if not( x in "HW")])
        while(len(vword) < 4): vword+='0'
        if len(vword)>4: vword=vword[:4]
        return f+vword[1:]


def samplelist_to_mat(samples):
    """Converts a list of samples into a matrix.

    Returns: (inputs, outputs), where each are matrices.

    """
    first = samples[0]
    inputs =  mat(zeros((len(samples), len(first[0]))))
    outputs = mat(zeros((len(samples), len(first[1]))))

    for i, s in enumerate(samples):
        inputs[i] = s[0]
        outputs[i] = s[1]

    return inputs, outputs

def gen_pca(matrix):
    """Returns (eigenvalues, eigenvectors) of the given matrix."""
    c = cov(matrix.T)
    eigval, eigvec = eigh(c)
    svals = [v[0] for v in sorted(enumerate(eigval), key=lambda x: x[1], reverse=True)]
    svecs = zeros(eigvec.shape)
    for i in range(eigvec.shape[1]):
        svecs[:,i] = eigvec[:,svals[i]]
    import ipdb; ipdb.set_trace()
    return eigval, svecs

def run_pca(matrix, eigvec, num_components):
    """Performs PCA on the given matrix of data."""
    vecs = eigvec[:, :num_components]
    return dot(matrix, vecs)

