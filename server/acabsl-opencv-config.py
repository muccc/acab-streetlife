#!/usr/bin/env python
# vim: set ts=4 sw=4 tw=0 et pm=:

# How to use me:
# - on acabsl server run "server/acabsl-rconfig-server.py -f new" (new = config output filename)
#   - check if it correctly detected the number of interfaces
# - locally run "server/acabsl-opencv-config.py"
#   - command line "-h acab2" for acabsl server name
#   - command line "-i 2,3" which interfaces to use on the server
#   - command line "-c 1" for second camera (if you have internal webcam)
#   - command line "--diff" for new "differential mode"
# - make sure whole wall is inside camera, and not too much around it
# - make sure wall is approximately aligned with picture borders
# - move the "pixel" slider slowly until any pixel is lit
# - fiddle with H+ and H- sliders so the pixel is well-recognized
# - move the "run" slider to 1
# - watch the script run. It will send the config to the server when done.
# - If the config looks good you are done.
# - kill acabsl-rconfig-server.py, and start "server/acabslserver.py server/config-new.py"

import time
import cv2
import numpy as np
import random
import sys
import getopt
from math import atan2, degrees
import acabsl_rconfig

options, remainder = getopt.getopt(sys.argv[1:], 'h:p:vc:i:rdx:g:', [
        'host=',
        'port=',
        'verbose',
        'cam=',
        'interfaces=',
        'run',
        'pixel=',
        'grid=',
        'diff'
        ])

path='/dev/serial/by-id'
UDP_IP="acab2.club.muc.ccc.de"
UDP_PORT=5555
verbose=0
autostart=0
cam_index=0 # Default camera is at index 0.
b_color=(0,255,0) # Background color
f_color=(0,0,255) # Foreground color
interfaces=[0,1,2]
min_addr=0x10 # According to schneider
max_addr=0x9f # According to schneider
def_pixel_if=1  # Which pixel to turn on when starting
def_pixel_addr=27 # Which pixel to turn on when starting
grid_x=20
grid_y=30
min_area=100 # Minimum size of lamp in picture
base_image=None
diffmode=0  # Differential mode

for opt, arg in options:
    if opt in ('-h', '--host'):
        UDP_IP=arg
    elif opt in ('-p', '--port'):
        UDP_PORT=int(arg)
    elif opt in ('-v', '--verbose'):
        verbose=1
    elif opt in ('-c', '--cam'):
        cam_index=int(arg)
    elif opt in ('-i', '--interfaces'):
        interfaces=[int(x) for x in arg.split(',')]
    elif opt in ('-r', '--run'):
        autostart=1
    elif opt in ('-d', '--diff'):
        diffmode=1
    elif opt in ('-x', '--pixel'):
        (def_pixel_if,def_pixel_addr)=[int(x) for x in arg.split(',')]
    elif opt in ('-g', '--grid'):
        (grid_x,grid_y)=[int(x) for x in arg.split(',')]

if diffmode==1:
    b_color=(0,0,0)
    f_color=(255,0,0)

# Global vars
pixels=None
grid=None
cap=None

def nothing(x):
    pass

# callback for pixel trackbar
def pixel(x):
    set_all(b_color)
    acabsl_rconfig.set_lamp((interfaces[cv2.getTrackbarPos('pixel_if','ctrl')],cv2.getTrackbarPos('pixel_addr','ctrl')),f_color)

# callback for pixel interface trackbar
def pixel_if(x):
    # 0 -> all lamps on currently selected interface
    pixel(0)

def set_all(color):
    global interfaces
    for i in interfaces:
        # 0 -> all lamps of interface i
        acabsl_rconfig.set_lamp((i, 0),color)

def run(x):
    global pixels
    global grid
    if x==1:
        acabsl_rconfig.set_all(b_color)
        grid=None
        pixels=None
        do_detect()
        print pixels
        grid=gridify(pixels)
        print grid
        send_config(grid)

def send_config(grid):
    # Generate config array
    config=[]
    for line in grid:
        cl=[]
        for point in line:
            cl.append(pixels[point][0])
        config.append(cl)
    print "config="
    for x in config:
        print "[",", ".join([addr(p) for p in x]),"]"
    acabsl_rconfig.send_config(config)

