#!/usr/bin/env python2
import acabsl_interface
import socket
import threading
import time
from queue import Queue
import sys

config_file = sys.argv[1]
with open(config_file) as f:
    exec(f.read())

q = Queue(100)
acabsl_interface.init(serials, interfaces, matrix)

def writer():
    while 1:
        data = q.get()
        #print list(data)
        try:
            cmd = data[2]
            if cmd == ord('C'):
                x = data[0]
                y = data[1]
                r = data[3]
                g = data[4]
                b = data[5]
                msh = data[6]
                msl = data[7]
                ms = (msh<<8) + msl
                acabsl_interface.send(x,y,r,g,b,ms/1000.)
            elif cmd == ord('U'):
                buffered = False
                if data[0]: buffered = True
                acabsl_interface.sendUpdate(buffered)

        except Exception as e:
            print("Unexpected error:", e)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((server_ip,server_port))
t = threading.Thread(target=writer)
t.daemon = True
t.start()

while True:
    data = sock.recv(1024)
    if not q.full():
        q.put(data)
    else:
        print('ignoring data')

