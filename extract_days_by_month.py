#-*- coding: utf-8 -*-

import os, sys
from datetime import datetime
from calendar import monthrange

targetMonth = str(os.environ['targetMonth'])
print("### 대상 월 {0}".format(targetMonth))
sys.stdout.flush()

dt = datetime.strptime(targetMonth, "%Y%m")
_, days = monthrange(dt.year, dt.month)

for day in range(1, days+1):
    dt = dt.replace(day=day)
    paramDate = dt.strftime("%Y-%m-%d")
    print("### 실행 파라미터 일자 {0}".format(paramDate))
    sys.stdout.flush()
    result = os.system('job.sh "interpretCompleteDate={0}"'.format(paramDate))
    if result != 0:
      raise Exception("### 진행 중 실패 {0} {1}".format(paramDate, result))