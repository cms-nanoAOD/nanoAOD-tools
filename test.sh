#!/bin/bash

test1=2

if [ "$test1" == "0" ];then
    echo "SKIMMING + SLIMMING"
    python scripts/nano_postproc.py -c "nTau==0 && Muon_pt[0]>20" -b "keepdropIN.txt" . /Users/shoh/Projects/CMS/PhD/Analysis/SSL/NANOAOD/HWplusJ_HToWWTo2L2Nu_WToLNu_M125_13TeV_powheg_pythia8-v1.root
elif [ "$test1" == "1" ];then
    echo "SKIMMING + SLIMMING + CLEANING + COMPUTING"
    python scripts/nano_postproc.py -c "nTau==0 && Muon_pt[0]>20" -b "keepdropIN.txt" -I PhysicsTools.NanoAODTools.postprocessing.operational.mhtjuProducerCpp mhtju . /Users/shoh/Projects/CMS/PhD/Analysis/SSL/NANOAOD/HWplusJ_HToWWTo2L2Nu_WToLNu_M125_13TeV_powheg_pythia8-v1.root
elif [ "$test1" == "2" ];then
    echo "SKIMMING + SLIMMING + CLEANING"
    python scripts/nano_postproc.py -c "nTau==0 && Muon_pt[0]>20" -b "keepdropIN.txt" -I PhysicsTools.NanoAODTools.postprocessing.operational.objCleaning cleaning . /Users/shoh/Projects/CMS/PhD/Analysis/SSL/datav8-skim/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8-v1.root
fi
