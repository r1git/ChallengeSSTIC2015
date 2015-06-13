import struct
import zlib

f = open("../congratulations.png","r").read()
res = ""
start = 0
ct = 0

while start!=-1:
	start = f.find("sTic", start+1)
	if(start != -1):
		size = struct.unpack(">I", f[start-4:start])[0]
		print "Found - Num:", ct, "Size:", size, "@", hex(start)
		if size <= 4919:
			res  = res + f[start+4:start+size+4]
		ct+=1

print "Total len:", len(res)

unco = zlib.decompress(res, 32)

f = open("stage8.tar.bz2", "w")
f.write(unco)
f.close()
