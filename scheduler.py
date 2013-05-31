import subprocess
import playlist
import time
import os
import signal
import random

pidfile='/tmp/animation_pids'


def abort(signal,frame,pids):
  for pid in pids:
   os.kill(pid,signal.SIGKILL)

signal.signal(signal.SIGINT, abort)
signal.pause

while 1:
  pl=playlist.getPlaylist()
  i =  random.choice(pl)
  t = i[0]
  processlist=[]
  pids=open(pidfile,"w")
  pids.close()
  for animation in i[1]:
    p=subprocess.Popen(animation)
    processlist.append(p)
    print "[" + str(p.pid) + "] " + str(animation)
    pids= open(pidfile,'a')
    pids.write(str(p.pid)+"\n")
    pids.close()
  time.sleep(t)
  for process in processlist:
    process.kill()
  print "next entry"
  reload(playlist)
