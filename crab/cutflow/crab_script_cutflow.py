#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from cutflowModule import *

#treecut = "Entry$<10000"
treecut = "nGenDressedLepton>0 && nGenJet>0"
p=PostProcessor(".",
		inputFiles(),
		treecut,   #in cutflow there should not be any cut
		modules=[cutflowModuleConstr_2J1T1_mu_mc_UL2016preVFP()],
		outputbranchsel="clean.txt",
		provenance=True,
		fwkJobReport=True,
		jsonInput=runsAndLumis(),
		noOut=False,
		histFileName="Cutflow_hist.root",
		histDirName="histograms")
p.run()

print("DONE")

