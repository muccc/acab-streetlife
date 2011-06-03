import serialinterface
import time

serials = [ "/dev/ttyUSB0","/dev/ttyUSB0","/dev/ttyUSB0",
            "/dev/ttyUSB0","/dev/ttyUSB0","/dev/ttyUSB0" ]

lamps = [[0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08],
         [0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18],
         [0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28],
         [0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38],
         [0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48],
         [0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58]]

interfaces = [0,0,1,1,2,2]

def createSerial(dev):
    return serialinterface.SerialInterface(dev,115200,1)

serials = map(createSerial,serials)

def send(x,y,r,g,b,t):
    lamp = lamps[y][x]
    if t == 0:
        sendSetColor(lamp,r,g,b,serials[interfaces[y]])
    else:
        sendTimedFade(lamp,r,g,b,t)

def high(x):
    return (x>>8)&0xff;

def low(x):
    return x&0xff;

def sendSetColor(lamp,r,g,b,serial):
    cmd = "%cC%c%c%c"%(chr(lamp),chr(r),chr(g),chr(b))
    cmd = cmd.replace("\\","\\\\")
    serial.write("\x5c\x30%s\x5c\x31"%cmd);

def SendMSFade(lamp,r,g,b,ms,serial):
    cmd = "%cM%c%c%c%c%c"%(chr(lamp),chr(r),chr(g),chr(b),chr(high(ms)),chr(low(ms)))
    cmd = cmd.replace("\\","\\\\")
    serial.write("\x5c\x30%s\x5c\x31"%cmd);

