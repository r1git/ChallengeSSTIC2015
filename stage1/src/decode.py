import sys
import struct

f = open("../inject.bin", "rb")

def p(sttr, el=True):
	sys.stdout.write(sttr)
	if el:
		sys.stdout.write("\n")

def bytetochar(h, s):
	v = struct.unpack('B',h)[0]
	if (v+0x5d>=97 and v+0x5d<=122):
		v = v+0x5d
		if s:
			v -= 0x20
		res = chr(v)
	elif (v+0x13>=49 and v+0x13<=57):
		res = chr(v+0x13)
	elif v == 0x2c:
		res = ' '
	elif v == 0x2d:
		res = '_'
	elif v == 0x2e:
		res = '+'
	elif v == 0x27:
		res = '0'
	else:
		res = ''
	
	return res

def decode():
    byte = f.read(1)
    while byte != "":
	if byte == '\x00':
		#p("\nDELAY "+str(int(f.read(1).encode("hex"),16)))
		f.read(1)
	elif byte == '\x29':
		p("\nCTRL ESC")
	elif byte == '\x48':
		p("\nPAUSE")
	elif byte == '\x28':
		p("\nENTER")
		byte = f.read(1)
		if(byte!='\x00'):
			p("Enter not followed by 0")
	else:
		s = f.read(1)
		shift = False
		if(s == '\x02'):
			shift = True
		elif(s != '\x00'):
			p("???",False)
		b = bytetochar(byte, shift)
		if b=='':
			p("UNDECODED "+byte.encode("hex")+"("+byte+")")
		else:
			p(b, False)
	byte = f.read(1)

decode()
