import requests
import time
from datetime import datetime
import subprocess

url = "https://www.drmartens.co.kr/product/sandals-nikolai-tan-westfield"
soldout_str = 'soldout","opt_string":"280'

applescript = """
display dialog "280 품절 아님!" ¬
with title "280 품절 아님!" ¬
with icon caution ¬
buttons {"OK"}
"""


while (True):
    r = requests.get(url)
    if (r.text.find(soldout_str) != -1):
        # 품절임
        print(str(datetime.now()) + " 280 soldout")
    else:
        # 품절이 아님
        print(str(datetime.now()) + "280 품절 아님!!!")
        subprocess.call("osascript -e '{}'".format(applescript), shell=True)
    
    time.sleep(30)