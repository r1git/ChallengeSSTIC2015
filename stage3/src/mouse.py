import sys
import struct
from PIL import Image, ImageDraw

mse = open("../paint.cap").read()
inf = "\xc0\x8d\xe7\xf6"+"\x00"*4+"\x43"

i=-1
startx = 0
starty = 0

im = Image.new('RGBA', (1024, 1024), (0, 255, 0, 0)) 
draw = ImageDraw.Draw(im) 

while(True):
	i = mse.find(inf, i+1)
	if i == -1:
		break
	mv = mse[i+0x40:i+0x44]	
	#sys.stdout.write(mv)

	if(mv[0]=='\x01'):
		but = True
	elif mv[0]=='\x00':
		but = False
	else:
		print "mouse != 1 !!!"
		but = False

	mvx = struct.unpack('b',mv[1])[0]
	mvy = struct.unpack('b',mv[2])[0]
	if mv[3]!='\x00':
		print "wheel !!!"

	if but:
		draw.line(((startx,starty), (startx+mvx,starty+mvy)), fill=128)
	startx += mvx
	starty += mvy
im.show()
