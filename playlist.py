import dircache
import random


def ddc_chooser():
 alle = dircache.listdir('animations/ddc')
 ddc_list = []
 for i in alle:
  if i[0:3] == 'ddc' and i[-1] == 'y':
   ddc_list.append('ddc/'+i)
 return random.choice(ddc_list)

def getPlaylist():
    playlist = [
            #[time_in_seconds, [[simultanious_animation1, argument1, ...], [simultanious_animation2, argument1, ...], ...]]
            #[20, [["python","animations/screw.py","--wall=0"], ["python","animations/rainbowscroll.py","--wall=1"]]],
            [20, [["python","animations/screw.py","--wall=0"]]],
            [20, [["python","animations/rainbowscroll.py","--wall=0"]]],
            [20, [["python","animations/multiwall_rainbowscroll.py"]]],
            [20, [["python","animations/s-color4-faster.py"]]],
            [20, [["python","animations/gameoflife.py"]]],
#            [20, [["python","animations/dmm/hackerbrucke.py"]]],
            #[20, [["python","animations/dmm/dt.py"]]],
#            [20, [["python","animations/dmm/uhrzeit.py"]]],
#            [20, [["python","animations/multiwall_warp_core.py"]]],
    ]
    return playlist
