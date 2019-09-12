#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from  PhysicsTools.NanoAODTools.postprocessing.examples.vbfhmmSkim import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetRecalib import *
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.lepSFProducer_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *






p=PostProcessor(".",inputFiles(), "Jet_pt>15 && Muon_pt > 9", modules=[jetmetUncertainties2018AK4PuppiAll(), btagSF2018(), muonScaleRes2018(), puAutoWeight_2018(), lepSFTrig2018(), lepSFID2018(), lepSFISO2018(), vbfhmmModule2018()], provenance=True,fwkJobReport=True,jsonInput=runsAndLumis()) 

#p=PostProcessor(".",inputFiles(), "Jet_pt>15 && Muon_pt > 9", modules=[jetRecalib2018A(), muonScaleRes2018(), vbfhmmModuleDATA()], provenance=True,fwkJobReport=True,jsonInput=runsAndLumis()) 
#p=PostProcessor(".",inputFiles(), "Jet_pt>15 && Muon_pt > 9", modules=[jetRecalib2018B(), muonScaleRes2018(), vbfhmmModuleDATA()], provenance=True,fwkJobReport=True,jsonInput=runsAndLumis()) 
#p=PostProcessor(".",inputFiles(), "Jet_pt>15 && Muon_pt > 9", modules=[jetRecalib2018C(), muonScaleRes2018(), vbfhmmModuleDATA()], provenance=True,fwkJobReport=True,jsonInput=runsAndLumis()) 
#p=PostProcessor(".",inputFiles(), "Jet_pt>15 && Muon_pt > 9", modules=[jetRecalib2018D(), muonScaleRes2018(), vbfhmmModuleDATA()], provenance=True,fwkJobReport=True,jsonInput=runsAndLumis()) 

p.run()

print "DONE"
os.system("ls -lR")

