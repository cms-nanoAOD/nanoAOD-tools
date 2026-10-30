#!/bin/bash

#REFERENCE
#https://github.com/florez/CONDOR
printf "Start Running Histogramming at ";/bin/date
printf "Worker node hostname ";/bin/hostname

date
outputroot=$1
channel=$2
count=$3
Process=$4
Cluster=$5
echo "ouput root file wull be" $outputroot
echo "CONDOR DIR: $_CONDOR_SCRATCH_DIR"
cd ${_CONDOR_SCRATCH_DIR}
ls -ltr
cd -

#--------------------------------------------
# Go to local directory and creat condor directory
#---------------------------------------------
cd /home/mikumar/t3store3/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/condor_job/Runing_condor/
pwd
mkdir -p cutflow_${channel}_${count}_${Process}_${Cluster} 
cd cutflow_${channel}_${count}_${Process}_${Cluster}
pwd
scp -r /home/mikumar/t3store3/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/cutflow .
cd cutflow
pwd
scp $_CONDOR_SCRATCH_DIR/cutflowModule_new.py .
scp $_CONDOR_SCRATCH_DIR/condor_script_cutflow.py .
ls -a

#------------------------------------------------
# set cmsenv
#------------------------------------------------
export SCRAM_ARCH=slc7_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh
#scramv1 project CMSSW CMSSW_10_6_28
#cd CMSSW_10_6_28/src 
eval `scramv1 runtime -sh`

#--dd----------------------------------------------
# untar nanoaod tools ans list the directory
#------------------------------------------------
#mv ../../cutflow.tar.gz .
#tar --strip-components=0 -zxf cutflow.tar.gz
echo "-------------------------------"
echo "python crab_script_cutflow.py"
echo "------------------------------"
python condor_script_cutflow.py

printf "Done cutflow at ";/bin/date

#---------------------------------------------
#copy the output from remote machine to the lxplus
#------------------------------------------------
xrdcp -f Cutflow_hist.root ${outputroot}

#---------------------------------------------
#Remove the package, after copying the output
#------------------------------------------------
echo "Cleaning up condor directory"

cd ../../
rm -rf cutflow_${channel}_${count}_${Process}_${Cluster}
cd ${_CONDOR_SCRATCH_DIR}
#rm -rf cutflow.tar.gz
#rm -rf CMSSW_10_6_28
rm -rf *.py
ls -ltr
printf "Done ";/bin/date

