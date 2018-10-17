#!/usr/bin/env python
import os
import sys
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

# get the options
from PhysicsTools.NanoAODTools.python.postprocessing.framework.crabhelper import getCrabOption
doData=getCrabOption("doData",False)


### SKIM 
cut = ''

### SLIM FILE
slimfile = "SlimFile.txt"

from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.EdgeZ.skimNRecoLeps import *
mod = [puAutoWeight(), skimRecoLeps()]
if doData: mod = [skimRecoLeps()]

POSTPROCESSOR=PostProcessor(".",inputFiles(),cut,slimfile,mod,provenance=True,fwkJobReport=True,jsonInput=runsAndLumis())

from PhysicsTools.NanoAODTools.postprocessing.datasets.mc2017    import samples as mcSamples
from PhysicsTools.NanoAODTools.postprocessing.datasets.data2017  import samples as dataSamples

selectedSamples=SAMPLES
if doData:
    jsonFile='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Final/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'
else: 
    jsonFile=None


if __name__ == "__main__":
    POSTPROCESSOR.run()
