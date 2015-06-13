import sys

data = open("../congratulations.tiff").read()[0x80:]
data = map(ord, data)

byte = ""
res = ""

length = 474
width = 636

for y in xrange(0, length):
	for x in xrange(0, width*3, 12):
		byte = ""
		for j in range(0,12):
			# Skip 1 byte every 3 bytes
			if((j+1)% 3 !=0):
				byte = byte + str(data[(x+y*width*3)+j] & 1)
		res += chr(int(byte,2))

sys.stdout.write(res)
