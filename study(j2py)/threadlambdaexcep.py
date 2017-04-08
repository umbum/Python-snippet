import math
import sys
import usermod
import userexcept
import time
import webbrowser
import threading

print(math.pi)
print("\n===================================================\n\n")


falcon = usermod.FastBird()
falcon.fly()

def raiseExcept():
    raise userexcept.UserException("usererror")

try:
    raiseExcept()
except userexcept.UserException as e:
    print(e)


enum = tuple(enumerate(['name', 'cha', 'che']))
print(enum)
for i, name in enum:
    print(i, name)



def positive(x):
    if x>0:
        return 3
    else:
        return 0

print(list(map(positive, [1, 3, -2, 0, -5, 3,7, -5, 11])))


eval("print(list(filter(lambda x: x > 5, range(10))))")

class BumThread(threading.Thread):
    def __init__(self, msg):
        threading.Thread.__init__(self)
        self.msg=msg
        self.daemon = True
    def run(self):
        while True:
            time.sleep(1)
            print(self.msg)


def say(msg):
    for i in range(2):
        time.sleep(1)
        print(msg)

for msg in ['THREAD1', 'THREAD2', 'THREAD3']:
    t = threading.Thread(target=say, args=(msg, ))
    t.start()


t = UserThread(msg)
t.start()


