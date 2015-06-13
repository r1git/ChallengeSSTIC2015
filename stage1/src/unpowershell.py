import base64
import string
import sys

f = open("decoded", "rb")

for line in f:
	if line[0:10] == "powershell":
		dec = base64.b64decode(line[16:])
		dec = filter(lambda x: x in string.printable, dec)
		start = dec.find('FromBase64String')
		if start == -1:
			continue
		start += 18
		end = dec.find("')",start)
		sys.stdout.write(base64.b64decode(dec[start:end]))
