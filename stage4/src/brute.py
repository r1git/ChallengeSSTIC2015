import re
import sys
import itertools
import time

from Crypto.Hash import SHA
from Crypto.Cipher import AES
from os import listdir, rename
from os.path import isfile, join, basename

unpad = lambda s : s[0:-ord(s[-1])]

data = open("data").read()[:-1].decode("hex")
ch = "08c3be636f7dffd91971f65be4cec3c6d162cb1c"

ptfm = ["Macintosh;", "Macintosh; U;"]
arch = ["Intel", "PPC"]
cy = ["", " fr;", " en-US;", " en-UK;", " en-GB;"]

version = [""]
for i in range(0,11):
	version += [" 10."+str(i)]

# Find possible firefox versions in online web page
rv = []
mydata = open("ffver.html").read()
reg = r"href=\"([0-9\.]+)/"
pattern = re.compile(reg)
res = re.findall(pattern, mydata)
rv = sorted(set(res))
# For each .0 version add the version without the .0
for el in rv:
	if(el[-2:] == ".0"):
		rv+=[el[:-2]]

all = [ptfm, arch, version, cy, rv]
total = len(ptfm)*len(arch)*len(version)*len(cy)*len(rv)
print "Trying a total of:", total
ct = 0
prog = 0
timer = 10000
stt = time.time()
for t in itertools.product(*all):
	timer -= 1
	if timer == 0:
		dt = time.time() - stt
		eta = (total / 10000) * dt	
		print "ETA:", eta, "s"
	if ct == total/10:
		prog+=1
		print str(prog*10)+"% done"
		ct = 0
	ua = t[0]+" "+t[1]+" Mac OS X"+t[2]+";"+t[3]+" rv:"+t[4]
	#print "<"+ua+">"

	iv = ua[:16]
	key = ua[-16:]
	if(len(key)<16):
		continue
	
	obj = AES.new(key, AES.MODE_CBC, iv)
	decoded = unpad(obj.decrypt(data))
	hashed = SHA.new()
	hashed.update(decoded)
	res = hashed.digest().encode("hex")

	if(res == ch):
		print "User agent found !"
		print ua
		f = open("decrypted", "w")
		f.write(decoded)
		f.close()
		sys.exit()
	ct += 1
