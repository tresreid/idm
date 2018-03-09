#! /usr/bin/env python
import os, sys
import commands
import pwd
import argparse
import logging
from datetime import datetime

eos='/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select'
MGrelease='2.6.1'
CMSSWrelease='CMSSW_7_1_30'

def fileExistsInEos(user, filename):
    ## I am afraid one has to make this folder first if not existed
    exists = commands.getoutput('%s ls eos/cms/store/user/%s/gridpack/%s | wc -l' %(eos,user,filename)  )
    if len(exists.splitlines()) > 1: 
       exists = exists.splitlines()[1]
    else:
       exists = exists.splitlines()[0]
    #print exists
    return int(exists) == 1


if __name__ == '__main__':
    
    aparser = argparse.ArgumentParser(description='Process benchmarks.')
    aparser.add_argument('-carddir', '--carddir', action='store', dest='carddir',
            default='Cards/psdcalar_darkphoton_13TeV-madgraph', help='carddir')
    aparser.add_argument('-q', '--queue', action='store', dest='queue',
            default='2nw', help='queue')
    aparser.add_argument('-dm', '--dmrange', dest='dmrange', nargs='+', type=int,
            default=[50], help='dark matter mass range')
    aparser.add_argument('-med', '--medrange', dest='medrange', nargs='+', type=float,
            default=[0.4], help='mediator mass range')
    aparser.add_argument('-dw', '--dwrange', dest='dwrange', nargs='+', type=float,
            default=[2e-12], help='mediator decay width range')
    aparser.add_argument('-release', '--release', dest='release', action='store',
            default='2.6.1', help='MG version')
    aparser.add_argument('-runcms', '--runcms', action='store', dest='runcms',
            default='runcmsgrid_LO.sh', help='runcms')
    args = aparser.parse_args()
    if args.release:
        MGrelease=args.release

    logfn = datetime.now().strftime('%Y%b%d-%H%M')+ \
            '_'+args.carddir.split('/')[1].replace('_','-')+'.log'
    if not os.path.isdir('Logs'): os.mkdir('Logs')
    logging.basicConfig(level=logging.INFO, filename='Logs/{0}'.format(logfn))

    logging.info('{0:15}:{1}'.format('carddir', args.carddir))
    logging.info('{0:15}:{1}'.format('queue',   args.queue))
    logging.info('{0:15}:{1}'.format('dmrange', args.dmrange))
    logging.info('{0:15}:{1}'.format('medrange',args.medrange))

    user = pwd.getpwuid(os.getuid()).pw_name
    basedir = os.getcwd()
    carddirAbsPath = os.path.join(basedir,args.carddir)

    tempFile = [f for f in os.listdir(carddirAbsPath) if f.endswith('~')]
    if len(tempFile) > 0:
        os.system('rm %s/*~' % (carddirAbsPath))
    paramdirs  = [f for f in os.listdir(carddirAbsPath) if os.path.isdir(carddirAbsPath+'/'+f)]
    paramfiles = [f for f in os.listdir(carddirAbsPath) if os.path.isfile(carddirAbsPath+'/'+f)]

    mgcf = [f for f in paramfiles if 'madconfig' in f]
    proc = [f for f in paramfiles if 'proc' in f]
    cust = [f for f in paramfiles if 'custom' in f]
    spin = [f for f in paramfiles if 'madspin' in f]
    rwgt = [f for f in paramfiles if 'reweight' in f]
    #rtct = [f for f in paramfiles if 'mass' in f]

    logging.info('{0:15}:{1}'.format('madconfig', str(mgcf)))
    logging.info('{0:15}:{1}'.format('proc',      str(proc)))
    logging.info('{0:15}:{1}'.format('custom',    str(cust)))
    logging.info('{0:15}:{1}'.format('madspin',   str(spin)))
    logging.info('{0:15}:{1}'.format('reweight',  str(rwgt)))
    #logging.info('{0:15}:{1}'.format('mass',      str(rtct)))

    if len(proc) != 1:
        logging.error('process file does not exist or more than one! exiting..')
        sys.exit('ERROR on process file.')
    if len(mgcf) != 1:
        logging.error('config file does not exist or more than one! exiting..')
        sys.exit('ERROR on madconfig file.')
    if len(paramdirs) != 1:
        logging.error('model folder does not exist or more than one! exiting..')
        sys.exit('ERROR on model folder.')

    cmd = "cat %s | grep output | awk \'{print $2}\' " % (os.path.join(carddirAbsPath, proc[0]))
    procnamebase = commands.getoutput(cmd)
    logging.info('Process base name: {0}'.format(procnamebase))

    cmsswtmp = '/tmp/{0}/{1}'.format(user, CMSSWrelease)
    mgtmp    = '/tmp/{0}/{1}'.format(user, 'MG5_aMC_v'+MGrelease)
    if os.path.isdir(cmsswtmp):
        cmd = 'rm -rf {0}'.format(cmsswtmp)
        logging.info('{0} exists, cleaning... {1}'.format(cmsswtmp, cmd))
        os.system(cmd)
    if os.path.isdir(mgtmp):
        cmd = 'rm -rf {0}'.format(mgtmp)
        logging.info('{0} exists, cleaning... {1}'.format(mgtmp, cmd))
        os.system(cmd)

    #cmd = './doinstall.sh {0}'.format(MGrelease)
    logging.info('Installing MG... >>{0}'.format(cmd))
    os.system(cmd)
    MGrelease = MGrelease.replace('.', '_')
    mginstalled = procnamebase+'MG5_aMC_v'+MGrelease
    os.system('mv {0} {1}'.format('MG5_aMC_v'+MGrelease, mginstalled))
    logging.info('Madgraph has been installed successfully as {0}'.format(mginstalled))

    os.chdir(mginstalled)
    ## copy predefined madconfig, and start madgraph with it.
    cmd = 'cp {0} .'.format(os.path.join(carddirAbsPath, mgcf[0]))
    logging.info(cmd)
    os.system(cmd)
    cmd = './bin/mg5_aMC {0}'.format(mgcf[0])
    logging.info('Starting madgraph!! >>'+cmd)
    os.system(cmd)

    logging.info('Loading model..')
    ## copy input UFO files into ./models folder
    cmd = 'cp -r {0} models/'.format(os.path.join(carddirAbsPath, paramdirs[0]))
    os.system(cmd)
    os.chdir('models/{0}'.format(paramdirs[0]))
    #os.system('python write_param_card.py')
    logging.info('Model loaded!')

    ## changing to madgraph directory
    os.chdir(os.path.join(basedir, mginstalled))


    params = [(dm, med, dw) for dm in args.dmrange for med in args.medrange for dw in args.dwrange]
    for p in params:

        dm, med, dw = p
        dl = (dm/med)*(2e-14/dw) # decay length

        dmstr = str(dm)
        medstr = str(med).replace('.', 'p') if '.' in str(med) else str(med)
        dlstr = str(dl).replace('.', 'p') if '.' in str(dl) else str(dl)
        procname = procnamebase.replace('XMASS', dmstr).replace('MED', medstr).replace('LENGTH', dlstr)

        logging.info('creating models for param: (dm, med, dw): ({0}).'.format(str(p)))
        customizedModelDirName = '_'.join([paramdirs[0], dmstr, medstr, dlstr])
        ## copying input UFO folders into ./models, with paramtrized name
        cmd = 'cp -r {0} models/{1}'.format(os.path.join(carddirAbsPath, paramdirs[0]),
                                            customizedModelDirName)
        logging.info(cmd)
        os.system(cmd)

        #paramFilesToRun = [f for f in os.listdir(os.path.join(os.getcwd(), 'models', customizedModelDirName)) \
        #        if os.path.isfile(os.path.join(os.getcwd(), 'models', customizedModelDirName, f))]
        #procToBeSed = [f for f in paramFilesToRun if 'proc' in f]
        #custToBeSed = [f for f in paramFilesToRun if 'custom' in f]
        os.system('rm -rf {0}/*py~'.format(os.path.join(os.getcwd(), 'models', customizedModelDirName)))
        paramInModelToBeSed = os.path.join(os.getcwd(), 'models', customizedModelDirName, 'parameters.py')
        
        cmd = 'sed -i "s/{0}/{1}/g" {2}'
        os.system(cmd.format('X_MZP_X', str(med), paramInModelToBeSed))
        os.system(cmd.format('X_MPS_X', str(dm), paramInModelToBeSed))

        #os.system(cmd.format('XMASS', dmstr,  procToBeSed[0]))
        #os.system(cmd.format('MED',   medstr, procToBeSed[0]))
        #os.system(cmd.format('LENGTH',dlstr,  procToBeSed[0]))
        #os.system(cmd.format('XMASS', dmstr,  custToBeSed[0]))
        #os.system(cmd.format('MED', str(med), custToBeSed[0]))
        #os.system(cmd.format('WIDTH', str(dw),custToBeSed[0]))

        os.chdir('models/'+customizedModelDirName)
        os.system('python write_param_card.py')

        ## going back to madgraph directory
        os.chdir(os.path.join(basedir, mginstalled))
        ## making a directory containing all the input cards, with procname as suffix..
        customizedCardDirName = 'MG_{0}'.format(procname)
        os.system('mkdir {0}'.format(customizedCardDirName))

        for f in paramfiles:
            os.system('cp {0}/{1} {2}'.format(carddirAbsPath, f, customizedCardDirName))

        os.system(cmd.format('XMASS', dmstr,  'MG_'+procname+'/'+proc[0]))
        os.system(cmd.format('MED',   medstr, 'MG_'+procname+'/'+proc[0]))
        os.system(cmd.format('LENGTH',dlstr,  'MG_'+procname+'/'+proc[0]))
        os.system(cmd.format('XMASS', dmstr,  'MG_'+procname+'/'+cust[0]))
        os.system(cmd.format('MED', str(med), 'MG_'+procname+'/'+cust[0]))
        os.system(cmd.format('WIDTH', str(dw),'MG_'+procname+'/'+cust[0]))

        jobFn = os.path.join(basedir, mginstalled, customizedCardDirName, 'integrate.sh')
        jobF = open(jobFn, 'w')
        
        jobF.write('#!/bin/bash\n')
        jobF.write('cp -r {0} .\n'.format(os.path.join(basedir, mginstalled, customizedCardDirName)))
        jobF.write('''
user=`id -u -n`
if [ ! -d "/tmp/$user/CMSSW_7_1_30" ]; then
    cd /tmp/$user
    scramv1 project CMSSW CMSSW_7_1_30
fi 
cd /tmp/$user/CMSSW_7_1_30/src

eval `scramv1 runtime -sh`
LHAPDFCONFIG=`echo "$LHAPDF_DATA_PATH/../../bin/lhapdf-config"`
LHAPDFINCLUDES=`$LHAPDFCONFIG --incdir`
LHAPDFLIBS=`$LHAPDFCONFIG --libdir`\n''')
        jobF.write('cd {0}\n'.format(os.path.join(basedir, mginstalled, customizedCardDirName)))
        jobF.write('{0}/bin/mg5_aMC {1}\n'.format(os.path.join(basedir, mginstalled), proc[0]))

        ## above will output a folder named as procname
        jobF.write('cp {0} {1}\n'.format(cust[0], procname))
        jobF.write('cd {0}\n'.format(procname))

        for f in paramfiles:
            if 'dat' in f:
                jobF.write('mv ../{0} Cards \n'.format(f))
        jobF.write('echo "done" >> makegrid.dat \n')
        jobF.write('cat {0} >> makegrid.dat \n'.format(cust[0]))
        jobF.write('echo "set gridpack true" >> makegrid.dat \n')
        jobF.write('echo "" >> makegrid.dat \n')
        jobF.write('echo "done" >> makegrid.dat \n')
        jobF.write('cat makegrid.dat | ./bin/generate_events pilotrun \n')
        jobF.write('cd .. \n')
        jobF.write('mkdir process \n')
        jobF.write('mv {0}/pilotrun_gridpack.tar.gz process \n'.format(procname))
        jobF.write('mv {0}/Events/pilotrun/unweighted_events.lhe.gz process \n'.format(procname))
        jobF.write('cd process \n')
        jobF.write('tar xzf pilotrun_gridpack.tar.gz  \n')
        jobF.write('rm pilotrun_gridpack.tar.gz  \n')
        jobF.write('echo "mg5_path = ../../mgbasedir" >> ./madevent/Cards/me5_configuration.txt \n')
        jobF.write('echo "run_mode = 0" >> ./madevent/Cards/me5_configuration.txt \n')  
        jobF.write('cd .. \n')
        jobF.write('cp %s/cleangridmore.sh .    \n'  % (basedir))
        jobF.write('cp %s/%s runcmsgrid.sh      \n'  % (basedir,args.runcms))
        jobF.write('./cleangridmore.sh          \n')
        jobF.write('mkdir  mgbasedir     \n')
        
        for d in ['MadSpin', 'SysCalc', 'input', 'HELAS', 'README', 'Template', 'VERSION', 'aloha', \
                'bin', 'madconfig', 'madgraph', 'mg5decay', 'models', 'tests', 'vendor', 'PLUGIN']:
            jobF.write('cp -r {0} mgbasedir \n'.format(os.path.join(basedir, mginstalled ,d)))

        output = '{0}_tarball.tar.xz'.format(procname)
        jobF.write('XZ_OPT="--lzma2=preset=9,dict=512MiB" tar -cJpsf {0} mgbasedir process runcmsgrid.sh \n'.format(output))
        jobF.write(('rm   /eos/user/%s/%s/gridpacks/%s  \n') % (user[0],user,output))
        jobF.write(('scp %s  /eos/user/%s/%s/gridpacks/%s  \n') % (output,user[0],user,output))
        jobF.close()

        os.chmod(jobFn, 0777)

        if not fileExistsInEos(user, output):
            cmd = 'bsub -q {0} -R "rusage[mem=12000]" {1}'.format(args.queue, jobFn)
            logging.info(cmd)
            os.system(cmd)
