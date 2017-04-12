#coding: utf-8
import os, sys
import glob
import re



files=glob.glob("D:\\스터디\\ML\\coursera machine-learning\\*\\*\\*.[!ke][!o].srt")
print(len(files))
print(files[0:3])

for f in files:
    os.unlink(f)