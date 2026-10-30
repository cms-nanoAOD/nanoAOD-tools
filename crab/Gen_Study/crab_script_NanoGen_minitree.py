#!/usr/bin/env python3
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
#import main module
from Gen_mass_reconstract_SingleTop_minitree import *
treecut = "top_mass_gen>=0 && top_mass_gen_reco>=0"
#nJet>0 && Jet_pt>20 && (Sum$(Muon_pt>20)>0 || Sum$(Electron_pt>30)>0)" #&& Entry$<10000"#(nMuon>0 || nElectron>0)" # && (Muon_pt>5 || Electron_pt>10) (nMuon>0 || nElectron>0)"
inputFiles=["root://cms-xrd-global.cern.ch//store/user/mikumar/RUN2_UL/Tree_crab/SIXTEEN/MC_NaNOGEN/Tbarchannel_wtop0p85/ST_t-channel_antitop_4f_InclusiveDecays_wtop0p85_TuneCP5_fixWidth_13TeV-powheg-madspin-pythia8/Tree_25_Jul22_MCUL2016_Tbarchannel_wtop0p85/220725_072653/0000/tree_10.root"]

p=PostProcessor( ".",
        inputFiles,
        treecut,
	    modules=[NanoGenConstr_UL2016()],
        #outputbranchsel="clean_All_keep_GenPart.txt",
        provenance=True,
        fwkJobReport=True,
        jsonInput=runsAndLumis())
 
p.run()

print("DONE")
