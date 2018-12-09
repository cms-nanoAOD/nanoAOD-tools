#!/bin/bash

#muon Muon_tightId
##ALPHA preselection
#"
#(Electron_pt[0]>10 && Electron_pt[1]>10 && Electron_cutBased[0]>0 && Electron_cutBased[1]>0) && 
#(Muon_pt[0]>10 && Muon_pt[1]>10 && Muon_mediumId[0]>0 && Muon_mediumId[1]>0 && Muon_pfRelIso04_all[0]<0.25 && Muon_pfRelIso04_all[1]<0.25 ) &&
#(Tau_pt[0]>18 && Tau_eta[0]<2.3 && Tau_idDecayMode==1 && DeltaBetaIso ??? && ) &&
#(Photon_pt[0]>15 &&  Photon_cutBased[0]>0)"

test1=3

if [ "$test1" == "0" ];then
    echo "LOCAL: SKIMMING + SLIMMING"
    python scripts/nano_postproc.py -c "Muon_pt[0]>20" -b "keep_and_drop_VH.txt" . /Users/shoh/Projects/CMS/PhD/Analysis/SSL/NANOAOD/HWplusJ_HToWWTo2L2Nu_WToLNu_M125_13TeV_powheg_pythia8-v1.root
elif [ "$test1" == "1" ];then
    echo "LOCAL: SKIMMING + SLIMMING + CLEANING + COMPUTING"
    python scripts/nano_postproc.py -c "nTau==0 && Muon_pt[0]>20" -b "keep_and_drop_VH.txt" -I PhysicsTools.NanoAODTools.postprocessing.operational.mhtjuProducerCpp mhtju . /Users/shoh/Projects/CMS/PhD/Analysis/SSL/NANOAOD/HWplusJ_HToWWTo2L2Nu_WToLNu_M125_13TeV_powheg_pythia8-v1.root
elif [ "$test1" == "2" ];then
    echo "LOCAL: SKIMMING + SLIMMING + CLEANING"
    python scripts/nano_postproc.py -c "Muon_pt[0]>20" -b "keep_and_drop_VH.txt" -I PhysicsTools.NanoAODTools.postprocessing.operational.objCleaning cleaning . /Users/shoh/Projects/CMS/PhD/Analysis/SSL/NANOAOD/DYJetsToLL_Pt-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext2-v1.root
elif [ "$test1" == "3" ];then
    echo "LOCAL: SKIMMING + SLIMMING + CLEANING + signal study"
    python python/analysis/signal/vh/signalAnalysis.py
elif [ "$test1" == "4" ];then
    echo "LOCAL: SKIMMING + SLIMMING + Object Cleaning Study"
    python scripts/nano_postproc.py -b "keep_and_drop_VH.txt" -I PhysicsTools.NanoAODTools.postprocessing.operational.cleaningStudy cleaning -E 100001 . /Users/shoh/Projects/CMS/PhD/Analysis/SSL/NANOAOD/DYJetsToLL_Pt-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext2-v1.root
elif [ "$test1" == "5" ];then
    echo "PD-T2: SKIMMING + SLIMMING + Object Cleaning Study"
    python scripts/nano_postproc.py -b "keep_and_drop_VH.txt" -I PhysicsTools.NanoAODTools.postprocessing.operational.cleaningStudy cleaning -E 100001 . /lustre/cmswork/hoh/NANO/SSLep/data/DYJetsToLL_Pt-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext2-v1.root
elif [ "$test1" == "6" ];then
    echo "LOCAL: SKIMMING + SLIMMING + PU"
    python scripts/nano_postproc.py -b "keep_and_drop_VH.txt" -I PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer puAutoWeight . /Users/shoh/Projects/CMS/PhD/Analysis/SSL/NANOAOD/DYJetsToLL_Pt-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext2-v1.root
elif [ "$test1" == "7" ];then
    echo "LOCAL: SKIMMING + SLIMMING + Object Cleaning Study + PU"
    python scripts/nano_postproc.py -b "keep_and_drop_VH.txt" -I PhysicsTools.NanoAODTools.postprocessing.operational.cleaningStudy cleaning -I PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer puAutoWeight . /Users/shoh/Projects/CMS/PhD/Analysis/SSL/NANOAOD/DYJetsToLL_Pt-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext2-v1.root
fi

#cleaningStudy

#HWminusJ_HToWWTo2L2Nu_WToLNu_M125_13TeV_powheg_pythia8-v1.root  HWplusJ_HToWW_M125_13TeV_powheg_pythia8-v1.root
#HWminusJ_HToWW_M125_13TeV_powheg_pythia8-v1.root                WmWmJJ_13TeV-powheg-pythia8_TuneCUETP8M1-v1.root
#HWplusJ_HToWWTo2L2Nu_WToLNu_M125_13TeV_powheg_pythia8-v1.root   WpWpJJ_13TeV-powheg-pythia8_TuneCUETP8M1-v1.root
