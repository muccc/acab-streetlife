#!/usr/bin/env python
import acabsl_interface
import sys
import time
import os
import socket
import getopt

options, remainder = getopt.getopt(sys.argv[1:], 'l:p:vf:', [
        'listen=',
        'port=',
        'verbose',
        'filename',
        'path=',
        ])

path='/dev/serial/by-id'
UDP_IP="0.0.0.0"
UDP_PORT=5555
filename="config-unknown.py"
verbose=0

for opt, arg in options:
    if opt in ('-l', '--listen'):
        UDP_IP=arg
    elif opt in ('-p', '--port'):
        UDP_PORT=int(arg)
    elif opt in ('-f', '--filename'):
        filename="config-"+arg+".py"
    elif opt in ('-v', '--verbose'):
        verbose=1
    elif opt in ('--path'):
        path=arg

serials = os.listdir(path)

if len(serials) == 0:
    print "Found no devices. Aborting."
    sys.exit(1)

print "Found %d serials."%len(serials)

serials = [path+'/'+serial for serial in serials]
interfaces = range(len(serials))

matrix = []
acabsl_interface.init(serials, interfaces, matrix)

def set_lamp((interface,address), r, g, b):
    acabsl_interface.sendSetColor(address, r, g, b, interface)
    if verbose:
        print "(%d,%d)->(%d,%d,%d)"%(interface,address,r,g,b)

def set_all_lamps(r,g,b):
    global interfaces
    if verbose:
        print "(all)->(%d,%d,%d)"%(r,g,b)
    for interface in interfaces:
        acabsl_interface.sendSetColor(0, r, g, b, interface)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP,UDP_PORT))

print "Listening on %s:%d..."%(UDP_IP,UDP_PORT)

def receive():
    try:
        data = sock.recv(1024)
        data = [ord(x) for x in data]
        if verbose:
            print data
        if data[0]==0x42:
            set_all_lamps(data[1],data[2],data[3])
        elif data[0]==0x23:
            set_lamp((data[1],data[2]),data[3],data[4],data[5])
        elif data[0]==0x05:
            xl=data[1]
            yl=data[2]
            data=data[3:]
            matrix=[]
            for x in xrange(xl):
                line=[]
                for y in xrange(yl):
                    line.append("(0x%2x,%d)"%(data[0],data[1]))
                    data=data[2:]
                matrix.append(line)
            write_config(matrix)
        else:
            print "Unknown packet received: %d"%(data[0])
    except IndexError:
        print "Broken Packet received"

def write_config(matrix):
    config_file = open(filename, 'w')
    
    config_file.write("server_ip = '0.0.0.0'\n")
    config_file.write("server_port = 5000\n")
    config_file.write("serials = %s\n"%str(serials))
    config_file.write("interfaces = %s\n"%str(interfaces))

    config_file.write("matrix = [\n")
    for line in matrix:
        config_file.write("          [" + ", ".join(line) + "],\n")
    config_file.write("]\n")

    config_file.write("simulation = False\n")
    config_file.write("router_base_port = 8000\n")
    config_file.write("""
walls = [
  { 'host': 'localhost', 'port': server_port,
    'simhost': '0.0.0.0', 'simport': server_port,
    'startx': 0, 'starty': 0},
]
""")
    config_file.close()
    print "Config written to %s"%filename

while True:
    receive()

