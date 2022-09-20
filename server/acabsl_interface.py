import serialinterface
import time
from queue import Queue
import threading

updatelock = threading.RLock()
updatequeues = []
updatecounter = 0

def interfaceHandler(queue, serial, updatequeue):
    global updatecounter
    while 1:
        msg = queue.get();
        if msg[4] == 'U':
            with updatelock:
                updatecounter += 1
                if updatecounter == len(interfaces):
                    updatecounter = 0
                    [q.put(0) for q in updatequeues]
            updatequeue.get()
        serial.write(msg)
        time.sleep(0.001)

def createBridge(dev):
    serial = serialinterface.SerialInterface(dev, 115200, 1)
    queue = Queue(255)
    updatequeue = Queue(1)
    updatequeues.append(updatequeue)
    return (queue, serial, updatequeue)

def init(s, i, m):
    global bridges, buffered, matrix, interfaces, serials, fullmessage
    serials = s
    interfaces = i
    matrix = m

    bridges = list(map(createBridge,serials))
    for bridge in bridges:
        bridge[1].write(b'\\F')
        # Put all lamps into the pause state
        msg = b'\x00S\x01'
        msg = b"\\\\0" + msg.replace(b"\\",b"\\\\\\\\") + b"\\\\1"
        bridge[1].write(msg)
        t = threading.Thread(target=interfaceHandler,args=bridge)
        t.daemon = True
        t.start()

    buffered = False
    
    fullmessage = [False for i in interfaces]

def send(x,y,r,g,b,t):
    ms = int(t*1000)
    if x == 100 and y == 100:
        if ms == 0:
            for i in interfaces:
                sendSetColor(0,r,g,b,i)
        else:
            for i in interfaces:
                sendMSFade(0,r,g,b,ms,i)
        return
    if x == 100:
        if ms == 0:
            sendSetColor(0,r,g,b,y)
        else:
            sendMSFade(0,r,g,b,ms,y)
        return

    lamp = matrix[y][x]

    if (lamp is not None) and (lamp != (None, None)):
        if ms == 0:
            sendSetColor(lamp[0],r,g,b,lamp[1])
        else:
            sendMSFade(lamp[0],r,g,b,ms,lamp[1])

def high(x):
    return (x>>8)&0xff;

def low(x):
    return x&0xff;

def sendSetColor(lamp,r,g,b,interface):
    global buffered
    if buffered:
        cmd = bytes([lamp,ord("P"),r,g,b])
    else:
        cmd = bytes([lamp,ord("C"),r,g,b])
    write(cmd,interface);

def sendMSFade(lamp,r,g,b,ms,interface):
    global buffered
    if buffered:
        cmd = bytes([lamp,ord("c"),r,g,b,high(ms),low(ms)])
    else:
        cmd = bytes([lamp,ord("M"),r,g,b,high(ms),low(ms)])
    write(cmd,interface);

def sendUpdate(mode):
    global buffered
    if mode and not buffered:
        buffered = True
        for i in interfaces:
            sendMSFade(0,0,0,0,1500,interfaces[i])
    buffered = mode
    if buffered:
        cmd = bytes([0,ord("U")])
        for i in interfaces:
            write(cmd, interfaces[i])


def write(msg, interface):
    msg = b"\\\\0" + msg.replace(b"\\",b"\\\\\\\\") + b"\\\\1"

    if not bridges[interface][0].full():
        if fullmessage[interface]:
            print('reactivating bridge')
            fullmessage[interface] = False
            bridges[interface][1].write(b'\\F')
        bridges[interface][0].put(msg)
    else:
        if fullmessage[interface] == False:
            print('ignoring', msg, 'queue for bridge is full')
            fullmessage[interface] = True

