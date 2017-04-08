import sys, os
import time

sys.path.append(os.getcwd()+"\DLfromScratch")
from dataset.mnist import load_mnist
import numpy as np
from PIL import Image #Python Image Library
import pickle

from functions import *

def get_data():
    (x_train, t_train), (x_test, t_test) = load_mnist(flatten=True, normalize=False)

    return x_test, t_test


def init_network():
    with open(".\DLfromScratch\dataset\sample_weight.pkl", 'rb') as f:
        network = pickle.load(f)
    return network


def predict(network, x):
    W1, W2, W3 = network['W1'], network['W2'], network['W3']
    b1, b2, b3 = network['b1'], network['b2'], network['b3']

    a1 = np.dot(x, W1) + b1
    z1 = sigmoid(a1)
    a2 = np.dot(z1, W2) + b2
    z2 = sigmoid(a2)
    a3 = np.dot(z2, W3) + b3
    y = softmax(a3)

    return y


def _main():
    x, t = get_data()
    network = init_network()

    accuracy_cnt = 0
    batch_size = 1000   
    start = time.time()
    for i in range(0, len(x), batch_size):
        x_batch = x[i:i+batch_size]
        y_batch = predict(network, x_batch)
        p = np.argmax(y_batch, axis=1)
        accuracy_cnt += np.sum(p == t[i:i+batch_size])

    print("Accuracy:" + str(float(accuracy_cnt) /len(x)))
    end = time.time() - start
    print("TIME:"+str(end))

if __name__=='__main__':
    _main()

