#!/bin/bash

test1=5

if [ "$test1" == "0" ];then
    echo "SKIMMING + SLIMMING"
    python scripts/nano_postproc.py -c "nTau==0 && Muon_pt[0]>20" -b "keepdropIN.txt" . /Users/shoh/Projects/CMS/PhD/Analysis/SSL/NANOAOD/HWplusJ_HToWWTo2L2Nu_WToLNu_M125_13TeV_powheg_pythia8-v1.root
elif [ "$test1" == "1" ];then
    echo "SKIMMING + SLIMMING + CLEANING + COMPUTING"
    python scripts/nano_postproc.py -c "nTau==0 && Muon_pt[0]>20" -b "keepdropIN.txt" -I PhysicsTools.NanoAODTools.postprocessing.operational.mhtjuProducerCpp mhtju . /Users/shoh/Projects/CMS/PhD/Analysis/SSL/NANOAOD/HWplusJ_HToWWTo2L2Nu_WToLNu_M125_13TeV_powheg_pythia8-v1.root
elif [ "$test1" == "2" ];then
    echo "SKIMMING + SLIMMING + CLEANING"
    python scripts/nano_postproc.py -c "Muon_pt[0]>20" -b "keepdropIN.txt" -I PhysicsTools.NanoAODTools.postprocessing.operational.objCleaning cleaning . /Users/shoh/Projects/CMS/PhD/Analysis/SSL/VHv9-skim_reprocess_v1/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v2.root
elif [ "$test1" == "3" ];then
    echo "SKIMMING + SLIMMING + CLEANING + signal study"
    for file in `ls /Users/shoh/Projects/CMS/PhD/Analysis/SSL/NANOAOD/*`
    do
	echo $file
	python scripts/nano_postproc.py -b "keepdropIN.txt" -I PhysicsTools.NanoAODTools.postprocessing.operational.signalStudy signal . ${file}
    done
elif [ "$test1" == "4" ];then
    echo "SKIMMING + SLIMMING + CLEANING + signal study"
    python scripts/nano_postproc.py -b "keepdropIN.txt" -I PhysicsTools.NanoAODTools.postprocessing.operational.signalStudy signal . /Users/shoh/Projects/CMS/PhD/Analysis/SSL/NANOAOD/HWminusJ_HToWW_M125_13TeV_powheg_pythia8-v1.root
elif [ "$test1" == "5" ];then
    echo "SKIMMING + SLIMMING + Object Cleaning Study"
    python scripts/nano_postproc.py -b "keepdropIN.txt" -I PhysicsTools.NanoAODTools.postprocessing.operational.cleaningStudy cleaning . /Users/shoh/Projects/CMS/PhD/Analysis/SSL/NANOAOD/HWminusJ_HToWW_M125_13TeV_powheg_pythia8-v1.root
fi

#cleaningStudy

#HWminusJ_HToWWTo2L2Nu_WToLNu_M125_13TeV_powheg_pythia8-v1.root  HWplusJ_HToWW_M125_13TeV_powheg_pythia8-v1.root
#HWminusJ_HToWW_M125_13TeV_powheg_pythia8-v1.root                WmWmJJ_13TeV-powheg-pythia8_TuneCUETP8M1-v1.root
#HWplusJ_HToWWTo2L2Nu_WToLNu_M125_13TeV_powheg_pythia8-v1.root   WpWpJJ_13TeV-powheg-pythia8_TuneCUETP8M1-v1.root
