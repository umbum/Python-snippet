import os, sys

import numpy as np
import matplotlib.pyplot as plt

from _4_two_layer_net import TwoLayerNet
sys.path.append(os.getcwd() + "\DLfromScratch")
from dataset.mnist import load_mnist


def _main():
    (x_train, t_train), (x_test, t_test) = \
    load_mnist(normalize=True, one_hot_label = True)

    train_loss_list = []

    #Hyper Parameters
    iters_num =1000
    train_size = x_train.shape[0]
    batch_size = 20
    lr = 0.1
    network = TwoLayerNet(input_size=784, hidden_size=10, output_size=10)

    for i in range(iters_num):
        print(i, " ", end="")

        batch_mask = np.random.choice(train_size, batch_size)
        x_batch = x_train[batch_mask]
        t_batch = t_train[batch_mask]

        g = network.wrap_gradient(x_batch, t_batch)
        #g는 params에 대한 손실 함수의 gradient params와 shape이 같은 dictionary다.
        print("very very slow numerical gradient")
        for key in network.params:
            network.params[key] -= lr * g[key]

        loss = network.loss(x_batch, t_batch)
        train_loss_list.append(loss)

        

    return train_loss_list
    

if __name__ == "__main__":
    y = _main()
    print(y[-1])
    x = np.arange(0, 1000, 1)
    
    plt.plot(x, y)
    plt.show()
