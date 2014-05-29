#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Image
from acabsl import send
from acabsl import update
import colorsys
import random
import time
import sys, os, glob

# more is faster
rotation_speed = 1.5
rounds_per_image = 3
directory = '.'

wall_count=2
rows=6
cols=8

def blank_walls():
  for col in range(cols):
    for row in range(rows):
      for wall in range(wall_count):
        send(col,row,0,0,0,0,wall);
  update()

def render_frame(wall, image_data, angle):
  ptr = 0
  for y in range(rows):
    for x in range(cols):
      x += angle
      x = x % cols
      if type(image_data[ptr]) == int:
        send(x,y,image_data[ptr],image_data[ptr],image_data[ptr],0,wall);
      else:
        send(x,y,image_data[ptr][0],image_data[ptr][1],image_data[ptr][2],0,wall);
      ptr += 1
  update()

def display_image(img):
  # initialize the wall
  blank_walls()
  
  for repeats in range(rounds_per_image):
    image_raw_data = img.resize((cols,rows)).getdata()
    for angle in range(cols):
      render_frame(0, image_raw_data, angle)
      render_frame(1, image_raw_data, angle)
      time.sleep(1/rotation_speed)

# let's find all images in the image directory and then
# shuffle the list to choose one randomly
image_list = []
for ext in ('jpg', 'jpeg', 'bmp', 'png', 'gif'):
  search_str = os.path.join(directory,'*.{0}'.format(ext))
  image_list.extend(glob.glob(search_str))
random.shuffle(image_list)

im = Image.open(image_list[0])
display_image(im)

  
