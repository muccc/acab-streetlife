#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import sys
#reload(sys)
#sys.setdefaultencoding('UTF8')


import json
import threading
import colorsys
import webcolors

from flask import Flask, request, jsonify, url_for
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

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/")
def site_map():
    links = []
    out = ""
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if True or "GET" in rule.methods and has_no_empty_params(rule):
            try:
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                links.append((url, rule.endpoint))
                out += '<li><a href="{0}">{1}</a> {2}</li>'.format(url, rule.endpoint, rule)
            #except BuildError:
            except:
                pass
    # links is now a list of url, endpoint tuples

    return "<ul>" + out + "</ul>"


@app.route("/routes/")
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("{:20s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    #for line in sorted(output):
    #    print line
    return "<pre>" + ("\n".join(output)) + "</pre>"

@app.route("/endpoints/")
def endpoints():
    endpoints = [rule.rule for rule in app.url_map.iter_rules()  if rule.endpoint !='static']
    return jsonify(dict(api_endpoints=endpoints))


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

  if name == 'all_black':
      state['decke'] = False
      state['wall'] = False
  elif not state['decke'] and not state['wall']:
      state['all_black'] = False

  return return_state(name)


def timer_trigger():
  if not state['all_black']:
    animations.blackAllTheThings.set_all_to_black()
  else:
    if not state['decke']:
      animations.blackAllTheThings.set_decke(0,0,0)
    if not state['wall']:
      animations.blackAllTheThings.set_wall(0,0,0)



@app.route("/acab/<string:name>", methods = ['POST'] )
def switch_on(name):
  state[name] = True
  if state['all_black'] and state['decke'] and state['wall']:
    stop_timer()

  if name == 'all_black':
      state['decke'] = True
      state['wall'] = True
  elif state['decke'] and state['wall']:
      state['all_black'] = True


  return return_state(name)

current_color = None

def hsv_to_rgb(c):
  return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(c[0]/360, c[1]/100, c[2]/100))

def rgb_to_hsv(c):
  hsv = colorsys.rgb_to_hsv(c[0]/255., c[1]/255., c[2]/255.)
  return tuple([int(hsv[0]*360), int(hsv[1]*100), int(hsv[2]*100)])

# POST /color/all?color=100,60,100     #for backwards compability
# POST /color/all?color=yellow
# POST /color/all?hsv=100,60,100
# POST /color/all?rbg=ffffff
@app.route("/color/<string:name>", methods = ['POST'] )
def change_color(name):
  color = request.args.get('color') or request.args.get('hsv')

  global timer, t_kill, current_color
  if color:
    try:
        # hsv color value e.g. "100,50,100"
        current_color = hsv_to_rgb([float(x) for x in color.split(',')])
    except ValueError:
        # color names e.g. "yellow"
        current_color = webcolors.html5_parse_legacy_color(color)
  else:
    color = request.args.get('rgb')
    # rbg color value e.g. "ff00dd"
    current_color = webcolors.html5_parse_simple_color(u"#" + color)

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


