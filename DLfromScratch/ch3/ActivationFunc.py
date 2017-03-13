import numpy as np
import matplotlib.pyplot as plt

def identity_function(x):
    return x

#SLP
def step_function(x):
    return np.array(x >0, dtype=np.int)

#MLP
def sigmoid(x):
    return 1/(1+np.exp(-x))

def relu(x):
    return np.maximum(0, x)

def softmax(x):
    c = np.max(x)
    return np.exp(x-c)/np.sum(np.exp(x-c))

def graph():
    x = np.arange(-10, 10, 0.1)
    y = relu(x)
    plt.plot(x, y)
    plt.show()



if __name__ == '__main__':
    #graph()
    x = np.array([1010, 1000, 990])
    print(softmax(x))