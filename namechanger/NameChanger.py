#-*- coding: utf-8 -*-
import os
import sys
import re

#파일(디렉토리) 이름으로 \ / : * ? " < > | 를 사용할 수 없다.

dir = os.path.dirname(os.path.realpath(__file__)) + "/"

po = re.compile(r"^[0-9]*\s+")
try:
    filelist = os.listdir(dir)
except WindowsError:
    print("dir error")
    sys.exit()

for f in filelist:
    m = po.search(f)
    if m:
        os.rename(dir+ f, dir+ f[m.end():])

