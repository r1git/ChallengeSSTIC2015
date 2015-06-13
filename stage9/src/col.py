import random
import sys
data = open("../congratulations.gif", "r").read()

start = 0x10
end = 0x30a

while start != -1:
	start = data.find("\x00\x00\x00", start+1, end)
	if start != -1:
		a = int(random.random()*255)
		b = int(random.random()*255)
		c = int(random.random()*255)
		data = data[0:start]+chr(a)+chr(b)+chr(c)+data[start+3:]

sys.stdout.write(data)
