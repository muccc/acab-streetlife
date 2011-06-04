import serialinterface
import time

serials = [ "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A100473q-if00-port0",
            "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A100473s-if00-port0",
            "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A1004b6A-if00-port0" ]

lamps = [[0x48, 0x2F, 0x49, 0x2E, 0x2D, 0x43, 0x54, 0x4d],
         [0x22, 0x44, 0x38, 0x27, 0x1A, 0x51, 0x34, 0x21],
         [0x41, 0x45, 0x40, 0x37, 0x50, 0x3F, 0x3C, 0x39],
         [0x3E, 0x2C, 0x3D, 0x32, 0x2B, 0x30, 0x1f, 0x28],
         [0x52, 0x2A, 0x36, 0x42, 0x33, 0x3B, 0x4E, 0x20],
         [0x23, 0x35, 0x25, 0x1E, 0x26, 0x31, 0x24, 0x53]]

interfaces = [0,0,1,1,2,2]
interface_timeouts = [0,0,0]

def createSerial(dev):
    return serialinterface.SerialInterface(dev,115200,1)

serials = map(createSerial,serials)

def send(x,y,r,g,b,t):
    lamp = lamps[y][x]
    ms = int(t*1000)

    if ms == 0:
        sendSetColor(lamp,r,g,b,interfaces[y])
    else:
        sendMSFade(lamp,r,g,b,ms,interfaces[y])

def high(x):
    return (x>>8)&0xff;

def low(x):
    return x&0xff;

def sendSetColor(lamp,r,g,b,interface):
    cmd = "%cC%c%c%c"%(chr(lamp),chr(r),chr(g),chr(b))
    cmd = cmd.replace("\\","\\\\")
    write("\x5c\x30%s\x5c\x31"%cmd,interface);

def sendMSFade(lamp,r,g,b,ms,interface):
    cmd = "%cM%c%c%c%c%c"%(chr(lamp),chr(r),chr(g),chr(b),chr(high(ms)),chr(low(ms)))
    cmd = cmd.replace("\\","\\\\")
    write("\x5c\x30%s\x5c\x31"%cmd,interface);

def sendSpeedFade(x,y,r,g,b,speed,interface):
    lamp = lamps[y][x]
 
    cmd = "%cF%c%c%c%c%c"%(chr(lamp),chr(r),chr(g),chr(b),chr(high(speed)),chr(low(speed)))
    cmd = cmd.replace("\\","\\\\")
    write("\x5c\x30%s\x5c\x31"%cmd,interfaces[y]);


def write(msg, interface):
    timeout = interface_timeouts[interface]
    t = time.time()

    if timeout - t > 0:
        time.sleep(timeout - t)
    
    interface_timeouts[interface] = time.time() + 0.001
    serials[interface].write(msg)

