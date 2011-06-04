import subprocess
import playlist
import time
import os
import signal

pidfile='/tmp/animation_pids'

pl=playlist.playlist

def abort(signal,frame,pids):
  for pid in pids:
   os.kill(pid,signal.SIGKILL)

signal.signal(signal.SIGINT, abort)
signal.pause

while 1:
 for i in pl:
  t = i[0]
  processlist=[]
  pids=open(pidfile,"w")
  pids.close()
  for animation in i[1]:
    p=subprocess.Popen(["python", animation])
    processlist.append(p)
    print "[" + str(p.pid) + "] " + animation
    pids= open(pidfile,'a')
    pids.write(str(p.pid)+"\n")
    pids.close()
  time.sleep(t)
  for process in processlist:
    process.kill()
  print "next entry"
