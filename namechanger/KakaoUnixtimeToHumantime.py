import os, sys
import re
from datetime import datetime

# 1296791749731.jpg -> (1296791749)731(.jpg) -> 
po = re.compile(r"([0-9]{10})([\w-]*)(\..+)")
current_dir = os.path.dirname(os.path.realpath(__file__)) + "\\"

try:
    _file_list = os.listdir(current_dir)
except WindowsError:
    print("dir error")
    sys.exit()

file_list = list(filter(lambda x: x not in __file__, _file_list))

for fname in file_list:
    m = po.search(fname)
    if m:
        human_readable_time = datetime.fromtimestamp(int(m[1])).strftime("%Y%m%d_%H%M%S")
        new_fname = "{}_{}{}".format(human_readable_time, m[2], m[3])
        print("{} -> {}".format(fname, new_fname))
        os.rename(current_dir + fname, current_dir + new_fname)
    else:
        print("doesn't matched : {}".format(fname))
    