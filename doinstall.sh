#!/bin/bash

# Lite version of:
# https://github.com/cms-sw/genproductions/blob/mg26x/bin/MadGraph5_aMCatNLO/gridpack_generation.sh

version=$1
#exit on first error
set -e

RUNHOME=`pwd`

echo "Starting job on " `date` #Only to display the starting of production date
echo "Running on " `uname -a` #Only to display the machine where the job is running
echo "System release " `cat /etc/redhat-release` #And the system release


MG=MG5_aMC_v${version}.tar.gz
#MGSOURCE=https://cms-project-generators.web.cern.ch/cms-project-generators/$MG
MGSOURCE=/afs/cern.ch/cms/generators/www/$MG
MGBASEDIRORIG=`echo MG5_aMC_v${version} | tr '.' '_'`

SYSCALC=SysCalc_V1.1.6.tar.gz
SYSCALCSOURCE=/afs/cern.ch/cms/generators/www/$SYSCALC

isscratchspace=0
user=`id -u -n`
if [ ! -d "/tmp/$user/CMSSW_7_1_30" ]; then
    cd /tmp/$user
    scramv1 project CMSSW CMSSW_7_1_30
fi 
cd /tmp/$user/CMSSW_7_1_30/src

eval `scramv1 runtime -sh`
echo $CMSSW_BASE
cd $RUNHOME

#Copy, Unzip and Delete the MadGraph tarball#
#wget --no-check-certificate ${MGSOURCE}
cp ${MGSOURCE} .
tar xzf ${MG}
rm $MG

#Apply any necessary patches on top of official release
cd $MGBASEDIRORIG
#cat $RUNHOME/patches/*.patch | patch -p1

LHAPDFCONFIG=`echo "$LHAPDF_DATA_PATH/../../bin/lhapdf-config"`
LHAPDFINCLUDES=`$LHAPDFCONFIG --incdir`
LHAPDFLIBS=`$LHAPDFCONFIG --libdir`
cd $CMSSW_BASE/src/
BOOSTINCLUDES=`scram tool tag boost INCLUDE`
echo $BOOSTINCLUDES
cd -
#echo  $LHAPDFCONFIG
echo "set auto_update 0"                  >  mgconfigscript
echo "set automatic_html_opening False"   >> mgconfigscript
#echo "set output_dependencies internal"   >> mgconfigscript
echo "set lhapdf $LHAPDFCONFIG"           >> mgconfigscript
if [ -n "$queue" ]; then
    echo "set run_mode  1"                 >> mgconfigscript
    echo "set cluster_type lsf"            >> mgconfigscript
    echo "set cluster_queue $queue"        >> mgconfigscript
    echo "set cluster_status_update 60 30" >> mgconfigscript
    echo "set cluster_nb_retry 5"          >> mgconfigscript
    echo "set cluster_retry_wait 300"      >> mgconfigscript 
    if [[ ! "$RUNHOME" =~ ^/afs/.* ]]; then
        echo "local path is not an afs path, batch jobs will use worker node scratch space instead of afs"
        echo "set cluster_temp_path `echo $RUNHOME`" >> mgconfigscript 
        isscratchspace=1
    fi      
else
    echo "set run_mode 2" >> mgconfigscript
fi
echo "save options" >> mgconfigscript
./bin/mg5_aMC mgconfigscript
#cp ../patches/mg5_configuration.txt input
rm mgconfigscript

#get syscalc and compile
#wget --no-check-certificate ${SYSCALCSOURCE}
cp ${SYSCALCSOURCE} .
tar xzf ${SYSCALC}
rm $SYSCALC
cd SysCalc
sed -i "s#INCLUDES = -I../include#INCLUDES = -I../include -I${BOOSTINCLUDES}#g" src/Makefile  
PATH=`${LHAPDFCONFIG} --prefix`/bin:${PATH} make
cd ..
cd $RUNHOME

