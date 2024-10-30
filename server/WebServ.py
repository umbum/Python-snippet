#-*- coding: utf-8 -*-
#main thread에서는 명령어 같은거 처리해야 하니까 servsock도 thread로 처리
import os
import sys
import socket
import threading
import time

IP = "127.0.0.1"
PORT = 9798
ADDR = (IP, PORT)

class ThreadWebServ(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.sock.bind(ADDR)
        self.sock.listen(1)
        while True:
            try:
                clntsock, addr = self.sock.accept()    #blocking
                recvmsg = clntsock.recv(1024)
                clntsock.send(self.response(recvmsg))
                #clntsock.send("browser send data :\n".encode('utf-8')+recvmsg)
                clntsock.close()
            except socket.error as e:
                print(e)
                break

    def stop(self):
        self.sock.close()

    def response(self, recvmsg):#일단은 웹서버로...
        body = "Server's response : \nHello!, %s\n\n%s" % (time.ctime(), str(recvmsg))
        header = """HTTP/1.1 200 OK
Server: pythonHTTPServer
Content-type: text/plain
Content-Length: %d

""" % len(body)
        print(len(body), end="")
        print(recvmsg)
        return (header+body).encode('utf-8')



def _main():
    serv = ThreadWebServ()
    serv.daemon=True
    serv.start()

    print("""
        ThreadServ is running...
        input 'exit' or 'Ctrl+C' to terminate thread""")

    while True:
        try:
            if input() == "exit":
                break
        except KeyboardInterrupt:
            #serv.stop()
            #serv.join() #wait until thread terminate
            break

    print("the number of thread : "+str(threading.active_count()))

if __name__ == '__main__':
    _main()
    