#-*- coding:utf-8 -*-
'''
순방향 입력 x, x2, ...
순방향 출력 y
역방향 입력 dout
'''
import numpy as np
from common.util import im2col

#from functions import *

class MulLayer:
    def __init__(self):
        self.x = None
        self.x2 = None

    def forward(self, x, x2):
        self.x = x
        self.x2 = x2
        return x*x2

    def backward(self, dout):
        dx = dout * self.x2
        dx2 = dout * self.x

        return dx, dx2

class AddLayer:
    def __init__(self):
        pass
    
    def forward(self, x, x2):
        return x+x2
    
    def backward(self, dout):
        return dout, dout

class ReLU:
    def __init__(self):
        self.mask = None
    
    def forward(self, x):
        self.mask = x <= 0
        out = x.copy()
        out[self.mask] = 0
        return out
        
    def backward(self, dout):
        dx = dout.copy()
        dx[self.mask] = 0
        
        return dx

class Sigmoid:
    def __init__(self):
        self.y = None

    def forward(self, x):
        self.y = 1/(1+np.exp(-x))
        return self.y
    
    def backward(self, dout):
        return dout*self.y*(1-self.y)

class Affine:
    def __init__(self, W, b):
        self.W = W
        self.b = b
        self.x = None
        self.dW = None
        self.db = None
    
    def forward(self, x):
        self.x = x
        out = np.dot(x, self.W) + self.b
        return out

    def backward(self, dout):
        dx = np.dot(dout, self.W.T)
        self.dW = np.dot(self.x.T, dout)
        self.db = np.sum(dout, axis=0)

        return dx

class SoftmaxWithLoss:
    def __init__(self):
        self.loss = None
        self.y = None
        self.t = None   #one-hot-vector
    
    def forward(self, x, t):
        self.t = t
        self.y = softmax(x)
        self.loss = cee(self.y, self.t)
        return self.loss
    
    def backward(self, dout=1):
        batch_size = self.t.shape[0]
        if self.t.size == self.y.size:
            dx = (self.y - self.t) / batch_size
        
        return dx
        '''
        아니 왜 batch_size로 나누지??
        np.sum( , axis=0)으로 같은 column끼리 더하면 batch_size로
        나눠줘야 하겠지만 그것도아닌데
        x는 입력 데이터에 대한 최종 출력 y이니까
        n*10일거고, softmax를 통과한 (여기서의)y도 n*10
        t도 n*10이니까 dx도 n*10인데 왜?? 갑자기 batch_size로 나누는거지?
        '''
        
 class Convolution:
    def __init__(self, W, b, stride=1, pad=0):
        self.W = W
        self.b = b
        self.stride = stride
        self.pad = pad

    def forward(self, x):
        FN, C, FH, FW = self.W.shape
        N, C, H, W = x.shape

        OH = int((H + 2*self.pad - FH)/self.stride +1)
        OW = int((W + 2*self.pad - FW)/self.stride +1)

        col_x = im2col(x, FH, FW, self.stride, self.pad)
        col_W = self.W.reshape(FN, -1).T


        result_2d = np.dot(col_x, col_W) + self.b
        result = result_2d.reshape(N, OH, OW, FN).transpose(3, 0, 1, 2)
        
        return result       


def apple():
    apple_cost = 100
    apple_num = 2
    tax = 1.1

    mul_apple_layer = MulLayer()
    mul_tax_layer = MulLayer()

    apple_price = mul_apple_layer.forward(apple_cost, apple_num)
    price = mul_tax_layer.forward(apple_price, tax)

    print(price)

    dprice=1
    dapple_price, dtax = mul_tax_layer.backward(dprice)
    dapple_cost, dapple_num = mul_apple_layer.backward(dapple_price)

    print(dapple_cost, dapple_num, dtax)

if __name__ == "__main__":
    x = np.array([1, 3, 5, 7, 9])
    #t = np.array([0, 0, 0, 0, 0, 0, 1])
    #s = SoftmaxWithLoss()
    #print(s.forward(x,t))
    #print(s.backward(1))
    s = Sigmoid()
    print(s.forward(x))
