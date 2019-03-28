#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

#from  PhysicsTools.NanoAODTools.postprocessing.examples.exampleModule import *
from PhysicsTools.NanoAODTools.analysis.Producer import producer
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import puWeight

preselection="( (Muon_pt[0]>5 && Muon_mediumId[0]>0) || (Electron_pt[0]>15 && Electron_cutBased[0]>0) ) || ( (Muon_pt[0]>5 && Muon_mediumId[0]>0) && (Electron_pt[0]>15 && Electron_cutBased[0]>0) )"
bIn="../scripts/keep_and_drop_Input.txt"
bOut="../scripts/keep_and_drop_Output.txt"
Nevent=-1

p=PostProcessor( "." , inputFiles() , cut=preselection , branchsel=bIn , modules=[ puWeight(), producer() ] , maxevent=Nevent , provenance=True , fwkJobReport=True , jsonInput=runsAndLumis() , outputbranchsel=bOut )
p.run()

print "DONE"
os.system("ls -lR")

