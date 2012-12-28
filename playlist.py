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
            #[time_in_seconds, [simultaniois_animation1, simultanious_animation2, ....]]
            [20, ["wall0_screw.py", "wall1_rainbowscroll.py"]],
            [20, ["multiwall_rainbowscroll.py"]],
            [20, ["warp_core.py"]],
    ]
    for entry in playlist:
        entry[1] = [ 'animations/'+path for path in entry[1]]
    return playlist
