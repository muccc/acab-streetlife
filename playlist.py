import dircache
import random


def ddc_chooser():
 alle = dircache.listdir('.')
 ddc_list = []
 for i in alle:
  if i[0:3] == 'ddc':
   ddc_list.append(i)
 return random.choice(ddc_list)

playlist = [
	    [20, ["rainbowwall.py", "randomfade.py"]],
            [30, ["s-rainbowscroll.py"]] ,
            [10, ["crazy.py"]] ,
            [10, ["kiu-arrows.py"]],
            [10, ["lines.py", "lines.py"]],
            [15, ["kiu-diebar-rwb.py"]],
	    [15, [ddc_chooser()]],
	    [15, ["dots.py"]],
	    [30, ["mc3_pixelpushers.py"]],
#	    [120, ["randomfade2.py"]],
	    [30, ["rainbowwall2.py"]],
            [40, ["kiu-font-acab.py"]],
	    [15, [ddc_chooser()]],
            [40, ["kiu-infinity.py"]],
            [60, ["kiu-random_pixels.py"]],
            [15, ["kiu-soft-scroll.py"]],
            [15, ["kiu-diebar-rw.py"]],
            [30, ["kiu-wabern.py"]],
            [10, [ddc_chooser()]],

            #[time_in_seconds, [simultaniois_animation1, simultanious_animation2, ....]]
]
