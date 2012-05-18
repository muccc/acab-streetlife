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
            [20, ["rainbowwall.py", "randomfade.py"]],
            [30, ["s-color4.py"]] ,
            [30, ["s-rainbowscroll.py"]] ,
            #[5, ["audiocolors.py"]],
            [5, ["crazy.py"]] ,
            [15, ["kiu-arrows.py"]],
            #[6, ["jamaikabeat.py"]],
            [10, ["lines.py", "lines.py"]],
            #[15, ["kiu-diebar-rwb.py"]],
            #[10, [ddc_chooser()]],
            [20, ["die_bar_thema.py"]], 
            [15, ["dots.py"]],
            #[30, ["mc3_pixelpushers.py"]],
            #[30, ["s-color.py"]] ,
    #	    [120, ["randomfade2.py"]],
            #[5, ["audiocolors.py"]],
            [30, ["rainbowwall2.py"]],
            #[40, ["kiu-font-acab.py"]],
            #[15, [ddc_chooser()]],
            [40, ["kiu-infinity.py"]],
            #[5, ["jamaikabeat.py"]],
            [60, ["kiu-random_pixels.py"]],
            [15, ["kiu-soft-scroll.py"]],
            [30, ["s-color2.py"]] ,
            #[15, ["kiu-diebar-rw.py"]],
            [30, ["kiu-wabern.py"]],
            [30, ["s-color4.py"]] ,
            #[10, [ddc_chooser()]],

            #[30, ["die_bar_thema.py"]],
            #[5, ["jamaikabeat.py"]],
            #[time_in_seconds, [simultaniois_animation1, simultanious_animation2, ....]]
    ]
    for entry in playlist:
        entry[1] = [ 'animations/'+path for path in entry[1]]
    return playlist
