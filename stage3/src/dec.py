from CryptoPlus.Cipher import python_Serpent
from Crypto.Hash import SHA256
import sys
import serpent

#key = Blake256("The quick brown fox jumps over the lobster dog")
key = "66c1ba5e8ca29a8ab6c105a9be9e75fe0ba07997a839ffeae9700b00b7269c8d"

unpad = lambda s : s[0:-ord(s[-1])]

encoded = open("../encrypted", "r").read()
ha = SHA256.new()
ha.update(encoded)
check = ha.digest().encode("hex")

if(check != "6b39ac2220e703a48b3de1e8365d9075297c0750e9e4302fc3492f98bdf3a0b0"):
	print "BAD INPUT"
	sys.exit()

IV = '5353544943323031352d537461676533'.decode('hex')
print IV

obj = python_Serpent.new(key.decode('hex'), python_Serpent.MODE_CBC, IV)
print "Trying"

decoded = obj.decrypt(encoded)[:-2]
print "Done"
hashed = SHA256.new()
hashed.update(decoded)
res = hashed.digest().encode("hex")

if(res == "7beabe40888fbbf3f8ff8f4ee826bb371c596dd0cebe0796d2dae9f9868dd2d2"):
	print "Yesss !"
else:
	print "Failed "

f = open("decrypted", "w")
f.write(decoded)
f.close()
