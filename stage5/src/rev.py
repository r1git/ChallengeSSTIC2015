import struct
import sys

A = ""
B = ""
C = ""
oreg = 0

def ps():
	global A,B,C
	print "A = ",A
	print "B = ",B
	print "C = ",C

def push(i):
	global A,B,C
	C=B
	B=A
	A=i

def fpop():
	global A,B,C
	res = A
	A=B
	B=C
	return res

popf = open("pop.txt", "r")

pop = []
popi =[]
for i in range(0,16):
	ops = popf.readline().rstrip().split(' ')
	pop.append(ops[0])

for i in range(0,16):
	ops = popf.readline().rstrip()
	popi.append(ops)

popf = open("sec2.txt", "r")

sec = []
seci = []
for line in popf:
	ops = line.rstrip().split(' ')
	sec.append(ops[0])
	if len(ops)>1:
		seci.append(" ".join(ops[1:]))
	else:
		seci.append("")

if(len(sys.argv) >= 3):
	start = int(sys.argv[2])
else:
	start = 1

if(len(sys.argv) >= 4):
	ad = int(sys.argv[3])
else:
	ad = 0

data = open(sys.argv[1], "r").read()[start:]
prev = -1
for op in data:
	m = struct.unpack("B", op)[0]
	o = (m & 0xf0) >> 4	
	n = (m & 0x0f)
	if o == 0xf:
		ind = 0
		if prev>=0x21 and prev<=0x29:
			ind = prev-0x20
		do = sec[n+ind*16]
		doi = seci[n+ind*16]
	else:
		do = ""
		doi = ""
	print '{0:5s} {1:5s} {2:5s} {3:10s} {4:5s} {5:24s} {6:16s}'.format(hex(ad), hex(m), pop[o], do, hex(n), popi[o], doi)
	if(prev<0x21 or prev>0x29):
		if(o==1):
			push("&STACK["+str(n)+"]")
		elif(o==2):
			oreg |= n
			oreg <<= 4
		elif(o==4):
			push(hex(n|oreg))
		elif(o==6):
			oreg |= ~n
			oreg <<= 4 
		elif(o==7):
			push("STACK["+str(n)+"]")
		elif(o==8):
			push("("+fpop()+" + "+hex(n|oreg)+")")
		elif(o==0xd):
			print("STACK["+str(n)+"] = "+fpop())
		elif(o==0xf):
			if(n==1):
				if(A[0] == '&'):
					A = A[1:]
				else:
					A = "*("+A+")"
			elif(n==2):
				arr = fpop()
				index = fpop()
				push(arr+"["+index+"]")
			elif(n==5):
				push("("+fpop()+" + "+fpop()+")")
			elif(n==8):
				push("("+fpop()+" * "+fpop()+")")
			elif(n==9):
				print("if "+fpop()+" > "+fpop())
			elif(n==0xa):
				index = fpop()
				arr = fpop()
				push(index+"[4*"+arr+"]")
		if(o!=2 and o!=6):
			oreg = 0
	else:
	    if(o==0xf):
	    	oreg = 0
		if(prev==0x23):
			if(n==3):
				push("("+fpop()+" ^ "+fpop()+")")
			elif(n==0xb):
				dest = fpop()
				if(dest[0]=='&'):
					dest = dest[1:]
				val = fpop()
				print(dest+" = "+val)
		elif(prev==0x24):
			if(n==0):
				val1 = fpop()
				val2 = fpop()
				push("("+val2+" >> "+val1+")")
			if(n==1):
				val1 = fpop()
				val2 = fpop()
				push("("+val2+" << "+val1+")")
			if(n==6):
				push("("+fpop()+" & "+fpop()+")")
		elif(prev==0x21):
			if(n==0xf):	
				val1 = fpop()
				val2 = fpop()
				push("("+val2+" % "+val1+")")
		elif(prev==0x25):
			if(n==0xa):
				C=B
				B=A
	    elif(o==2):
		oreg |= n
		oreg <<= 4

				
	#ps()
				
				
	prev = m
	ad += 1
