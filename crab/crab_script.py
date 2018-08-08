#!/usr/bin/env python
import os
import sys
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

### SKIM 
#cut = 'Jet_pt > 200 && (nElectron + nMuon) >= 2 && nGenDressedLepton >= 2'
cut = '(nElectron + nMuon) >= 2'

### SLIM FILE
slimfile = "SlimFile.txt"

from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.skimNRecoLeps import *
isData = sys.argv[-1] == 'data'
mod = [puAutoWeight(), skimRecoLeps()]
#mod = [puAutoWeight(),jetmetUncertainties2017All(), skimRecoLeps()]
if isData: mod = [skimRecoLeps()]

p=PostProcessor(".",inputFiles(),cut,slimfile,mod,provenance=True,fwkJobReport=True,jsonInput=runsAndLumis())
p.run()

print "DONE"
os.system("ls -lR")
