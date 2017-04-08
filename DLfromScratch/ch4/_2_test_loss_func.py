import sys, os

import numpy as np

sys.path.append(os.getcwd()+"\DLfromScratch")
from functions import *

def _main():
    y = np.array([0.1, 0.05, 0.6, 0.0, 0.05, 0.1, 0.0, 0.1, 0.0, 0.0])
    t = np.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 0])

    print(mse(y, t))
    print(cee(y, t))


if __name__=='__main__':
    _main()
