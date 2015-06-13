import trans
import time
import sys
import struct
import hashlib

data = open("../input.bin").read()[0x9ad:]
good = "a5790b4427bc13e4f4e9f524c684809ce96cd2f724e29d94dc999ec25e166a81"
hur = "9128135129d2be652809f5a1d337211affad91ed5827474bf9bd7e285ecef321"

ha = hashlib.sha256()
ha.update(data)
check = ha.digest().encode("hex")

if(check != good):
        print "BAD INPUT"
	sys.exit()
else:
	print"Input Ok"

data = map(ord, data)
ctr = 0
timestart = time.time()
step = 500000
tried = 0

# bs is the Block Size unknwon value of bzip2 header (probably '9' == 0x39)
for bs in range(0x39, 0x30, -1):
	header = ("425a68"+str(hex(bs)[2:])+"314159265359").decode("hex")
	# crc1 and crc2 are the unknown 2 bytes of the crc32
	for crc1 in xrange(0,256):
	   for crc2 in xrange(0,256):
		#ti is the possible decrypted header tested
		ti = header+chr(crc1)+chr(crc2)
		
		# sh nth bit at 1 will take the 2nd solution for n+2*key[n]
		for sh in xrange(0, pow(2,12)):
			skip = False
			ctr+=1
			if(ctr%step==0 or tried>50):
				now = time.time()
				print "bs:", hex(bs), "index:",crc1,crc2, "time for last ",step,":", now-timestart, "s", "Tried:", tried, "sh:",sh
				tried = 0
				timestart = time.time()
			trans.LKey = [0]*12

			for i in range(0,12):
				# The 2 possible solutions
				if(sh & pow(2,i)):
					thissh = 0x100
				else:
					thissh = 0	
				calc = ((ord(ti[i]) ^ data[i]) | thissh) - i
				if calc%2 != 0:
					#print "Skip modulo"
					skip = True
					break
				if calc<0:
					skip = True
					break
				trans.LKey[i] = calc / 2
				if(trans.LKey[i]>255):
					skip = True
					break
			
			if(skip):
				continue

			trans.initi()	

			decr = [ trans.main(e) for e in data[0:0xf] ]
			# Expecting the 4 null bits
			if decr[0xe] & 0xf0 != 0:
				continue
			middle = [ trans.main(e) for e in data[0xf:0x21] ]
			# Expecting the 0xff value
			if middle[17] != 255:
				continue
			#If we are here we are going to try the full decryption and SHA256. This is expensive.
			tried += 1

			end = [ trans.main(e) for e in data[0x21:] ]
			decr = decr + middle + end
			decr = "".join(map(chr, decr))

			ha = hashlib.sha256()
			ha.update(decr)
			check = ha.digest().encode("hex")

			if(check == hur):
				print "We have a match !"
				f = open("decrypted", "w")
				f.write(decr)
				f.close()
				f = open("res", "w")
				f.write(str(map(chr, trans.LKey))+" bs"+hex(bs))
				f.close()
				sys.exit()
			else:
				pass
print "CTR:", ctr
