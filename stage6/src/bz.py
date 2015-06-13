f = open("../congratulations.jpg", "r").read()[0xd7d0:]
o = open("stage7.tar.bz2","w")
o.write(f)
o.close()

