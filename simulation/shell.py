import sys
import os
import time
from socket import socket

# These args come from Server's subprocess.Popen()
address = sys.argv[1]
port = int(sys.argv[2])

s = socket()
s.connect((address, port))

while True:
    query = input("Send: ")
    if query == 'exit':
        os.system('taskkill /f /im python.exe')  # exit server + shell (does this work outside windows?)
    if query == 'run':
        try:
            while True:
                s.send(str.encode('01 0c'))
                rx = s.recv(512).decode('utf-8').split(' ')[:-1]
                values = [int(x, 16) for x in rx]
                time.sleep(10 / 1000)
                rpm = (values[2] * 256 + values[3]) / 4
                print("\r%d%%" % rpm)
        except KeyboardInterrupt:
            pass
    else:
        s.send(str.encode(query.upper()))
        print(s.recv(512).decode('utf-8'))