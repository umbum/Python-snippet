import sys, os

import numpy as np

sys.path.append(os.getcwd()+"\DLfromScratch")
from common.util import im2col


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

if __name__=="__main__":
    x1 = np.random.rand(1, 3, 7, 7)
    col1 = im2col(x1, 5, 5, stride=1, pad=0)
    print(col1.shape)

    x2 = np.random.rand(10, 3, 7, 7)
    col2 = im2col(x2, 5, 5, stride=1, pad=0)
    print(col2.shape)
