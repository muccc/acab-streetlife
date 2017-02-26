#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import threading
import colorsys

from flask import Flask
from flask import request
app = Flask(__name__)

class RepeatingTimer(threading.Thread):
    def __init__(self, event, target):
        threading.Thread.__init__(self)
        self.stopped = event
        self.target = target

    def run(self):
        while not self.stopped.wait(1):
            self.target()


import animations.blackAllTheThings

t_kill = None
timer = None

state = {
  'all_black' : True,
  'decke' : True,
  'wall' : True,
  'all' : 0x000000
}

@app.route("/")
def hello():
    return "Hello World!"

# returns True when state in ON and False when state is OFF
def is_on(name):
    return state[name]


@app.route("/acab/", methods = ['GET'] )
def index():
  return json.dumps( { i: return_state(i) for i in state.keys() }, indent=2 )



@app.route("/acab/<string:name>", methods = ['GET'] )
def return_state(name):
  return 'ON' if is_on(name) else 'OFF'


def set_all_to_black():
  print('.')
  animations.blackAllTheThings.set_all_to_black()



@app.route("/acab/<string:name>", methods = ['DELETE'] )
def switch_off(name):
  global timer, t_kill

  if timer is None:
    t_kill = threading.Event()
    timer = RepeatingTimer(t_kill, timer_trigger)
    timer.start()
    state[name] = False

  return return_state(name)


def timer_trigger():
  if not state['all_black']:
    animations.blackAllTheThings.set_all_to_black()
  if not state['decke']:
    animations.blackAllTheThings.set_decke(0,0,0)
  if not state['wall']:
    animations.blackAllTheThings.set_wall(0,0,0)



@app.route("/acab/<string:name>", methods = ['POST'] )
def switch_on(name):
  state[name] = True
  if state['all_black'] and state['decke'] and state['wall']:
    stop_timer()
  
  return return_state(name)

current_color = None

def hsv_to_rgb(c):
  return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(c[0]/360, c[1]/100, c[2]/100))

def rgb_to_hsv(c):
  hsv = colorsys.rgb_to_hsv(c[0]/255., c[1]/255., c[2]/255.)
  return tuple([int(hsv[0]*360), int(hsv[1]*100), int(hsv[2]*100)])




@app.route("/color/<string:name>", methods = ['POST'] )
def change_color(name):
  color = request.args.get('color')
  print color

  global timer, t_kill, current_color
  current_color = hsv_to_rgb([float(x) for x in color.split(',')])

  stop_timer()

  if timer is None:
    t_kill = threading.Event()
    timer = RepeatingTimer(t_kill, set_color)
    timer.start()

  return color

def set_color():
  c = current_color
  animations.blackAllTheThings.set_all(c[0],c[1],c[2])


@app.route("/color/<string:name>", methods = ['GET'] )
def get_color(name):
  if current_color:
    return '%d,%d,%d' % rgb_to_hsv(current_color)
  else:
    return ''


@app.route("/playlist/<string:name>", methods = ['POST'] )
def stop_timer(name=None):
  global timer, t_kill
  if timer is not None:
    t_kill.set()
    timer = None
  return ''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


