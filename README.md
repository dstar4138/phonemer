# Phonemer: Grapheme-to-Phoneme classifier #

This application was a Natural Language Processing class project at RIT to 
determine word pronunciations. It also examines the abilities of Neural 
Networks as classifiers of Phonemes. 

Please note that we did not include a data set in this repo, but a previously
trained Neural Net instead. Use this .nn file for testing purposes. If you
would like train one yourself, you will need to look for a dataset with
aligned graphemes and phonemes. We suggest looking at the PMTools paper by
Richard Sproat (2001).


## How to Use Phonemer##

### For finding the pronunciation of a word? ###

A NeuralNet file is needed to know how to pronounce a word correctly, we have 
trained one for you and its located in the 'nets' directory. To load the nn and
check the pronunciation of a word, run the following:

    cd src
    ./phonemer.py -t ../nets/saved.nn -w <YOUR WORD HERE>

By replacing '<YOUR WORD HERE>' with a random word, you will get a print out
of the pronunciation, character by character.


### For generating a new neural net file? ###

A neural netfile is just a pickled representation of our NeuralNet class. To 
generate one you would need an aligned dataset that we can generate enough
features to train the network. Please see our PhonemeDataFile class for more
information on how we parse a dataset. Otherwise you can substitute your own
parsing class.


The neural net can be customized and tweaked in order to tune on a specific
dataset or language. Some options for tuning are as follows:

* -n = Change the number of nodes per hidden layer. We've found that around 100
      is best. Must be > 0, default is 100

* -l = Change the number of hidden layers. Typically this isn't as useful as 
      the previous option but we provided it anyway. Must be > 0, default is 1.

* -p = Run PCA algorithm over the feature vectors before classification. Must
      be > 0, default is disabled.

An example command for generating nn file:

    cd src
    ./phonemer.py -d ../data/dataset.dat -n 150 -l 1 -f ../nets/saved2.nn

This will save a neural net with 150 nodes on 1 hidden layer to `../nets/saved2.nn`.


### For splitting a large dataset up for testing? ###

Sometimes datasets are larger than you need them to be for development purposes.
Phonemer can split your dataset up for you based on a percentage:

    cd src
    ./phonemer.py -d ../data/large.dat -s 0.8

This will split large.dat dataset into two large\_1.dat and large\_2.dat in 80%
and 20% chunks.



