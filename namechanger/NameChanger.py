#-*- coding: utf-8 -*-
import os
import sys
import glob

#파일(디렉토리) 이름으로 \ / : * ? " < > | 를 사용할 수 없다.


dir = input("target dir : ")

try:
    files = os.listdir(dir)
except WindowsError:
    print("dir error")
    sys.exit()

