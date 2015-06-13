from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import sys

unpad = lambda s : s[0:-ord(s[-1])]

encoded = open("../encrypted", "r").read()
ha = SHA256.new()
ha.update(encoded)
check = ha.digest().encode("hex")

if(check != "91d0a6f55cce427132fc638b6beecf105c2cb0c817a4b7846ddb04e3132ea945"):
	print "BAD INPUT"
	sys.exit()

IV = '5353544943323031352d537461676532'.decode('hex')
key = ["9e2f31f7", "8153296b", "3d9b0ba6", "", "b0daf152", "b54cdc34", "ffe0d355", ""]

p1 = ["7695dc7c", "f61a3560", "36c2e6fc", "3c66fa3b", "8154c63a",
	"8ca39515", "e8c67d28", "7c16f3e9", "a5cb854f", "fbfac1eb"]

p2 = ["eda879c3", "26609fac", "c2e15ca0", "93fa1122", "db12fe60",
	"42404ba0", "c70a5383", "9dfc72db", "43210a41", "5a689be0"]

i1 = -1
i2 = 0

while True:
	i1 += 1
	if i1 == len(p1):
		i1 = 0
		i2 += 1
		if i2 == len(p2):
			print "Tested all"
			break
	key[3] = p1[i1]
	key[7] = p2[i2]
	obj = AES.new("".join(key).decode('hex'), AES.MODE_OFB, IV)
	decoded = unpad(obj.decrypt(encoded))
	hashed = SHA256.new()
	hashed.update(decoded)
	res = hashed.digest().encode("hex")

	if(res == "845f8b000f70597cf55720350454f6f3af3420d8d038bb14ce74d6f4ac5b9187"):
		print "Found correct key:", "".join(key)
		f = open("decrypted", "w")
		f.write(decoded)
		f.close()
		break
	else:
		print "Failed ",i1,i2,"".join(key)
