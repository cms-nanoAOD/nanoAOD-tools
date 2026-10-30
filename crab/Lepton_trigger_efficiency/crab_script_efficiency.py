#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from EfficiencyModule import *


treecut="Sum$(Electron_cutBased==4)==1 && Sum$(Electron_cutBased<3)==0 && Sum$(Jet_pt > 40 && abs(Jet_eta)<4.7)>=2 && HLT_IsoMu27==1 && HLT_Ele35_WPTight_Gsf==1"
inputFiles=["root://se01.indiacms.res.in//store/user/mikumar/RUN2_UL/Tree_crab/SEVENTEEN_new/MC/ttbar_FullyLeptonic/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/Tree_15_Jul22_MCUL2017_ttbar_FullyLeptonic/220715_133732/0000/tree_60.root"]
p=PostProcessor(".",
		inputFiles,
		treecut,  #efficecncy histogram there should be no cut
		modules=[EfficiencyConstr_UL2017()],
		outputbranchsel="clean.txt",
		provenance=True,
		fwkJobReport=True,
		jsonInput=runsAndLumis(),
		noOut=False,
		histFileName="Ele_trigger_hist.root",
		histDirName="Events_2D_hist")
p.run()

print "DONE"

