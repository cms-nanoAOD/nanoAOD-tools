#!/usr/bin/env python3
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
#import main module
from Gen_mass_reconstract_SingleTop import *
from Gen_mass_reconstract_ttbar import *

#treecut = "Entry$<1000"
treecut = "nGenDressedLepton>0 && nGenJet>0" # && Entry$<200"
#nJet>0 && Jet_pt>20 && (Sum$(Muon_pt>20)>0 || Sum$(Electron_pt>30)>0)" #&& Entry$<10000"#(nMuon>0 || nElectron>0)" # && (Muon_pt>5 || Electron_pt>10) (nMuon>0 || nElectron>0)"
#inputFiles=["16815E77-B19A-E94C-805A-FACF666F3D04.root"]
#inputFiles=[ "/home/mikumar/t3store3/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/Gen_Study/NANOGEN_file_wtop1p0.root"] 
#inputFiles=[ "72DF6C8D-6A14-C745-A924-8CBFB1C3592A.root"]
p=PostProcessor( ".",
        inputFiles(),
        treecut,
	modules=[NanoGenConstr_UL2016_Alt_mass()],
        outputbranchsel="clean_All_keep_GenPart.txt",
        provenance=True,
        fwkJobReport=True,
        jsonInput=runsAndLumis())
 
p.run()

print("DONE")
