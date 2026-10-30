#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from EfficiencyModule import *


treecut=" Entry$<500 "
#inputFiles=["root://cms-xrd-global.cern.ch///store/mc/RunIISummer16NanoAODv3/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/NANOAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/120000/E4046A1B-A2E1-E811-8878-0025905B85DC.root"]
inputFiles=["/afs/cern.ch/user/m/mikumar/work/private/NanoAOD_new/CMSSW_10_6_0/src/Inputroot_files/Tree/ST_tch/06314878-0D6B-544B-9E2C-C5EDCD0666D3_2017.root"]
p=PostProcessor(".",
		inputFiles,
		treecut,  #efficecncy histogram there shoulld be no cut
		modules=[EfficiencyConstr_2017()],
		outputbranchsel="clean.txt",
		provenance=True,
		fwkJobReport=True,
		jsonInput=runsAndLumis(),
		noOut=False,
		histFileName="B_DeepCSV_Efficiency.root",
		histDirName="Efficiency")
p.run()

print "DONE"

