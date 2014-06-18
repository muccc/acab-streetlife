import dircache
import random


def getPlaylist():
    playlist = [
            #[time_in_seconds, [[simultanious_animation1, argument1, ...], [simultanious_animation2, argument1, ...], ...]]
            [15, [["python","animations/screw.py","--wall=0"]]],
            #[5, [["python","animations/rainbowscroll.py","--wall=0"]]],
            #[5, [["python","animations/multiwall_rainbowscroll.py"]]],
            #[5, [["python","animations/s-color4-faster.py"]]],
            #[5, [["python","animations/red-sym-scroll.py"]]],
            #[5, [["python","animations/multiwall_fullpulse.py"]]],
            #[5, [["python","animations/dropping.py"]]],
            [15, [["python","animations/multiwall_warp_core.py"]]],
    ]
    return playlist
