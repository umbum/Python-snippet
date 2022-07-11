#-*- coding: utf-8 -*-

import os, sys
from datetime import date, timedelta


targetYear = int(os.environ['targetYear'])

first_day = date(targetYear, 1, 1)
first_day_of_the_next_year = date(targetYear+1, 1, 1)

print("### 대상 [{} ~ {})".format(first_day, first_day_of_the_next_year))
sys.stdout.flush()

i_day = first_day
while True:
    paramDate = i_day.strftime("%Y-%m-%d")
    print("### 실행 파라미터 일자 {0}".format(paramDate))
    sys.stdout.flush()
    result = os.system('job.sh "interpretCompleteDate={0}"'.format(paramDate))
    if result != 0:
        raise Exception("### 진행 중 실패 {0} {1}".format(paramDate, result))

    i_day += timedelta(days=1)
    if i_day >= first_day_of_the_next_year:
        break