import socket
import thread
import time
import Queue
import sys

UDP_IP="0.0.0.0"
UDP_PORT=5006
q = Queue.Queue(100)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP,UDP_PORT))

while True:
    data = sock.recv(1024)
    if not q.full():
        q.put(data)
    else:
        print 'ignoring data'

