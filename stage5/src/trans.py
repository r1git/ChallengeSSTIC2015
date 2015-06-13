import sys

var4 = 0
def F4(key):
	global var4
	for e in key:
		var4 = (var4 + e) & 0xff	
	return var4

var5 = 0
def F5(key):
	global var5
	for e in key:
		var5 = (var5 ^ e) & 0xff	
	return var5

var6_3 = 0
var6_1 = 0
def F6(key):
	global var6_3, var6_1
	if var6_3 == 0:
		for e in key:
			var6_1 = (var6_1 + e) & 0xffff				
		var6_3 = 1		
	aux1 = (var6_1 << 1) & 0xffff
	aux2 = (var6_1 & 0x4000) >> 0xe
	aux3 = (var6_1 & 0x8000) >> 0xf

	var6_1 = (aux1 ^ ((aux2 ^ aux3) & 0xffff)) & 0xffff
	return (var6_1 & 0xff)

def F7(key):
	res1 = 0
	res2 = 0
	for i in range(0,6):	
		res1 = (key[i]+res1) & 0xff	
		res2 = (key[i+6]+res2) & 0xff
	return (res1 ^ res2) & 0xff

var8_5 = []
var8_5.append([0]*12)
var8_5.append([0]*12)
var8_5.append([0]*12)
var8_5.append([0]*12)
var8_4 = 0
def F8(key):
	global var8_5, var8_4
	var8_5[var8_4] = key 
	var8_4+=1
	if var8_4 == 4:
		var8_4 = 0
	res = 0
	for i2 in range(0,4):
		acc = 0
		for i0 in range(0,12):
			acc = (acc + var8_5[i2][i0]) & 0xff
		res = (res ^ acc) & 0xff

	return res

def F9(key):
	res = 0	
	for i in range(0,12):
		res = ((key[i] << (0x7 & i)) ^ res) & 0xff
	
	return res
		
var10_4 = []
var10_4.append([0]*12)
var10_4.append([0]*12)
var10_4.append([0]*12)
var10_4.append([0]*12)
var10_2 = 0
def F10(key):
	global var10_4, var10_2
	var10_4[var10_2] = key	
	var10_2+=1
	if(var10_2==4):
		var10_2=0
	res = 0
	for i in range(0,4):
		res = (res + var10_4[i][0]) & 0xff	

	index = res & 0x3
	chrn = ((res >> 4) % 0xc) & 0xff
	
	return var10_4[index][chrn]

var12_3 = [0]*12
def F12(key, read):
	global var12_3
	tosend = (var12_3[1] ^ var12_3[5] ^ var12_3[9]) & 0xff
	var12_3 = key	
	index = (read % 0xc) & 0xff
	res2 = var12_3[index]

	return tosend, res2


def F11(key):
	tosend = (key[0] ^ key[3] ^ key[7]) & 0xff
	read, res2 = F12(key, tosend)
	index = (read % 0xc) & 0xff
	res1 = key[index]

	return res1, res2

def F1(key):
	res1 = F4(key)
	res2 = F5(key)
	res3 = F6(key)
	return res1 ^ res2 ^ res3

def F2(key):
	res1 = F7(key)
	res2 = F8(key)
	res3 = F9(key)
	return res1 ^ res2 ^ res3

def F3(key):
	res1 = F10(key)
	res2, res3 = F11(key)
	#res3 = F12(key)
	return res1 ^ res2 ^ res3

LKey = []
L4 = 0
def main(ch):
	global LKey, L4
	newkey = (F1(LKey) ^ F2(LKey) ^ F3(LKey)) & 0xff
	res = (ch ^ (L4 + 2*LKey[L4])) & 0xff
	LKey = LKey[:]
	LKey[L4] = newkey
	L4+=1
	if(L4 == 0xc):
		L4 = 0
	return res

def initi():
	global var4, var5, var6_3, var6_1, var8_5, var8_4, var10_4, var10_2, var12_3, L4
        var4 = 0
        var5 = 0
        var6_3 = 0
        var6_1 = 0
        var8_5 = []
        var8_5.append([0]*12)
        var8_5.append([0]*12)
        var8_5.append([0]*12)
        var8_5.append([0]*12)
        var8_4 = 0
        var10_4 = []
        var10_4.append([0]*12)
        var10_4.append([0]*12)
        var10_4.append([0]*12)
        var10_4.append([0]*12)
        var10_2 = 0
        var12_3 = [0]*12
        #LKey = []
        L4 = 0


if __name__ == '__main__':
	data = "1d87c4c4e0ee40383c59447f23798d9fefe74fb82480766e".decode("hex")
	LKey = map(ord, '*SSTIC-2015*')
	for e in data:
		sys.stdout.write(chr(main(ord(e))))
	print ""
