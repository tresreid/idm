import os, sys

dirlist = os.listdir(os.getcwd())
for f in dirlist:
	if ('iDM_Mchi' in f) and ('ctau' not in f):
		fbase = f.split('_Wchi2-1p00e-03_')[0] +'_Wchi2-1p00e-03'
		fbase1 = fbase+'_ctau-0p012_tarball.tar.xz'
		fbase2 = fbase+'_ctau-0p12_tarball.tar.xz'
		fbase3 = fbase+'_ctau-1p2_tarball.tar.xz'
		fbase4 = fbase+'_ctau-12_tarball.tar.xz'
		fbase5 = fbase+'_ctau-120_tarball.tar.xz'
		#fbase1 = fbase+'_ctau-0p1_tarball.tar.xz'
		#fbase2 = fbase+'_ctau-1_tarball.tar.xz'
		#fbase3 = fbase+'_ctau-10_tarball.tar.xz'
		#fbase4 = fbase+'_ctau-100_tarball.tar.xz'
		#fbase5 = fbase+'_ctau-1000_tarball.tar.xz'
		cmd1 = 'cp {0} {1}'.format(f,fbase1)
		os.system(cmd1)
		cmd2 = 'cp {0} {1}'.format(f,fbase2)
		os.system(cmd2)
		cmd3 = 'cp {0} {1}'.format(f,fbase3)
		os.system(cmd3)
		cmd4 = 'cp {0} {1}'.format(f,fbase4)
		os.system(cmd4)
		cmd5 = 'cp {0} {1}'.format(f,fbase5)
		os.system(cmd5)
	print "done: ", f
print "complete"
