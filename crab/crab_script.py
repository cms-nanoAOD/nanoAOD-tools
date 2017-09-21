#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles
crabFiles=inputFiles()
#FIXME: add lumiToProcess

from  PhysicsTools.NanoAODTools.postprocessing.examples.mhtProducer import *
p=PostProcessor(".",crabFiles,"Jet_pt>200",modules=[mht()],provenance=True,fwkJobReport=True)
p.run()

print "DONE"
os.system("ls -lR")

