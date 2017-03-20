import sys, os
import time

sys.path.append(os.getcwd()+"\DLfromScratch")
from dataset.mnist import load_mnist
import numpy as np
from PIL import Image #Python Image Library
import pickle

from functions import *

def get_train_data():
    (x_train, t_train), (x_test, t_test) = \
    load_mnist(flatten=True, one_hot_label=True)

    return x_train, t_train


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

def get_mini_batch(x, t):
    data_size = x.shape[0]
    batch_size = 10
    batch_mask = np.random.choice(data_size, batch_size)

    return x[batch_mask], t[batch_mask]


def _main():
    x_train, t_train = get_train_data()
    x_batch, t_batch = get_mini_batch(x_train, t_train)
    network = init_network()

    y_batch = predict(network, x_batch)
    print(y_batch[0])
    print(y_batch[0, 3])
    print(y_batch[0][3])
    #print(cee(y_batch, t_batch))

if __name__=='__main__':
    _main()

