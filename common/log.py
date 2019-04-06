"""
Usage
-----
import common
common.logger.debug("string")
"""
import os, sys
import logging
import logging.handlers

__all__ = ["logger"]

formatter = logging.Formatter("%(asctime)s[%(levelname)s|%(filename)s:%(lineno)s]: %(message)s")

def addFileHandler():
    """ RotatingFileHander는 지정된 파일 크기에 도달할 때 까지 foo.log에 이어서 쓰다가
    크기가 초과하면 foo.log.1 -> foo.log.2로 밀어내고 foo.log -> foo.log.1로 만든 다음
    다시 foo.log에 쓴다. 즉, 항상 foo.log에 쓰기 때문에 이게 최신 로그이고 숫자가 클 수록 오래된 로그다.
    """
    file_max_byte = 100 * 1024 * 1024
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    log_file_path = BASE_PATH + "\\out\\log.txt"
    file_handler  = logging.handlers.RotatingFileHandler(log_file_path, maxBytes=file_max_byte, backupCount=10)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def addConsoleHandler():
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def addSockHandler(ADDR):
    HOST, PORT = ADDR
    socket_handler = logging.handlers.SocketHandler(HOST, PORT)
    print("[*] try to connect control&log socket to {}:{} .....".format(HOST, PORT))
    socket_handler.retryMax = 3.0    # exponential back-off retry 대기 최대 시간
    socket_handler.createSocket()
    while socket_handler.sock is None:
        pass
    # try:
    #     socket_handler.sock = socket_handler.makeSocket(10)
    # except ConnectionRefusedError as e:
    #     print("[*] Perhaps the RAPT server socket is not listening.")
    #     print(e)
    #     sys.exit(0)
    logger.addHandler(socket_handler)
    print("[*] socket handler added.")
    return socket_handler.sock


"""
Multiple calls to logging.getLogger('someLogger') return a reference to the same logger object. multi-process에서도 성립.
테스트해보니 전역 스코프의 코드는 import 될 때 마다 매번 실행되는게 아니라 최초 import 시 한 번만 실행된다. 
그래서 전역 스코프에서 막 초기화해도 상관 없는 듯.
"""
logger = logging.getLogger("rapt")
if True:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
""" handler.setLevel()로 따로 지정해 주더라도, 
logger의 level보다 높은 log만 출력되기 때문에 먼저 logger의 level을 내려주어야 한다. 
"""

# set custom log level (used only in agent.py:AutoRunThread)
logging.addLevelName(21, "SUCCESS")
logging.addLevelName(31, "FAIL")

addFileHandler()
addConsoleHandler()

if __name__ == "__main__":
    logger.log(11, "asdf")
    try:
        raise ValueError("error test")
    except Exception as e:
        logger.debug("test debug", exc_info=e)



"""    2018-11-09 18:01:13,408[INFO|clnt_test.py:57]: TEST LOG
< 위 로그를 서버로 보냈을 때, 서버가 수신하는 pickle 객체의 멤버 목록. SocketHandler는 pickle 객체로 딱 이 멤버만 보내기 때문에 Formatter를 설정하는건 의미 없음. > 
args: null
asctime: "2018-11-09 17:59:23,729"
created: 1541753963.7292228
exc_info: null
exc_text: null
filename: "clnt_test.py"
funcName: "main"
levelname: "INFO"
levelno: 20
lineno: 57
module: "clnt_test"
msecs: 729.2227745056152
msg: "TEST LOG"
name: "__main__"
pathname: "clnt_test.py"
process: 19900
processName: "MainProcess"
relativeCreated: 10049.57127571106
stack_info: null
thread: 22748
threadName: "MainThread"

# logger.debug("TEST DEBUG")
# logger.info("TEST INFO")
# logger.warning("TEST WARNING")
# logger.error("TEST ERROR")
# logger.critical("TEST CRITICAL")
"""
