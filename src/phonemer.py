#!/usr/bin/env python 
#
# Usage:
#   ./phonemer.py [--train=<TRAINING_FILE>] <WORD>
# 

import os
import sys
import nltk
from optparse import OptionParser
from FeatureGenerator import FeatureGenerator
from PhonemeDataFile import PhonemeDataFile
from network import    NeuralNet,loadNN
from random import shuffle

def gen_optparse():
    parser = OptionParser(usage="%prog -h | ([-s P | [-n H] [-p V]] -d D [-f F] | -t N [-w W]) ")
    parser.add_option('-s', '--split', action="store", dest="splitsize", type="float",
                      help="Split the raw data set into some random subsets, please give the percent as a decimal.")
    parser.add_option('-n', '--hidden', action="store", dest="numhidden", default=50, type="int",
                      help="The number of hidden nodes in the neural net.")
    parser.add_option('-p', '--pca', dest="pca", type="int",
                      help="The number of PCA vectors")
    parser.add_option('-t', '--trained', dest="nnfile",
                      help="The data file you get after training on a data set", metavar="NN_FILE")
    parser.add_option('-d', '--rawdata', dest="trainfile",
                      help="The raw training file to train the Neural net and save it to a file.", metavar="DAT_FILE")
    parser.add_option('-f', '--savefile', dest='savefile',default="savedweights.nn",
                      help="The optional output name for a trained neural net file.", metavar="NN_FILE")
    parser.add_option('-w', '--word', dest="word",
                      help="The word to get the phoneme list for.", metavar="WORD")
    return parser

def makeNN(filename, outputfile, hidden, pca):
    fgen = FeatureGenerator(PhonemeDataFile(filename))
    features, pcas = list(fgen.features_vector(pca))
    shuffle(features)
    split = int(len(features) * 0.8)
    train = features[:split] #The larger set for training
    test = features[split:] 
    
    num_input = len(train[0][0])
    num_output = len(train[0][1])
    network = NeuralNet((num_input, hidden, num_output))
    network.train(train, test, debug=True)
    if network.save(pcas, outputfile):
        print "Saved nn successfully"
    else: print "Error while saving nn"


def validateNN( nnfile ):
    try:
        res = loadNN( nnfile )
        if res is not None:
            print "Valid NeuralNet file."
        else: print "INVALID NeuralNet file, please regenerate."
    except: print "INVALID NeuralNet file, please regenerate."

def testWord( nnfile, word ):
    pcas, nn = loadNN( nnfile )
    
#TODO: test the word.
    print "Not implemented yet! Sorry!"

def splitTrainingSet( trainFile, splitSize ):
    if splitSize < 0 or splitSize > 1:
        print "Split size must be within 0.0 and 1.0 NON-inclusive."
        return
    dat = []
    f = PhonemeDataFile( trainFile )
    for word in f.readWord():
        dat.append(word)
    shuffle(dat)

    split = int(splitSize * len(dat))
    firstHalf = dat[:split]
    secondHalf = dat[split:]

    fname,ext = os.path.splitext(trainFile)

    with open( fname+"_1"+ext, 'w' ) as a:
        for (word,deff) in firstHalf:
            a.write(word)
            a.write(deff)
    with open( fname+"_2"+ext, 'w' ) as b:
        for (word,deff) in secondHalf:
            b.write(word)
            b.write(deff)
    print "Success, your two files are located at:"
    print "%s_1%s  and  %s_2%s"%(fname,ext,fname,ext)


def main(opts):
    print opts
    if opts.trainfile is not None:
        if opts.splitsize is not None:
            splitTrainingSet(opts.trainfile, opts.splitsize)
        else:
            makeNN( opts.trainfile, opts.savefile, opts.numhidden, opts.pca )
    elif opts.nnfile is not None:
        if opts.word is not None:
            testWord( opts.nnfile, opts.word )
        else:
            validateNN( opts.nnfile )
    else: gen_optparse().print_usage()

if __name__ == "__main__":
    parser = gen_optparse()

    options, args = parser.parse_args()
    if len(args) > 0 or len(sys.argv)==1:
        parser.print_usage()
    else: main(options)

