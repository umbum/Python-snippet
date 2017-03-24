import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread

def eg_pyplot():
    x = np.arange(0, 6, 0.1)
    y1 = np.sin(x)
    y2 = np.cos(x)

    plt.figure(1)
    plt.plot(x, y1, label="sin")
    plt.figure(2)
    plt.plot(x, y2, linestyle="--", label="cos")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("sin & cos")
    plt.legend()
    plt.show()

    

def eg_image():
    img = imread('C:\BUM\GIT\Python\DLfromScratch\lena.jpg')

    plt.imshow(img)
    plt.show()

if __name__ == "__main__":
    eg_pyplot()