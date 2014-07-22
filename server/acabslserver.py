#!/usr/bin/env python2
import acabsl_interface
import socket
import thread
import time
import Queue
import sys

config_file = sys.argv[1]
execfile(config_file)

q = Queue.Queue(100)
acabsl_interface.init(serials, interfaces, matrix)

def writer():
    while 1:
        data = q.get()
        #print list(data)
        try:
            x = ord(data[0])
            y = ord(data[1])
            cmd = data[2]
            r = ord(data[3])
            g = ord(data[4])
            b = ord(data[5])
            msh = ord(data[6])
            msl = ord(data[7])
            ms = (msh<<8) + msl;
            if cmd == 'C':
                acabsl_interface.send(x,y,r,g,b,ms/1000.)
            elif cmd == 'U':
                buffered = False
                if ord(data[0]): buffered = True
                acabsl_interface.sendUpdate(buffered)

        except Exception as e:
            print "Unexpected error:", e


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((server_ip,server_port))
thread.start_new_thread(writer,())

while True:
    data = sock.recv(1024)
    if not q.full():
        q.put(data)
    else:
        print 'ignoring data'

