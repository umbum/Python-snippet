import matplotlib.pyplot as plt
import numpy as np


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

#loss function
def mse(y, t):
    if y.ndim == 1:
        y = y.reshape(1, y.size)
        t = t.reshape(1, t.size)
    return 0.5*np.sum((y-t)**2)/y.shape[0]

def cee(y, t):
    delta = 1e-7
    if y.ndim == 1:
        y = y.reshape(1, y.size)
        t = t.reshape(1, t.size)

    if t.size == y.size:
        t = t.argmax(axis=1)
    return -np.sum(t*np.log(y[np.arange(y.shape[0]), t]))/y.shape[0]

#differential
def numerical_diff(f, x):
    h = 1e-4
    return (f(x+h) - f(x-h))/ (2*h)

def tangent_line(f, x, a):
    g = numerical_diff(f, a)
    return g*(x-a) + f(a)


def numerical_gradient(f, x):
    h = 1e-4 # 0.0001
    grad = np.zeros_like(x)
    
    it = np.nditer(x, flags=['multi_index'], op_flags=['readwrite'])

    while not it.finished:
        idx = it.multi_index
        tmp_val = x[idx]
        x[idx] = float(tmp_val) + h
        fxh1 = f(x) # f(x+h)
        
        x[idx] = tmp_val - h 
        fxh2 = f(x) # f(x-h)
        grad[idx] = (fxh1 - fxh2) / (2*h)
        
        x[idx] = tmp_val #restore
        it.iternext()   
        
    return grad

def gradient_descent(f, init_x, lr=0.01, step_num=100):
    x = init_x
    for i in range(step_num):
        g = numerical_gradient(f, x)
        x -= lr * g
    return x

def function_1(x):
    return 0.1*x**2 + 1*x

def function_2(x):
    return x[0]**2 + x[1]**2


def graph():
    x = np.arange(0, 20, 0.1)
    y1 = softmax(x)
    #y2 = tangent_line(function_1, x, 5)
    plt.plot(x, y1)
    #plt.plot(x, y2)
    plt.show()



if __name__ == '__main__':
    graph()
    #x = np.array([1010, 1000, 990])
    #print(np.sum(softmax(x)))
    
    #print(gradient_descent(function_2, np.array([3.0, 4.0]), lr=0.1))
