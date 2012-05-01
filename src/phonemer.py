#!/usr/bin/env python
#
# Usage:
#   ./phonemer.py [--train=<TRAINING_FILE>] <WORD>
# 

import sys
import nltk
from FeatureGenerator import FeatureGenerator
from PhonemeDataFile import PhonemeDataFile
from network import	NeuralNet
from random import shuffle

__usage__ = "%s [--train=<TRAINING_FILE>] <WORD>"

def main(filename):
	fgen = FeatureGenerator(PhonemeDataFile(filename))
	features = list(fgen.features_vector())
	shuffle(features)
	split = int(len(features) * 0.8)
	train = features[split:]
	test = features[:split]
	
	num_input = len(train[0][0])
	num_output = len(train[0][1])
	network = NeuralNet((num_input, 20, num_output))
	network.train(train, test)

if __name__ == "__main__":
	if len(sys.argv) > 1:
		main(sys.argv[1])
	else:
		print __usage__%sys.argv[0]
