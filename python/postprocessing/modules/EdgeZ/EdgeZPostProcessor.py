#!/usr/bin/env python
import os
import sys
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

### SKIM 
cut = ''

### SLIM FILE
slimfile = "SlimFile.txt"

from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.EdgeZ.skimNRecoLeps import *
isData = sys.argv[-1] == 'data'
mod = [puAutoWeight(), skimRecoLeps()]
#mod = [puAutoWeight(),jetmetUncertainties2017All(), skimRecoLeps()]
if isData: mod = [skimRecoLeps()]

POSTPROCESSOR=PostProcessor(".",inputFiles(),cut,slimfile,mod,provenance=True,fwkJobReport=True,jsonInput=runsAndLumis())

