import sys, os

import numpy as np
from collections import OrderedDict
import pickle

sys.path.append(os.getcwd()+"\DLfromScratch")
from common.layers import *


'''
conv - relu - pool - affine - relu - affine - softmax
'''
class SimpleConvNet:
    def __init__(self, input_shape=(1, 28, 28), conv_param={'filterNumber':30, 'filterSize':5, 'pad':0, 'stride':1}, hidden_size=100, output_size=10, weight_init_std=0.01):
        FN = conv_param['filterNumber']
        FHW = conv_param['filterSize']
        pad = conv_param['pad']
        stride = conv_param['stride']
        C = input_shape[0]
        HW = input_shape[1]
        OHW = int((HW + 2*pad - FHW)/stride + 1)
        #원래는 pool_param도 입력 받아야 하지만 그냥 이렇게 처리 2x2 pooling
        pool_output_cube = int(FN * (OHW/2) * (OHW/2))
        
        self.params = {}
        self.params['W1'] = weight_init_std * \
        np.random.randn(FN, C, FHW, FHW)
        '''??? 왜 ((FN, 1, 1))을 넣으면 안되는거지? 모양이 다른건 알겠는데
        2차원 행렬로 전개한 상태에서 b를 더하게 되는데, (N*OH*OW, FN) + (FN, 1, 1)을 더하게 되니까
        브로드캐스트가 이상하게 적용되어 오류가 발생.
        그래서 ((FN, 1, 1))을 사용하려면 4차원으로 reshape한 다음 b를 더해줘야 하며
        grads['b1'] = self.layers['Conv1'].db 에서 grads['b1']을 (FN, 1, 1)로 reshape해줘야
        optimizer.update()에서 에러가 발생하지 않는다.
        '''
        self.params['b1'] = np.zeros(FN)
        self.params['W2'] = weight_init_std * \
        np.random.randn(pool_output_cube, hidden_size)
        self.params['b2'] = np.zeros(hidden_size)
        self.params['W3'] = weight_init_std * \
        np.random.randn(hidden_size, output_size)
        self.params['b3'] = np.zeros(output_size)

        self.layers = OrderedDict()
        self.layers['Conv1'] = Convolution(self.params['W1'], self.params['b1'], stride, pad)
        self.layers['Relu1'] = Relu()
        self.layers['Pool1'] = Pooling(pool_h=2, pool_w=2, stride=2)
        
        self.layers['Affine2'] = Affine(self.params['W2'], self.params['b2'])
        self.layers['Relu2'] = Relu()
        
        self.layers['Affine3'] = Affine(self.params['W3'], self.params['b3'])
        self.lastlayer = SoftmaxWithLoss()
        
    def predict(self, x):
        for layer in self.layers.values():
            x = layer.forward(x)
        return x

    def loss(self, x, t):
        y = self.predict(x)
        return self.lastlayer.forward(y, t)

    def accuracy(self, x, t, batch_size=100):
        if t.ndim != 1 : t = np.argmax(t, axis=1)
        
        acc = 0.0
        
        for i in range(int(x.shape[0] / batch_size)):
            tx = x[i*batch_size:(i+1)*batch_size]
            tt = t[i*batch_size:(i+1)*batch_size]
            y = self.predict(tx)
            y = np.argmax(y, axis=1)
            acc += np.sum(y == tt) 
        
        return acc / x.shape[0]

    def gradient(self, x, t):
        lossValue = self.loss(x, t)

        dout = self.lastlayer.backward(1)

        re_layers = list(self.layers.values())
        re_layers = re_layers[::-1]

        for layer in re_layers:
            dout = layer.backward(dout)

        grads = {}
        grads['W1'] = self.layers['Conv1'].dW
        grads['b1'] = self.layers['Conv1'].db
        grads['W2'] = self.layers['Affine2'].dW
        grads['b2'] = self.layers['Affine2'].db
        grads['W3'] = self.layers['Affine3'].dW
        grads['b3'] = self.layers['Affine3'].db

        return grads, lossValue
    
    def save_params(self, filename="params.pkl"):
        with open(filename, mode='wb') as f:
            pickle.dump(self.params, f)
        
    def load_params(self, filename="params.pkl"):
        with open(filename, mode='rb') as f:
            self.params = pickle.load(f)
        
        for i, key in enumerate(['Conv1', 'Affine2', 'Affine3']):
            self.layers[key].dW = self.params['W'+str(i+1)]
            self.layers[key].db = self.params['b'+str(i+1)]


if __name__ == "__main__":
    x = np.zeros((3,1,1))
    x2 = np.zeros(3)
    print(x)
    print(x2)
    d = {}
    d['w'] = 3
    for i, j in d.items():
        print(i, j)