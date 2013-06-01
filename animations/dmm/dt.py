from acabsl import send
from acabsl import update
import acabsl

import colorsys
import random
import time
import string

tick = 0.3
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

def printCLS(fade):
	update()
	for fx in range(16):
		for fy in range(6):
			send(fx,fy,back_r, back_g,back_b,fade)
	update()



def printDigit(digit, x,r,g,b, fade):
	Font_Letter=Font_ABC[digit]
	for fy in range(6):
		for fx in range(4):
			if (x+fx)>=0:
				if Font_Letter[fy][fx] == 1:
					send(x+fx,fy,r, g,b, fade)
				else:
					send(x+fx,fy,back_r, back_g,back_b, fade)




while 1:
	# Aktuelle Uhrzeit
	zeitH = time.localtime().tm_hour
	zeitM = time.localtime().tm_min	
	zeitS = time.localtime().tm_sec*4
	zeitDD = time.localtime().tm_mday
	zeitMM = time.localtime().tm_mon

	
	
	# Doppelpunkte
	
	#printCLS(0)
	printDigit(11,6,0,255-(zeitS),zeitS,tick*3)
	time.sleep(tick*2)
	printDigit(11,7,zeitS,255-(zeitS),0,tick*3)
	time.sleep(tick*3)

	

	# Zeit darstellen
	if zeitH<10 :
		 
		printDigit(6,-1,hour_r,hour_g,hour_b,tick*2)
		printDigit(zeitH,3,hour_r,hour_g,hour_b,tick*3)
	elif zeitH<20 :
		 
		printDigit(1,-1,hour_r,hour_g,hour_b,tick*2)
		printDigit(zeitH-10,3,hour_r,hour_g,hour_b,tick*3)
	else :
		 
		printDigit(2,-1,hour_r,hour_g,hour_b,tick*2)
		printDigit(zeitH-20,3,hour_r,hour_g,hour_b,tick*3)	
	
	printDigit(zeitM/10,8,minu_r,minu_g,minu_b,tick*3)
	printDigit(zeitM%10,12,minu_r,minu_g,minu_b,tick*2)
	update()
	time.sleep(tick*5)
	

		
	if(1 or zeitS/4%3==0):
		printDigit(12,6,255-zeitS,zeitS,255-zeitS,tick)
		printDigit(zeitDD/10,-1,minu_r,minu_g,minu_b,tick*2) 	
		printDigit(zeitDD%10,3,minu_r,minu_g,minu_b,tick*3)
		printDigit(zeitMM/10,8,hour_r,hour_g,hour_b,tick*3) 	
		printDigit(zeitMM%10,12,hour_r,hour_g,hour_b,tick*2)
		update()
		time.sleep(tick*3)
		printCLS(tick*3)
		time.sleep(tick*2)
