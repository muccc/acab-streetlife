import serialinterface
import time
import Queue
import threading
import thread

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
    serial = serialinterface.SerialInterface(dev,115200,1)
    queue = Queue.Queue(130)
    updatequeue = Queue.Queue(1)
    updatequeues.append(updatequeue)
    return (queue, serial, updatequeue)

def init(s, i, m):
    global bridges, buffered, matrix, interfaces, serials, fullmessage
    serials = s
    interfaces = i
    matrix = m

    bridges = map(createBridge,serials)
    for bridge in bridges:
        bridge[1].write('\\F')
        # Put all lamps into the pause state
        msg = '\x00S\x01'
        msg = "\x5c\x30%s\x5c\x31"%(msg.replace("\\","\\\\"))
        msg = msg.replace("\\","\\\\")
        bridge[1].write(msg)
        thread.start_new_thread(interfaceHandler,bridge)

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
        cmd = "%cP%c%c%c"%(chr(lamp),chr(r),chr(g),chr(b))
    else:
        cmd = "%cC%c%c%c"%(chr(lamp),chr(r),chr(g),chr(b))
    write(cmd,interface);

def sendMSFade(lamp,r,g,b,ms,interface):
    global buffered
    if buffered:
        cmd = "%cc%c%c%c%c%c"%(chr(lamp),chr(r),chr(g),chr(b),chr(high(ms)),chr(low(ms)))
    else:
        cmd = "%cM%c%c%c%c%c"%(chr(lamp),chr(r),chr(g),chr(b),chr(high(ms)),chr(low(ms)))
    write(cmd,interface);

def sendUpdate(mode):
    global buffered
    if mode and not buffered:
        buffered = True
        for i in interfaces:
            sendMSFade(0,0,0,0,1500,interfaces[i])
    buffered = mode
    if buffered:
        cmd = "%cU"%chr(0)
        for i in interfaces:
            write(cmd, interfaces[i])


def write(msg, interface):
    msg = "\x5c\x30%s\x5c\x31"%(msg.replace("\\","\\\\"))
    msg = msg.replace("\\","\\\\")

    if not bridges[interface][0].full():
        if fullmessage[interface]:
            print 'reactivating bridge'
            fullmessage[interface] = False
            bridges[interface][1].write('\\F')
        bridges[interface][0].put(msg)
    else:
        if fullmessage[interface] == False:
            print 'ignoring', msg, 'queue for bridge is full'
            fullmessage[interface] = True

