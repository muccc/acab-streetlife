import serialinterface
import time

serials = [ "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A100473q-if00-port0",
            "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A100473s-if00-port0",
            "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A1004b6A-if00-port0" ]

lamps = [[0x27, 0x54, 0x49, 0x04, 0x05, 0x06, 0x07, 0x08],
         [0x1A, 0x28, 0x48, 0x14, 0x15, 0x16, 0x17, 0x18],
         [0x1A, 0x28, 0x48, 0x14, 0x15, 0x16, 0x17, 0x18],
         [0x00, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38],
         [0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48],
         [0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58]]

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

def write(msg, interface):
    timeout = interface_timeouts[interface]
    t = time.time()

    if timeout - t > 0:
        time.sleep(timeout - t)
    
    interface_timeouts[interface] = time.time() + 0.001
    serials[interface].write(msg)

