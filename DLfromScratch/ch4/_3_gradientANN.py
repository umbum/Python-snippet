import sys, os

import numpy as np

sys.path.append(os.getcwd() + "\DLfromScratch")
from functions import *

class simpleNet:
    def __init__(self):
        self.W = np.random.randn(2, 3)

    def predict(self, x):
        return np.dot(x, self.W)
    
    def loss(self, x, t):
        z = self.predict(x)
        y = softmax(z)
        
        return cee(y, t)

        
    

net = simpleNet()

x = np.array([0.6, 0.9])
t = np.array([0, 0, 1])

#def f(W):
    #return net.loss(x)

f = lambda w: net.loss(x, t)
numerical_gradient(f, net.W)