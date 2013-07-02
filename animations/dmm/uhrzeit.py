from acabsl import send
from acabsl import update
import acabsl

import colorsys
import random
import time
import string

tick = 0.2
back_r=0
back_g=0
back_b=0

hour_r=255
hour_g=32
hour_b=0

minu_r=0
minu_g=32
minu_b=255

Font_0=((0,0,1,0),(0,1,0,1),(0,1,0,1),(0,1,0,1),(0,1,0,1),(0,0,1,0))
Font_1=((0,0,1,0),(0,1,1,0),(0,0,1,0),(0,0,1,0),(0,0,1,0),(0,0,1,0))
Font_2=	((0,1,1,0),(0,0,0,1),(0,0,0,1),(0,0,1,0),(0,1,0,0),(0,1,1,1))
Font_3=	((0,1,1,0),(0,0,0,1),(0,0,1,0),(0,0,0,1),(0,0,0,1),(0,1,1,0))
Font_4=	((0,1,0,1),(0,1,0,1),(0,1,0,1),(0,1,1,1),(0,0,0,1),(0,0,0,1))
Font_5=	((0,1,1,1),(0,1,0,0),(0,1,1,0),(0,0,0,1),(0,0,0,1),(0,1,1,0))
Font_6=	((0,0,1,1),(0,1,0,0),(0,1,0,0),(0,1,1,1),(0,1,0,1),(0,1,1,1))
Font_7=	((0,1,1,1),(0,0,0,1),(0,0,1,0),(0,0,1,0),(0,1,0,0),(0,1,0,0))
Font_8=	((0,0,1,0),(0,1,0,1),(0,0,1,0),(0,1,0,1),(0,1,0,1),(0,0,1,0))
Font_9=	((0,1,1,1),(0,1,0,1),(0,1,0,1),(0,0,1,1),(0,0,0,1),(0,0,0,1))
Font__=	((0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0))
Font_D=	((0,0,0,0),(0,1,0,0),(0,0,0,0),(0,0,0,0),(0,1,0,0),(0,0,0,0))
Font_P=	((0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,1,0,0),(0,1,1,0))
Font_ABC=(Font_0, Font_1, Font_2, Font_3, Font_4, Font_5, Font_6, Font_7, Font_8, Font_9, Font__, Font_D, Font_P)

def printCLS():
	update()
	for fx in range(16):
		for fy in range(6):
			send(fx,fy,back_r, back_g,back_b,tick)
	update()



def printDigit(digit, x,r,g,b):
	Font_Letter=Font_ABC[digit]
	for fy in range(6):
		for fx in range(4):
			if (x+fx)>=0:
				if Font_Letter[fy][fx] == 1:
					send(x+fx,fy,r, g,b, tick)
				else:
					send(x+fx,fy,back_r, back_g,back_b, tick)

printCLS()
printDigit(9,6,0,255,0)
time.sleep(1)

printDigit(8,6,0,224,0)
time.sleep(1)

printDigit(7,6,0,192,0)
time.sleep(1)

printDigit(6,6,0,192,0)
time.sleep(1)

printDigit(5,6,64,192,0)
time.sleep(1)

printDigit(4,6,64,128,0)
time.sleep(1)

printDigit(3,6,64,96,0)
time.sleep(1)

printDigit(2,6,128,96,0)
time.sleep(1)

printDigit(1,6,192,0,0)
time.sleep(1)

printDigit(0,6,255,0,0)
time.sleep(1)


while 1:
	
	printCLS()
	printDigit(11,6,0,64,255)
	time.sleep(tick*1)
	printDigit(11,7,255,64,0)
	time.sleep(tick*1)
	printCLS()
	zeitH = time.localtime().tm_hour
	zeitM = time.localtime().tm_min
	


	if zeitH<10 :
		printDigit(0,-1,hour_r,hour_g,hour_b)
		printDigit(zeitH,3,hour_r,hour_g,hour_b)
	elif zeitH<20 :
		printDigit(1,-1,hour_r,hour_g,hour_b)
		printDigit(zeitH-10,3,hour_r,hour_g,hour_b)
	else :
		printDigit(2,-1,hour_r,hour_g,hour_b)
		printDigit(zeitH-20,3,hour_r,hour_g,hour_b)	
	

	if zeitM<10 :
		printDigit(0,8,minu_r,minu_g,minu_b)
		printDigit(zeitM,12,minu_r,minu_g,minu_b)
	else :
		printDigit(zeitM/10,8,minu_r,minu_g,minu_b)
		printDigit(zeitM%10,12,minu_r,minu_g,minu_b)
	update()
	time.sleep(tick*5)