# Get coordinates of "pixel"
def pt(x):
    global pixels
    return (pixels[x][1])

# Get beautified address of pixel
def addr((i,a)):
    global pixels
    return "(0x%x, %d)"%(a,i)

# Find coordinates of the lamp
def find_pixel(show):
    global pixels,base_image
    ret, frame = cap.read()
    if ret!=True or frame is None:
        print "Image Aquisition error"
        cap.release()
        exit(1)

    img=cv2.GaussianBlur(frame, (5,5), 0)
    img=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    if diffmode==0:
        lower=np.array([cv2.getTrackbarPos('H-','ctrl'), cv2.getTrackbarPos('S-','ctrl'), cv2.getTrackbarPos('V-','ctrl') ],np.uint8)
        upper=np.array([cv2.getTrackbarPos('H+','ctrl'), cv2.getTrackbarPos('S+','ctrl'), cv2.getTrackbarPos('V+','ctrl') ],np.uint8)
    else:
        img=frame
        if base_image is None or cv2.waitKey(1)&0xff == 115: # 's'
            base_image=cv2.split(img)[0]
        img = abs((cv2.split(img)[0])/2+128-base_image/2)
        cv2.imshow('img',img)
        lower=np.array([cv2.getTrackbarPos('V-','ctrl')])
        upper=np.array([cv2.getTrackbarPos('V+','ctrl')])
    separated=cv2.inRange(img,lower,upper)
