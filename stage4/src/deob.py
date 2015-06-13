import re
import sys

def repl(myfind, myto, mystr):
	fr = myfind.replace('$', '\\$')
	reg = r"(?<![_\$])(" + fr + r")(?![_\$])"
	pattern = re.compile(reg)
	return re.sub(reg, myto, mystr)


def main():
	f = open("firebug.js", "r").read()
	f = repl('_____', 'FUN1', f)
	f = repl('______', 'localVar', f)
	f = repl('________', 'arg', f)
	f = repl('_$__', 'localVar2', f)
	f = repl('_____________________', 'FUN2', f)
	f = repl('_______________________', 'FUN3', f)
	f = repl('___________________________', 'FUN4', f)
	f = repl('___________', 'index', f)
	f = repl('_', 'localArray', f)
	f = repl('$_', 'localVar3', f)
	f = repl('_$__', 'localVar4', f)
	f = repl('_$', 'localVar5', f)
	f = repl('_____$_', 'localArray2', f)
	f = repl('_$___', 'FUN5', f)
	f = repl('__$__', 'FUN6', f)
	f = repl('____$$', 'FUN7', f)
	f = repl('_$___', 'FUN8', f)
	f = repl('___$_', 'FUN9', f)

	for i in range(0,40):
		f2 = open("firebug.js", "r")
		l = f2.readline()
		while(l):
			#print l
			regex = r"[ \t]*([_\$]*) = (.*);$"
			pa = re.compile(regex)
			res = re.match(pa, l)
			if res:
				#print res.group(1), res.group(2)
				f = repl(res.group(1), res.group(2), f)	
			l = f2.readline()
		f = f.replace('\' + \'', '')
		f2.close()
	print f

main()
