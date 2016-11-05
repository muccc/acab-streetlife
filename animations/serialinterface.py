import serial
import string
import sys
import time

class SerialInterface:
    def  __init__ ( self, path2device, baudrate, timeout=0):
      self.portopen = False
      self.dummy = False

      if path2device == '/dev/null':
            self.dummy = True
            self.portopen = True

      while not self.portopen:
        try:
            self.ser = serial.Serial(path2device, baudrate)
            self.path2device = path2device
            self.baudrate = baudrate
            self.timeout = timeout+1
            self.ser.flushInput()
            self.ser.flushOutput()
            if timeout:
                self.ser.setTimeout(timeout+1)
            self.portopen = True
            break
        except serial.SerialException:
            #print "Exception while opening", path2device
            pass
        time.sleep(1)
      print "Opened", path2device
    def close(self):
        try:
            self.portopen = False
            self.ser.close()
        except serial.SerialException:
            pass
    def reinit(self):
        self.close()
        #print "reopening"
        while not self.portopen:
            self.__init__(self.path2device, self.baudrate, self.timeout)
            time.sleep(1)
        #print "done"

    def writeMessage(self,message):
        enc = "\\1" + message.replace('\\','\\\\') + "\\2";
        #print 'writing %s' % list(enc)
        try:
            self.ser.write(enc)
        except :
            pass
            #self.reinit()


    def write(self,message):
        #print 'writing', list(message)
        if self.dummy:
            return
        try:
            self.ser.write(message)
        except :
            self.reinit()

    def readMessage(self):
        data = ""
        escaped = False
        stop = False
        start = False
        inframe = False

        while True:
            starttime = time.time()
            c = self.ser.read(1)
            endtime = time.time()
            if len(c) == 0:             #A timout occured
                if endtime-starttime < self.timeout - 1:
                    print "port broken"
                    self.reinit()
                    raise Exception()
                else:
                    #print 'TIMEOUT'
                    return False
            if escaped:
                if c == '1':
                    start = True
                    inframe = True
                elif c == '9':
                    stop = True
                    inframe = False
                elif c == '\\':
                    d = '\\'
                escaped = False
            elif c == '\\':
                escaped = 1
            else:
                d = c
                
            if start and inframe:
                start = False
            elif stop:
                if data[0] == 'D':
                    message = '%f %s'%(time.time(), data[2:])
                    print 'serial debug message:',data
                    #print message
                    data = ""
                    stop = False
                else:
                    #print 'received message: len=%d data=%s'%(len(data),data)
                    #print 'received message:',list(data)
                    return data
            elif escaped == False and inframe:
                data += str(d)

