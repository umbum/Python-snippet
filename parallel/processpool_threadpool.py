import os, sys
import csv
import glob
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from threading import Lock
from time import sleep, ctime
import queue

start_date = sys.argv[1]
end_date = sys.argv[2]

path_dir = "/Users/user/Documents/parsed"
whole_fpaths = glob.glob(os.path.join(path_dir, "**/*.csv"))

start_fname = start_date + '.csv'
end_fname = end_date + '.csv'

target_fpaths = sorted([fpath for fpath in whole_fpaths if start_fname <= os.path.basename(fpath) <= end_fname])


##########################

class ThreadPoolExecutorWithQueueSizeLimit(ThreadPoolExecutor):
    def __init__(self, max_size=100000, *args, **kwargs):
        super(ThreadPoolExecutorWithQueueSizeLimit, self).__init__(*args, **kwargs)
        self._work_queue = queue.Queue(maxsize=max_size)

class Requester:
    def __init__(self, target_fpath):
        self.target_fpath = target_fpath
        self.thread_lock = Lock()
        self.result_dict = defaultdict(int)
        self.total_count = 0


    def __request(self, row):
        data = {
            "id" : row[0],
            "businessNo" : row[4],
            "orderNo" : row[6]
        }

        sleep(0.001)  ### mocking routine
        with self.thread_lock:
            self.total_count += 1
        

    def main(self):
        print("#### {} job start".format(self.target_fpath), flush=True)

        with open(self.target_fpath, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            header = next(reader)

            with ThreadPoolExecutorWithQueueSizeLimit(max_workers=100) as executor:
                for row in reader:
                    executor.submit(self.__request, row)

        print("{} #### {} 결과 통계 : total_count - {} {}".format(ctime(), self.target_fpath, self.total_count, self.result_dict), flush=True)

def request_wrapped(target_fpath):
    '''
    executor.submit이 class.method 넘기면 동작하지 않아 최상위 함수로 wrapping
    '''
    requester = Requester(target_fpath)
    requester.main()

if __name__ == '__main__':
    print("{} #### job 시작 {} ~ {}".format(ctime(), start_date, end_date), flush=True)
    print("#### 대상 files {}".format(target_fpaths))

    with ProcessPoolExecutor(max_workers=3) as executor:
        for target_fpath in target_fpaths:
            executor.submit(request_wrapped, target_fpath)
    