#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

#Module
from PhysicsTools.NanoAODTools.analysis.Producer import producer
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import puWeight

preselection="( (Muon_pt[0]>5 && Muon_mediumId[0]>0) || (Electron_pt[0]>15 && Electron_cutBased[0]>0) ) || ( (Muon_pt[0]>5 && Muon_mediumId[0]>0) && (Electron_pt[0]>15 && Electron_cutBased[0]>0) )"
bIn="keep_and_drop_Input.txt"
bOut="keep_and_drop_Output.txt"
Nevent=-1

p=PostProcessor( "." , inputFiles() , cut=preselection , branchsel=bIn , modules=[ puWeight(), producer() ] , maxevent=Nevent , provenance=True , fwkJobReport=True , jsonInput=runsAndLumis() , outputbranchsel=bOut )
p.run()

print "DONE"
os.system("ls -lR")

