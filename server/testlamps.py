#!/usr/bin/env python
import acabsl_interface
import os
import sys
import time

# Script to test all lamps. Sends colors black->red->green->blue->white in a loop to all lamps (address 0).

try:
    serials1 = set(os.listdir('/dev/serial/by-id'))
except:
    serials1 = set()

serials1 = set()

input("Please attach the USB to RS485 bridges and press enter.: ")

serials2 = set(os.listdir('/dev/serial/by-id'))

serials = ['/dev/serial/by-id/'+serial for serial in serials2 - serials1]

if len(serials) == 0:
    print("Found no devices. Aborting.")
    sys.exit(1)

for serial in serials:
    print("Found device: ", serial)

interfaces = range(len(serials))

matrix = []

acabsl_interface.init(serials, interfaces, matrix)

def set_color(r, g, b, ms):
    for interface in interfaces:
        acabsl_interface.sendMSFade(0, r, g, b, ms, interface)

while True:
    set_color(0, 0, 0, 500)
    time.sleep(1)
    set_color(255, 0, 0, 500)
    time.sleep(1)
    set_color(0, 255, 0, 500)
    time.sleep(1)
    set_color(0, 0, 255, 500)
    time.sleep(1)
    set_color(255, 255, 255, 500)
    time.sleep(1)
