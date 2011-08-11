import serialinterface
import time

serials = [ 
    "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A1004b6r-if00-port0",
    "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A9005npX-if00-port0",
    "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A100473q-if00-port0",
    "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A100473s-if00-port0",
    "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A1004b6A-if00-port0",
    "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A400fvDA-if00-port0",
    ]
#            0   1     2     3     4     5     6     7     8     9     10    11    12    13    14
lamps = [[0x74, 0x74, 0x47, 0x68, 0x6c, 0x12, 0x13, 0x14, 0x1b, 0x1a, 0x18, 0x11, 0x10, 0x19, 0x15],
         [0x2b, 0x29, 0x1e, 0x2a, 0x16, 0x1f, 0x17, 0x1c, 0x20, 0x23, 0x21, 0x22, 0x2c, 0x24, 0x2e],
         [0x35, 0x25, 0x36, 0x2d, 0x3f, 0x2f, 0x37, 0x26, 0x32, 0x34, 0x33, 0x3c, 0x6c, 0x28, 0x27],
         [0x44, 0x6c, 0x43, 0x40, 0x41, 0x42, 0x74, 0x49, 0x4a, 0x4b, 0x30, 0x3d, 0x45, 0x3b, 0x3e],
         [0x5b, 0x68, 0x46, 0x53, 0x55, 0x57, 0x54, 0x58, 0x5e, 0x4d, 0x48, 0x5c, 0x4f, 0x4e, 0x5f],
         [0x52, 0x50, 0x6b, 0x5a, 0x71, 0x6c, 0x6c, 0x6a, 0x72, 0x69, 0x63, 0x6c, 0x6c, 0x6f, 0x51]]

interfaces = [5,4,3,2,1,0]
interface_timeouts = [0,0,0,0,0,0]

def createSerial(dev):
    return serialinterface.SerialInterface(dev,115200,1)

serials = map(createSerial,serials)

def send(x,y,r,g,b,t):
    ms = int(t*1000)
    if x == 100 and y == 100:
      if ms == 0:
	sendSetColor(0,r,g,b,0)
	sendSetColor(0,r,g,b,1)
	sendSetColor(0,r,g,b,2)
      else:
        sendMSFade(0,r,g,b,ms,0)
        sendMSFade(0,r,g,b,ms,1)
        sendMSFade(0,r,g,b,ms,2)
      return
    if x == 100:
      if ms == 0:
	sendSetColor(0,r,g,b,y)
      else:
        sendMSFade(0,r,g,b,ms,y)
      return
             
    lamp = lamps[y][14-x]
    if lamp == ord('l'):
        return
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
    if lamp == ord('l'):
        return
    lamp = lamps[y][14-x]
 
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

