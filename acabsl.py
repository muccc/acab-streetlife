import serialinterface
import time
import Queue
import threading
import thread

serials = [ 
    "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A400fvDr-if00-port0",
    "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A400fvDu-if00-port0",
    "/dev/null",
    "/dev/null",
    "/dev/null",
    "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A400fvDt-if00-port0",
    ]
#            0   1     2     3     4     5     6     7     8     9     10    11    12    13    14    15
lamps = [[0x74, 0x74, 0x47, 0x68, 0x6c, 0x12, 0x13, 0x14, 0x1b, 0x1a, 0x18, 0x11, 0x10, 0x19, 0x15, 0xFF ],
         [0x2b, 0x29, 0x1e, 0x2a, 0x16, 0x1f, 0x17, 0x1c, 0x20, 0x23, 0x21, 0x22, 0x2c, 0x24, 0x2e, 0xFF ],
         [0x35, 0x25, 0x36, 0x2d, 0x3f, 0x2f, 0x37, 0x26, 0x32, 0x34, 0x33, 0x3c, 0x6c, 0x28, 0x27, 0xFF ],
         [0x44, 0x6c, 0x43, 0x40, 0x41, 0x42, 0x74, 0x49, 0x4a, 0x4b, 0x30, 0x3d, 0x45, 0x3b, 0x3e, 0xFF ],
         [0x5b, 0x68, 0x46, 0x53, 0x55, 0x57, 0x54, 0x58, 0x5e, 0x4d, 0x48, 0x5c, 0x4f, 0x4e, 0x5f, 0xFF ],
         [0x52, 0x50, 0x6b, 0x5a, 0x71, 0x6c, 0x6c, 0x6a, 0x72, 0x69, 0x63, 0x6c, 0x6c, 0x6f, 0x51, 0xFF ]]

interfaces = [5,4,3,2,1,0]
#interfaces = [2,1,0]
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
    queue = Queue.Queue(100)
    updatequeue = Queue.Queue(1)
    updatequeues.append(updatequeue)
    return (queue, serial, updatequeue)

bridges = map(createBridge,serials)
for bridge in bridges:
    thread.start_new_thread(interfaceHandler,bridge)

buffered = True

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

    lamp = lamps[y][x]

    if ms == 0:
        sendSetColor(lamp,r,g,b,interfaces[y])
    else:
        sendMSFade(lamp,r,g,b,ms,interfaces[y])

def high(x):
    return (x>>8)&0xff;

def low(x):
    return x&0xff;

def sendSetColor(lamp,r,g,b,interface):
    if buffered:
        cmd = "%ca%c%c%c"%(chr(lamp),chr(r),chr(g),chr(b))
    else:
        cmd = "%cC%c%c%c"%(chr(lamp),chr(r),chr(g),chr(b))
    write(cmd,interface);

def sendMSFade(lamp,r,g,b,ms,interface):
    if buffered:
        cmd = "%cc%c%c%c%c%c"%(chr(lamp),chr(r),chr(g),chr(b),chr(high(ms)),chr(low(ms)))
    else:
        cmd = "%cM%c%c%c%c%c"%(chr(lamp),chr(r),chr(g),chr(b),chr(high(ms)),chr(low(ms)))
    write(cmd,interface);

def sendSpeedFade(x,y,r,g,b,speed,interface):
    lamp = lamps[y][x]
    cmd = "%cF%c%c%c%c%c"%(chr(lamp),chr(r),chr(g),chr(b),chr(high(speed)),chr(low(speed)))
    write(cmd,interfaces[y]);

def sendUpdate():
    cmd = "%cU"%chr(0)
    for i in interfaces:
        write(cmd, interfaces[i])
 
def write(msg, interface):
    msg = "\x5c\x30%s\x5c\x31"%msg
    msg = msg.replace("\\","\\\\")

    if not bridges[interface][0].full():
        bridges[interface][0].put(msg)
    else:
        print 'ignoring', msg, 'queue for bridge is full'

