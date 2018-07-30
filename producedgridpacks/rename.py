import os, sys

files = [ x for x in os.listdir(os.getcwd()) if ".tar" in x]
for f in files:
	cmd = "cp %s rename/tar_%s"%(f,f)
	os.system(cmd)
