#!/usr/bin/env python
#
# Run some tests on our Neural Net and feature extractor.
#
import profile
import sys

from FeatureGenerator import FeatureGenerator
from PhonemeDataFile import PhonemeDataFile
from network import NeuralNet
from random import shuffle


def genFeatures(filename):
    fgen = FeatureGenerator(PhonemeDataFile(filename))
    features = list(fgen.features_vector())
    shuffle(features)
    pivot = int(len(features) * 0.8)
    test,train = features[pivot:],features[:pivot]
    return test,train

def trainOnFeatures(filename):
    train,test = genFeatures(filename)
    nin,nout = len(train[0][0]),len(train[0][1])
    net = NeuralNet( (nin, 20, nout) )
    num_epochs = net.train( train, test )
    return net,test

def testOnNet(filename):
    net,test = trainOnFeatures(filename)
    net.test(test)

def test1(f):
    profile.run('genFeatures("%s")'%f)

def test2(f):
    profile.run('trainOnFeatures("%s")'%f)

def test3(f):
    profile.run('testOnNet("%s")'%f)


if __name__ == "__main__":
    tests = [test1,test2,test3]
    
    if len(sys.argv)!=3:
        print "Usage:\n\t%s <datafile> <test_number>"
        print "*Note: there are 1 to %d tests to choose from."%len(tests)
    else: 
        f = sys.argv[1]
        i = int(sys.argv[2])-1
        tests[i](f)
