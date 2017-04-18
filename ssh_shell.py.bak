#coding: utf-8
from time import sleep
from collections import OrderedDict

import paramiko

'''
자동으로 세션을 여는 등의 복잡한 작업이 아니라
세션에서 특정 커맨드를 실행하는 간단한 작업은 secureCRT 등의 script로 
처리하는게 더 나을 수 있다.

su 같이 추가적인 입력을 받을 필요 없는 단일 명령어 조합은 exec_command로 처리하는 편이 더 나을 수 있다.
여기서는 su를 사용해야 해서 invoke_shell로 shell channel을 열었다.

command를 보내고 서버에서 response가 생성될 때 까지 기다리려고 했는데, (recv_ready())
send로 command를 전송하는 시간 보다 서버에서 처리하는 시간이 더 느려서 recv로 데이터를 받게 되면 보낸 command만 찍혀 돌아오는 reponse가 한번, command에 대한 응답으로 또 한 번, 총 두 번 찍혀 돌아올 수 있다.
e.g ) su
      suPW
      ls
한 번에 돌아올지, 두 번에 돌아올지는 서버 응답성에 달린거라 이런 식으로는 처리 불가능. sleep을 사용해야 함.
'''

systemList = OrderedDict()
systemList['test'] = {
    'user' : "user",
    'pw' : "passwd",
    'suPW' : "supasswd",
    'IP' : "127.0.0.1",
    'port' : 22
}

def __main():
    for sname, sattr in systemList.items():
        checker = System_checker(sattr['user'], sattr['pw'], sattr['suPW'], sattr['IP'], sattr['port'])
        print sname,
        checker.check()

class System_checker:
    def __init__(self, user, pw, suPW, IP, port):
        self.user = user
        self.pw = pw
        self.suPW = suPW
        self.IP = IP
        self.port = port
        self.session = None
        self.channel = None
    
    def open_session(self):
        self.session = paramiko.SSHClient()
        self.session.load_system_host_keys()
        self.session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.session.connect(self.IP, port=self.port, username=self.user, passwd=self.pw)
        self.channel = self.session.invoke_shell()
        sleep(0.3)

    def do_task(self):
        self.channel.send("su\n")
        sleep(0.1)

        self.channel.send(self.suPW+"\n")
        sleep(0.1)

        self.channel.send("id;ls -l\n")
        sleep(0.1)

        output = ''
        while self.channel.recv_ready():
            output += self.channel.recv(1024)
        
        print output

    def close_session(self):
        self.session.close()

    def check(self):
        try:
            self.open_session()
            self.do_task()
        except Exception as e:
            print "* Error occurred during check() "+self.IP+". Manual check is needed"
            print e
        finally:
            self.close_session()


if __name__ == "__main__":
    __main()        
