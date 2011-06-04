#!/usr/bin/python
## This is an example of a simple sound capture script.
##
## The script opens an ALSA pcm for sound capture. Set
## various attributes of the capture, and reads in a loop,
## Then prints the volume.
##
## To test it out, run it and shout at your microphone:

import alsaaudio, time, audioop
import random,time,lib_sl

# Open the device in nonblocking capture mode. The last argument could
# just as well have been zero for blocking mode. Then we could have
# left out the sleep call in the bottom of the loop
inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)

# Set attributes: Mono, 8000 Hz, 16 bit little endian samples
inp.setchannels(1)
inp.setrate(8000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

# The period size controls the internal number of frames per period.
# The significance of this parameter is documented in the ALSA api.
# For our purposes, it is suficcient to know that reads from the device
# will return this many frames. Each frame being 2 bytes long.
# This means that the reads below will return either 320 bytes of data
# or 0 bytes of data. The latter is possible because we are in nonblocking
# mode.
inp.setperiodsize(160)
t=0.001
count=0
dia=1
vavg = 0
vmin = 0
vmax = 0

while True:
    for i in range(0,8):
        l,data = inp.read()
        if l:
        	# Return the maximum of the absolute value of all samples in a fragment.
        	
		try:
			vavg= audioop.avg(data, 2)
        		vmin,vmax= audioop.minmax(data, 2)
		catch:
			pass

                val=min(200,vmax/40)
                val2=min(200,-1*(vmin/40))
                lib_sl.send(dia*(i+1)%8,5,val,i*20,0,t)
                lib_sl.send(dia*(i+2)%8,4,val,val,i*20,t)
                lib_sl.send(dia*(i+3)%8,3,val,val,val,t)
                lib_sl.send(dia*(i+4)%8,2,val2,0,i*20,t)
                lib_sl.send(dia*(i+5)%8,1,val2,val2,i*20,t)
                lib_sl.send(dia*(i+6)%8,0,val2,val2,val2,t)
                if count < 400:
                    count=count+1
                else:
                    count=0
                    dia=-1*dia
                    print "switch dia"
        time.sleep(t)
