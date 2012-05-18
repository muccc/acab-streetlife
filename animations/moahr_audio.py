#!/usr/bin/python
import alsaaudio, time, audioop
import random,time,lib_sl

inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NORMAL)

inp.setchannels(1)
inp.setrate(44100)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

inp.setperiodsize(320)
t=0.001
count=0
dia=1
vavg = 0
vmin = 0
vmax = 0

colors=(random.randint(0,1),random.randint(0,1),random.randint(0,1))
while True:
    for i in range(0,16):
        l,data = inp.read()
        if l:
		vavg=audioop.avg(data, 2)
       		vmin,vmax= audioop.minmax(data, 2)

                vmax+=63
                vavg*=-1
                vmin*=-1
                print vmin, vavg, vmax, count
                lib_sl.send(i%8,0+(0 if i>7 else 3),colors[0]*vmax,colors[1]*vmax,colors[2]*vmax,t)
                lib_sl.send(i%8,1+(0 if i>7 else 3),colors[0]*vavg,colors[1]*vavg,colors[2]*vavg,t)
                lib_sl.send(i%8,2+(0 if i>7 else 3),colors[0]*vmin,colors[1]*vmin,colors[2]*vmin,t)
                if count < 50000:
                    count+=vmax
                else:
                    if vmax > 25:
                        count=0
                        dia=-1*dia
                        while True:
                            colors=(random.randint(0,1),random.randint(0,1),random.randint(0,1))
                            if (colors[0]+colors[1]+colors[2]):
                                break
