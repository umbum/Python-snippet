import sys
import glob
import os

fullpaths = glob.glob("D:\\WSB\\#HyperSlave\\GIT\\Python\\study\\*")


files=[]
for i in range(len(fullpaths)):
    files.append(os.path.split(fullpaths[i])[1])

files2 = list(map(lambda x: os.path.split(x)[1], fullpaths))

print(files2)

for i in files:
    print(i)

'''
files2 = os.listdir("D:\\WSB\\#HyperSlave\\GIT\\Python\\study")
for i in files2:
    print(i)
'''

