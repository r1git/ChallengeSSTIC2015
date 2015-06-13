import struct

data = open("../input.bin", "r").read()

i = 0xf8+1
n = 1
size = 1
while(size!=0):
	F1 = data[i:i+0xc]
	#fi = open("F"+str(n),"w")
	#fi.write(F1)
	#fi.close()
	size = struct.unpack("<I", F1[0:4])[0]
	dest = struct.unpack("<I", F1[4:8])[0]
	print "T"+str(n)+":", "Index", hex(i), "Size", hex(size), "Dest", hex(dest)
	i += 0xc
	if size != 0:
		D1 = data[i:i+size]
		fi = open("T"+str(n),"w")
		fi.write(D1)
		fi.close()
		i += size
	n+=1
