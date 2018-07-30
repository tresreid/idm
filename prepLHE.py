import os, sys
import subprocess

gridpackdir = os.listdir(os.getcwd()+"/producedgridpacks/ctau1000/")

for f in gridpackdir:
	if('iDM_Mchi' in f) and ('ctau' in f):
		ctau_str = f.split('ctau-')[1].split('_tarball')[0]
		ctau = float(ctau_str.replace('p','.'))*10
		#print ctau
		#print f
		cmd1 = 'python extractLHEFromGridpack.py producedgridpacks/ctau1000/%s' %(f)
		process = subprocess.Popen(cmd1,shell=True, stdout=subprocess.PIPE)
		for line in iter(process.stdout.readline,b''):
			print line,
		process.stdout.close()
		process.wait()
		lhe = f.split(".")[0] +".lhe"
		cmd2 = "python LHEs/replaceLHELifetime.py -i LHEs/%s -t %s"%(lhe,ctau)
		process1 = subprocess.Popen(cmd2,shell=True,stdout=subprocess.PIPE)
		print "replacing life with: ", ctau
		process1.wait()
		cmd3 = "gzip LHEs/%s"%(lhe)
		os.system(cmd3)
		print "done: ",f
	
