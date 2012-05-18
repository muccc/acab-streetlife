import serialinterface
import time
import Queue
import threading
import thread

serials = [ 
    "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A400fvDr-if00-port0",
    "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A400fvDs-if00-port0",
    "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A400fvDu-if00-port0",
    "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A10044Xp-if00-port0",
    "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A400fvDt-if00-port0",
    "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A400fvDq-if00-port0",
    ]

#serials = [ 
#    "/dev/null",
#    "/dev/null",
#    "/dev/null",
#    "/dev/null",
#    "/dev/null",
#    "/dev/null",
#    ]

#              0   1     2     3     4     5     6     7     8     9     10    11    12    13    14    15
lamps =  [[0x17, 0x6E, 0x54, 0x31, 0x90, 0x25, 0x2B, 0x19, 0x37, 0x35, 0x68, 0x26, 0x70, 0x55, 0x1B, 0x24 ],
          [0x51, 0x6C, 0x32, 0x50, 0x39, 0x40, 0x3B, 0x52, 0x4F, 0x42, 0x6D, 0x57, 0x71, 0x28, 0x5A, 0x2E ],
          [0x5C, 0x2C, 0x5F, 0x47, 0x1F, 0x53, 0x2D, 0x27, 0x59, 0x64, 0x48, 0x3F, 0x15, 0x56, 0x20, 0x72 ],
          [0x43, 0x2A, 0x6F, 0x11, 0x14, 0x41, 0x3C, 0x4C, 0x45, 0x4D, 0x63, 0x62, 0x30, 0x22, 0x3A, 0x5B ],
          [0x23, 0x1E, 0x49, 0x4E, 0x4B, 0x12, 0x36, 0x69, 0x60, 0x6A, 0x3D, 0x6B, 0x44, 0x18, 0x46, 0x21 ],
          [0x58, 0x67, 0x4A, 0x16, 0x38, 0x2F, 0x66, 0x1A, 0x61, 0x33, 0x3E, 0x10, 0x29, 0x34, 0x13, 0x1C ]]

# 1D 5C 5D 5E 65 
interfaces = [0,1,2,3,4,5]
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
    bridge[1].write('\\F')
    thread.start_new_thread(interfaceHandler,bridge)

buffered = False

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

def sendSpeedFade(x,y,r,g,b,speed,interface):
    global buffered
    lamp = lamps[y][x]
    if buffered:
        cmd = "%ca%c%c%c%c%c"%(chr(lamp),chr(r),chr(g),chr(b),chr(high(speed)),chr(low(speed)))
    else:
        cmd = "%cF%c%c%c%c%c"%(chr(lamp),chr(r),chr(g),chr(b),chr(high(speed)),chr(low(speed)))

    write(cmd,interfaces[y]);

def sendUpdate(mode):
    global buffered
    buffered = mode
    if buffered:
        cmd = "%cU"%chr(0)
        for i in interfaces:
            write(cmd, interfaces[i])

fullmessage = [False for i in interfaces]

def write(msg, interface):
    msg = "\x5c\x30%s\x5c\x31"%(msg.replace("\\","\\\\"))
    msg = msg.replace("\\","\\\\")

    if not bridges[interface][0].full():
        if fullmessage[interface]:
            print 'reactivating bridge'
            fullmessage[interface] = False
        bridges[interface][0].put(msg)
    else:
        if fullmessage[interface] == False:
            print 'ignoring', msg, 'queue for bridge is full'
            fullmessage[interface] = True

