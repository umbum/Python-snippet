import sys


if len(sys.argv) != 2:
    print("usage : textedit.py filename")
    sys.exit()

try:
    f = open(sys.argv[1], 'r')
    print(f.read())
    f.close()
except IOError:
    pass
finally:
    f = open(sys.argv[1], 'a')

while True:
    getdata=raw_input()
    if getdata == 'exit':
        break
    else:
        f.write(str(getdata))

f.close()

'''
option = sys.argv[1]
if option == '-a':
    f = open('memo.txt', 'a')
    f.write(sys.argv[2])
    f.close()

elif option == '-v':
    f = open('memo.txt', 'r')
    print(f.read())
    f.close()
'''