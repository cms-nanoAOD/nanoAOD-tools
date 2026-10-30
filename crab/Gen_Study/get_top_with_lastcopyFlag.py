#!/usr/bin/env python3
import os, sys
import ROOT 
import numpy as np
import math
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from Gen_mass_functions import *
class NanoGenModule(Module):
    def __init__(self,datayear):
	self.writeHistFile=True
	self.datayear = datayear
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("ntop","I")
        self.out.branch("gen_mtop","F")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
	Genparts = Collection(event,"GenPart")
        #GenJets = Collection(event,"GenJet")
        #GenDressedLeptons = Collection(event,"GenDressedLepton")
	top_with_flag_lastcopy = []

        genpartID = -1
	for genpart in Genparts:
            if(abs(genpart.pdgId)==6 and isflagTrue(Binary_flags(genpart.statusFlags),"isLastCopy")):
	 	#print abs(motherPDG)," --> ",   
	 	top_with_flag_lastcopy.append(genpart.pdgId)
                mtop = genpart.mass

        self.out.fillBranch("ntop",len(top_with_flag_lastcopy))
	self.out.fillBranch("mtop",mtop)    
	#print("----------------------------------")
             #return True
        return True

NanoGenConstr_top_lastCopy = lambda : NanoGenModule('UL2016')

#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
#import main module
#treecut = "top_mass_gen>=0 && top_mass_gen_reco>=0"

inputFiles=["/grid_mnt/t3storage3/mikumar/UL_Run2/SEVENTEEN/minitree/Mc/2J1T1/Minitree_Tbarchannel_2J1T1_mu.root","/grid_mnt/t3storage3/mikumar/UL_Run2/SEVENTEEN/minitree/Mc/2J1T1/Minitree_Tchannel_2J1T1_mu.root","/grid_mnt/t3storage3/mikumar/UL_Run2/SEVENTEEN/minitree/Mc/2J1T1/Minitree_Tbarchannel_2J1T1_el.root","/grid_mnt/t3storage3/mikumar/UL_Run2/SEVENTEEN/minitree/Mc/2J1T1/Minitree_Tchannel_2J1T1_el.root"]

p=PostProcessor( ".",
        inputFiles,
        #treecut,
        modules=[NanoGenConstr_top_lastCopy()],
        #outputbranchsel="clean_All_keep_GenPart.txt",
        provenance=True,
        fwkJobReport=True,
        jsonInput=runsAndLumis())

p.run()

print("DONE")

