#!/bin/bash

#REFERENCE
#https://github.com/florez/CONDOR

date
myArg1=$1
myArg2=$2
myArg3=$3
#myArg4=$4
echo $1
echo $2
echo "CONDOR DIR: $_CONDOR_SCRATCH_DIR"
cd ${_CONDOR_SCRATCH_DIR}
#cp -r /home/mikumar/tryout .
mkdir tryout
mv haddnano.py tryout/
mv hadd.sh tryout/
 
#------------------------------------------------
#------------------------------------------------
cd /home/mikumar/t3store3/workarea/Nanoaod_tools/CMSSW_10_2_28/src
source /cvmfs/cms.cern.ch/cmsset_default.sh
pwd
eval `scramv1 runtime -sh`
cd ${_CONDOR_SCRATCH_DIR}/tryout/
ls -ltr
#./hadd.sh $myArg1 . $myArg2 -j4
./hadd.sh $myArg1 . $myArg2 -j4
#root -l -b -q "minitree_data_mu.C($myArg1, $myArg2, $myArg3, $myArg4)"

#---------------------------------------------
#copy the output from remote machine to the lxplus
#or to any other place e.g. Tier-2
#Remove the package, after copying the output
#------------------------------------------------
echo "OUTPUT: "
ls -ltrh ${_CONDOR_SCRATCH_DIR}/tryout/

rsync -avz ${_CONDOR_SCRATCH_DIR}/tryout/Minitree*.root $myArg3
#rsync -avz ${_CONDOR_SCRATCH_DIR}/tryout/Cutflow*.root $myArg3
#cp -rf ${_CONDOR_SCRATCH_DIR}/tryout/Minitree*.root $myArg3
cd ${_CONDOR_SCRATCH_DIR}
rm -rf truout/
echo "DONE"
date

