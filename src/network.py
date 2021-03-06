"""

"""
import math
import random
import time
import pickle

from numpy import concatenate, mat, multiply, ones, power, vectorize, zeros
from numpy.random import rand

def timef(f, *args, **kwargs):
    """Measures the runtime of the provided function and arguments."""
    start = time.time()
    f(*args, **kwargs)
    end = time.time()
    ms = (end - start) * 1000
    print('Execution time: %s ms.' % ms)
    return ms

@vectorize
def sigmoid(x):
    if x > 25:
        return 1.0
    elif x < -25:
        return 0.0
    else:
        return 1 / (1 + math.exp(-1 * x))

@vectorize
def dsigmoid(x):
    """Calculates the derivative of the sigmoid of x."""
    if x > 25 or x < -25:
        return 0.0
    else:
        return math.exp(x) / (1 + math.exp(x))**2

def class_to_truth(cls_num, num_classes):
    """Converts the class into a truth vector."""
    truth = zeros((num_classes,))
    truth[int(cls_num)] = 1
    return truth

def truth_to_class(truth):
    """Converts a truth vector into the class."""
    return max((x,i) for i,x in enumerate(truth))[1]

def pad(x):
    """Adds a row of 1's to the top of a vector."""
    cols = x.shape[1]
    return concatenate((mat(ones((1,cols))), x))


def loadNN(filename):
    """ Returns a NeuralNet that was saved to a file using NeuralNet.save() """
    try:
        pcas, phones, nn = None, None, None
        with open(filename,'r') as f:
            dat = pickle.load(f)
            pcas = dat["pcas"]
            phones = dat["phones"]
            nn = dat["nn"]
        return pcas,phones,nn
    except: return None, None, None
                

class NeuralNet(object):
    def __init__(self, structure, learning_rate=0.1):
        self.structure = list(structure)
        self.lr = learning_rate
        self.reset_weights()

    @property
    def num_outputs(self):
        return self.structure[-1]

    def reset_weights(self):
        self.weights = []
        for i in range(len(self.structure) - 1):
            inp = self.structure[i]
            out = self.structure[i + 1]
            self.weights.append(mat(rand(inp + 1, out)) * 2 - 1)

    def backprop(self, sample, return_values=False):
        input = mat(sample[0]).T
        truth = mat(sample[1]).T

        sums, outputs = self.run(input.T, verbose=True)
        inputs = [input]
        inputs.extend(outputs[:-1])
        errors = []

        # calculate errors at each layer
        error = truth - outputs[-1]
        errors.insert(0, error)
        for weights in reversed(self.weights[1:]):
            error = (errors[0].T * weights.T).T[1:]
            errors.insert(0, error)

        # update each set of weights
        for i, weights in enumerate(self.weights):
            input = inputs[i]
            sum = sums[i]
            error = errors[i]

            adjustments = self.lr * pad(input) * multiply(error.T, dsigmoid(sum.T))
            self.weights[i] = self.weights[i] + adjustments

        if return_values:
            return sums, outputs, errors, self.weights
       

    def train(self, samples, test, epochs=500, train_size=1000, val_size=500, debug=False):
        best_rmse = 9000000001
        best_weights = []
        epochs_since_best = 0

        if train_size > len(samples):
            train_size = len(samples)*0.8
        if val_size > len(samples):
            val_size = len(samples)*0.2

        cur_set = samples
        try:
            for num_epoch in range(epochs):
                if epochs_since_best > 50:
                    break

                if len(samples) > train_size + val_size:
                    cur_set = random.sample(samples, train_size + val_size)
                    cur_train = cur_set[:train_size]
                    cur_val = cur_set[-val_size:]
                else:
                    split = int((float(train_size) / train_size + val_size) * len(samples))
                    cur_set = random.sample(samples, len(samples))
                    cur_train = cur_set[:split]
                    cur_val = cur_set[split:]
                for s in cur_train:
                    self.backprop(s)

                misclassified, rmse, _ = self.test(cur_val, to_print=False)
                if rmse < best_rmse:
                    best_rmse = rmse
                    best_weights = list(self.weights)
                    epochs_since_best = 0
                else:
                    epochs_since_best += 1

                if debug:
                    print('Epoch %d, \tRMSE: %f' % (num_epoch, rmse))        
        except KeyboardInterrupt:
            pass
        self.weights = best_weights

        print('\n---Final Results:---')
        print('epochs: %d' % (num_epoch - 1))
        self.test(test)


    def save(self, pcas, phones, filename):
        try:
            with open(filename,'w') as f:
                dat = {"nn":self,"phones":phones,"pcas":pcas}
                pickle.dump(dat,f)
            return True
        except: return False   

    def run(self, input, verbose=False):

        # if input is a tuple, it is (input, output) - we want input only
        if type(input) == tuple:
            input = input[0]

        output = mat(input).T
        sums = []
        outputs = []

        for weights in self.weights:
            sum = (pad(output).T * weights).T
            output = sigmoid(sum)
            sums.append(sum)
            outputs.append(output)

        if verbose:
            return sums, outputs
        else:
            return output

    def test(self, samples, to_print=True):
        error_sum = 0
        num_miss = 0
        confusion = [[0] * self.num_outputs for _ in range(self.num_outputs)]
        for s in samples:
            input = s[0]
            truth = s[1]

            output = self.run(input)

            o = truth_to_class(output)
            t = truth_to_class(truth)
            confusion[o][t] += 1
            if o != t:
                num_miss += 1

            error = power(truth - output.T, 2).sum() / len(truth)
            error_sum += error

        misclassified = float(num_miss) / len(samples)
        rmse = math.sqrt(error_sum / len(samples))

        if to_print:
            print('misclassified: %f' % misclassified)
            print('rmse: %f' % rmse)
            if len(confusion) < 30:
                print('confusion:')
                print(confusion)

        return misclassified, rmse, confusion

    def time(self, function, samples, num_runs=1000):
        start = time.time()
        for i in range(num_runs):
            function(samples[i % len(samples)])
        end = time.time()

        print 'Total time: %f s' % (end - start)
        print 'Average time: %f ms per run' % ((end - start) / num_runs * 1000)
