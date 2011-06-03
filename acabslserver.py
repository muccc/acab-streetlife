import acabsl
import socket
import thread
import time
import Queue

UDP_IP="0.0.0.0"
UDP_PORT=5005
q = Queue.Queue(100)

def writer():
    while 1:
        data = q.get()
        print list(data)
        try:
            x = ord(data[0])
            y = ord(data[1])
            r = ord(data[2])
            g = ord(data[3])
            b = ord(data[4])
            msh = ord(data[5])
            msl = ord(data[6])
            ms = (msh<<8) + msl;
            acabsl.send(x,y,r,g,b,ms/1000.)
        except:
            pass
        time.sleep(.001)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP,UDP_PORT))
thread.start_new_thread(writer,())

while True:
    data = sock.recv(1024)
    if not q.full():
        q.put(data)
    else:
        print 'ignoring data'

