#-*- coding : utf-8 -*-
import os
import re


tasklist = os.popen("tasklist /nh", 'r')

po = re.compile(r'(.+?)(?:\s\s+)(\d+)(?:.+?\d+\s+)([\d, ]+ K)')
#po = re.compile(r'([\w.]+(?: [\w.]+)*)\s\s+(\d+) \w+\s\s+\d+\s\s+([\d, ]+ K)')

for line in tasklist:
    s = po.match(line)
    if s:       #첫번째line이 None type으로 반환되기 때문에 에러난다.
        print(s.group(1))

