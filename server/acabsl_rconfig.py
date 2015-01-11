# vim: set ts=4 sw=4 tw=0 et pm=:
import socket

# module to send packets to acabsl-rconfig-server.py

UDP_HOST="0.0.0.0"
UDP_PORT=5555
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def set_target(host,port):
    global UDP_HOST,UDP_PORT
    UDP_HOST=host
    UDP_PORT=port

def set_lamp((i,a),(r,g,b)):
    msg=[0x23,i,a,r,g,b]
    msg=[chr(x) for x in msg]
    sock.sendto(''.join(msg), (UDP_HOST, UDP_PORT))

def set_all((r,g,b)):
    msg=[0x42,r,g,b]
    msg=[chr(x) for x in msg]
    sock.sendto(''.join(msg), (UDP_HOST, UDP_PORT))

def send_config(config):
    msg=[0x5,len(config),len(config[0])]
    for line in config:
        for (i,a) in line:
            msg.append(a)
            msg.append(i)
    msg=[chr(x) for x in msg]
    sock.sendto(''.join(msg), (UDP_HOST, UDP_PORT))
