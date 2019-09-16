#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from  PhysicsTools.NanoAODTools.postprocessing.examples.vbfhmmSkim import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.lepSFProducer_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *




p=PostProcessor(".",inputFiles(), "Jet_pt>15 && Muon_pt > 9", modules=[jetmetUncertainties2017All(), btagSF2017(), muonScaleRes2017(), PrefCorr2017(), puAutoWeight_2017(), lepSFTrig2017(), lepSFID2017(), lepSFISO2017(),vbfhmmModule2017()], provenance=True,fwkJobReport=True,jsonInput=runsAndLumis()) 


#p=PostProcessor(".",inputFiles(), "Jet_pt>15 && Muon_pt > 9", modules=[muonScaleRes2017(), vbfhmmModuleDATA()], provenance=True,fwkJobReport=True,jsonInput=runsAndLumis()) 


p.run()

print "DONE"
os.system("ls -lR")

