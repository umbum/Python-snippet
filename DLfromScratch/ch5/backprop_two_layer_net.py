import sys, os

import numpy as np
sys.path.append(os.getcwd()+"\DLfromScratch")
from functions import *
from layers import *

class TwoLayerNet():
    def __init__(self, input_size, hidden_size, output_size, weight_init_std=0.01):
        self.params = {}
        self.params['W1'] = weight_init_std * \
        np.random.randn(input_size, hidden_size)
        self.params['b1'] = np.zeros(hidden_size)
        self.params['W2'] = weight_init_std * \
        np.random.randn(hidden_size, output_size)
        self.params['b2'] = np.zeros(output_size)
        
        self.layers = {}
        self.layers['Affine1'] = Affine(self.params['W1'], self.params['b1'])
        self.layers['ReLU1'] = ReLU()
        self.layers['Affine2'] = Affine(self.params['W2'], self.params['b2'])
        
        self.lastLayer = SoftmaxWithLoss()

    def predict(self, x):
        for layer in self.layers.values():
            x = layer.forward(x)
        
        return x

    def loss(self, x, t):
        y = self.predict(x)

        return self.lastLayer.forward(y, t)

    def accuracy(self, x, t):
        y = self.predict(x)
        y = np.argmax(y, axis=1)
        if t.ndim != 1:
            t = np.argmax(t, axis=1)
        
        return np.sum(y==t) / x.shape[0]

    def gradient(self, x, t):
        self.loss(x, t)

        dout = self.lastLayer.backward(1)
        
        relayers = list(self.layers.values).reverse()

        for layer in relayers:
            dout = layer.backward(dout)
        
        g = {}
        g['W1'] = self.layers['Affine1'].dW

        



if __name__=="__main__":

    dic = {}
    dic['a'] = 1
    dic['b'] = 2
    li = list(dic.values())
    
    for i in li:
        print(i)

