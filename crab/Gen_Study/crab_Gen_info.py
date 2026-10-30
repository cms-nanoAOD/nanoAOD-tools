#!/usr/bin/env python3
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from Gen_info import *


treecut=" Entry$<10 "
inputFiles=["/grid_mnt/t3storage3/mikumar/Run2/SIXTEEN/minitree/Mc/2J1T1/final/Minitree_Tchannel_2J1T1_mu.root"]

p=PostProcessor(".",
		inputFiles,
		treecut,
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