#    cv2.imshow('img',separated)

    contours,hierarchy=cv2.findContours(separated,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    max_area = min_area
    largest_contour = None
    for idx, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area=area
            largest_contour=contour
        if area > min_area and show:
            cv2.drawContours(frame,[contour],0,(0,0,255), 2)

    if not largest_contour is None:
        moment = cv2.moments(largest_contour)
        x=int(moment["m10"]/moment["m00"])
        y=int(moment["m01"]/moment["m00"])
        if show:
            cv2.circle(frame,(x,y),3,(0,255,255),-1)

    if show:
        if not pixels is None:
            for (px,pos) in pixels:
                cv2.circle(frame,pos,3,(255,0,0),-1)
                cv2.putText(frame,addr(px), (pos[0]+5,pos[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,0,0))
        if not grid is None:
            # Debugging output
            for x in xrange(len(grid)):
                for y in xrange(len(grid[x])):
                    try:
                        if y>0:
                            cv2.line(frame,pt(grid[x][y-1]),pt(grid[x][y]),(255,0,0))
                        if x>0:
                            cv2.line(frame,pt(grid[x-1][y]),pt(grid[x][y]),(255,0,0))
                    except IndexError:
                        pass
        cv2.imshow('frame',frame)
    if largest_contour is None:
        return (0,0)
    else:
        return (x,y)

# Go through all addresses, and find where they are
def do_detect():
    global pixels
    pixels=[]
    set_all(b_color)
    idx=0
    for i in interfaces:
        for a in xrange(min_addr,max_addr):
            px=(i,a)
            print "Testing: ",addr(px),
            acabsl_rconfig.set_lamp(px,f_color)
            time.sleep(.05)
            for x in range(3):
                ret, frame = cap.read()
            if ret != True:
                print "Image error"
                exit(1)
            pos=find_pixel(True)
            if pos!=(0,0):
                pixels.append([px,pos])
                print "@",pos
            else:
                print "<notfound>"
            acabsl_rconfig.set_lamp(px,b_color)
            if cv2.waitKey(1)&0xff == 27: # Escape key
                cv2.destroyAllWindows()
                cap.release()
                break

# calculates length and angle for the vector from p1 to p2
def dist((x1,y1),(x2,y2)):
    xD=x2-x1
    yD=y2-y1
    return (xD**2+yD**2,degrees(atan2(yD,xD)))

# Finds closest pixel to position p0 in pixel list pixels
def find_closest_pixel_pos(p0,pixels):
    mind=None
    minc=None
    for (ct,(idx,p1)) in enumerate(pixels):
        (d,a)=dist(p0,p1)
        if mind is None or d<mind:
            mind=d
            minc=ct
    return minc

# Finds closest pixel to spixel in pixels with
# angular constraint (between amin and amax) when seen from spixel
# spixel is index into pixels array
# amin, amax is in degrees (-180,180)
def find_closest_pixel(spixel,pixels,amin,amax):
    p0=pixels[spixel][1]
    mind=None
    minc=None
    for (ct,(idx,(x2,y2))) in enumerate(pixels):
        (d,a)=dist(p0,(x2,y2))
        if a>amin and a<amax and d>0:
            if mind is None or d<mind:
                mind=d
                minc=ct
    return minc

# Try to match points into an 2d array
def gridify(pixels):
    array=[]

    # Start with pixel closest to the origin
    cp=find_closest_pixel_pos((0,0),pixels)

    while cp is not None:
        row=[]
        while cp is not None: # Gather up pixels to the right
            row.append(cp)
            cp=find_closest_pixel(cp,pixels,-grid_x,grid_x)
        array.append(row)
        #print row

        # Next row starts with pixel below leftmost pixel of current row
        cp=find_closest_pixel(row[0],pixels,90-grid_y,90+grid_y)

    # We're done.
    height=len(array)
    width=len(array[0])
    print "Array size %d x %x"%(width,height)

    # Debugging output
    for line in array:
        for point in line:
            print "(%3d,%3d) "%(pt(point)),
        print

    # Do some consistency checks
    ccheck=[0]* len(pixels)

    for (y,line) in enumerate(array):
        if len(line)!=width:
            print "ERROR: line %d length is %d!"%(y,len(line))
        for point in line:
            ccheck[point]+=1

    for (ctr,cv) in enumerate(ccheck):
        if cv==0:
            print "ERROR: pixel %d %s remains unused"%(ctr,addr(pixels[ctr][0]))
        if cv>1:
            print "ERROR: pixel %d %s used %d times"%(ctr,addr(pixels[ctr][0]),cv)

    return array

class MockCamera(object):
    def read(self):
        return (True,np.zeros((900,1400,3), np.uint8))
    def release(self):
        pass

def main():
    global cap
    global pixels,grid
    
    # Init OpenCV
    if cam_index <0:
        cap=MockCamera()
    else:
        cap = cv2.VideoCapture(cam_index) # Video capture object
        cap.open(cam_index) # Enable the camera
        cap.set(cv2.cv.CV_CAP_PROP_EXPOSURE, 0)
        #cap.set(cv2.cv.CV_CAP_PROP_WHITE_BALANCE, 0) # not implemented yet
    
    # Init rconfig 
    acabsl_rconfig.set_target(UDP_IP,UDP_PORT)
    
    # Setup OpenCV GUI
    cv2.namedWindow('ctrl', cv2.WINDOW_NORMAL)
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    if diffmode ==0:
        cv2.resizeWindow('ctrl', 1000, 300)
        cv2.createTrackbar('H-','ctrl', 90,255,nothing)
        cv2.createTrackbar('H+','ctrl',140,255,nothing)
        cv2.createTrackbar('S-','ctrl', 20,255,nothing)
        cv2.createTrackbar('S+','ctrl',255,255,nothing)
        cv2.createTrackbar('V-','ctrl',100,255,nothing)
        cv2.createTrackbar('V+','ctrl',255,255,nothing)
    else:
        cv2.createTrackbar('V-','ctrl',210,255,nothing)
        cv2.createTrackbar('V+','ctrl',255,255,nothing)
    cv2.createTrackbar('pixel_if','ctrl',def_pixel_if,len(interfaces)-1,pixel_if)
    cv2.createTrackbar('pixel_addr','ctrl',def_pixel_addr,255,pixel)
    cv2.createTrackbar('run','ctrl',0,1,run)
    
    if pixels is not None:
        grid=gridify(pixels)
        send_config(grid)
    
    run(autostart)
    
    acabsl_rconfig.set_all(b_color)
    pixel(cv2.getTrackbarPos('pixel','ctrl'))
    
    while True:
        find_pixel(True)
        k = cv2.waitKey(20) & 0xFF
        if k == 27: # Escape key
            cv2.destroyAllWindows()
            cap.release()
            break

if __name__ == "__main__":
    main()

