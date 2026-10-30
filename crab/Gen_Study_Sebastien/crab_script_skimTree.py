#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 
#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
#from exampleModule import *
from MainModule import *

treecut = "nJet>0 && Jet_pt>20 && (Sum$(Muon_pt>20)>0 || Sum$(Electron_pt>30)>0)"
treecutEN = "Entry$<100"#(nMuon>0 || nElectron>0)" # && (Muon_pt>5 || Electron_pt>10) (nMuon>0 || nElectron>0)"
#inputFiles=["root://cms-xrd-global.cern.ch//store/data/Run2017B/SingleMuon/NANOAOD/02Apr2020-v1/50000/FBFADBAD-5164-6A4D-A19E-EFF003090EC5.root"]
#inputFiles=["/afs/cern.ch/user/m/mikumar/work/private/NanoAOD_new/CMSSW_10_6_0/src/Inputroot_files/Tree/single_muondata_2016_runD/5A4AA866-8941-334C-A591-7D2728C6F63F.root"]
inputFiles=[
	#"/grid_mnt/t3storage3/mikumar/Run2/SIXTEEN/minitree/Mc/2J1T1/final/Minitree_Tchannel_2J1T1_el.root",
	#"/grid_mnt/t3storage3/mikumar/Run2/SIXTEEN/minitree/Mc/2J1T1/final/Minitree_Tchannel_2J1T1_mu.root",
	#"/grid_mnt/t3storage3/mikumar/Run2/SIXTEEN/minitree/Mc/2J1T1/final/Minitree_Tchannel_mtop1695_2J1T1_el.root",
	#"/grid_mnt/t3storage3/mikumar/Run2/SIXTEEN/minitree/Mc/2J1T1/final/Minitree_Tchannel_mtop1695_2J1T1_mu.root",
	#"/grid_mnt/t3storage3/mikumar/Run2/SIXTEEN/minitree/Mc/2J1T1/final/Minitree_Tchannel_mtop1715_2J1T1_el.root",
	#"/grid_mnt/t3storage3/mikumar/Run2/SIXTEEN/minitree/Mc/2J1T1/final/Minitree_Tchannel_mtop1715_2J1T1_mu.root",
	#"/grid_mnt/t3storage3/mikumar/Run2/SIXTEEN/minitree/Mc/2J1T1/final/Minitree_Tchannel_mtop1735_2J1T1_el.root",
	#"/grid_mnt/t3storage3/mikumar/Run2/SIXTEEN/minitree/Mc/2J1T1/final/Minitree_Tchannel_mtop1735_2J1T1_mu.root",
	"/grid_mnt/t3storage3/mikumar/Run2/SIXTEEN/minitree/Mc/2J1T1/final/Minitree_Tchannel_mtop1755_2J1T1_el.root",
	"/grid_mnt/t3storage3/mikumar/Run2/SIXTEEN/minitree/Mc/2J1T1/final/Minitree_Tchannel_mtop1755_2J1T1_mu.root"	   
]

p=PostProcessor(".",
		inputFiles,
	#	treecutEN,
		modules=[MainModuleConstr_Gen()],
		outputbranchsel="clean.txt",
		provenance=True,
		fwkJobReport=True,
		jsonInput=runsAndLumis())
		
p.run()

print "DONE"
