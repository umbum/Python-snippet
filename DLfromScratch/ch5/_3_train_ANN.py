import sys, os

import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.getcwd()+"\DLfromScratch")
from dataset.mnist import load_mnist
from _1_two_layer_net import TwoLayerNet
from optimizer import *

def _main():
    (x_train, t_train), (x_test, t_test) = \
    load_mnist(normalize=True, one_hot_label=True)

    net = TwoLayerNet(input_size=784, hidden_size=50, output_size=10)

    iters_num = 6001
    batch_size = 100
    train_size = x_train.shape[0]
    optimizer = SGD(lr=0.1)

    train_loss_list = []
    train_acc_list = []
    test_acc_list = []

    iter_per_epoch = max(train_size / batch_size, 1)

    for i in range(iters_num):
        batch_mask = np.random.choice(train_size, batch_size)
        x_batch = x_train[batch_mask]
        t_batch = t_train[batch_mask]

        grads, loss = net.gradient(x_batch, t_batch)

        optimizer.update(net.params, grads)

        train_loss_list.append(loss)

        if i % iter_per_epoch == 0:
            train_acc = net.accuracy(x_train, t_train)
            test_acc = net.accuracy(x_test, t_test)
            
            train_acc_list.append(train_acc)
            test_acc_list.append(test_acc)
            
            print(i, "th iter")
            print("train_acc : ", train_acc)
            print("test_acc : ", test_acc)
    
    return train_loss_list, train_acc_list, test_acc_list

if __name__ == "__main__":

    train_loss_list, train_acc_list, test_acc_list = _main()
    
    x = np.arange(0, len(train_loss_list), 1)
    plt.figure(1)
    plt.plot(x, train_loss_list)

    plt.figure(2)
    x = np.arange(0, len(train_acc_list), 1)
    plt.plot(x, train_acc_list, label="train_acc")
    plt.plot(x, test_acc_list, label="test_acc", linestyle="--")
    
    plt.legend()
    plt.show()


