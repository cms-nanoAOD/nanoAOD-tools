#!/usr/bin/env python
import os,PSet, sys
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


modulesToBeCalled = {
"data2016"    : ["muonScaleRes2016", "vbfhmmModuleDATA"],
"data2017"    : ["muonScaleRes2017", "vbfhmmModuleDATA"],
"data2018A"   : ["jetRecalib2018A", "muonScaleRes2018", "vbfhmmModuleDATA18"],
"data2018B"   : ["jetRecalib2018B", "muonScaleRes2018", "vbfhmmModuleDATA18"],
"data2018C"   : ["jetRecalib2018C", "muonScaleRes2018", "vbfhmmModuleDATA18"],
"data2018D"   : ["jetRecalib2018D", "muonScaleRes2018", "vbfhmmModuleDATA18"],

"mc2016"      : ["jetmetUncertainties2016All", "btagSF2016", "muonScaleRes2016", "PrefCorr2016", "puAutoWeight_2016", "lepSFTrig2016_B", "lepSFID2016_B", "lepSFISO2016_B", "lepSFTrig2016_H", "lepSFID2016_H", "lepSFISO2016_H", "vbfhmmModule2016"],
"mc2017"      : ["jetmetUncertainties2017All", "btagSF2017", "muonScaleRes2017", "PrefCorr2017", "puAutoWeight_2017", "lepSFTrig2017",   "lepSFID2017",   "lepSFISO2017",   "vbfhmmModule2017"],
"mc2018"      : ["jetmetUncertainties2018All", "btagSF2018", "muonScaleRes2018",                 "puAutoWeight_2018", "lepSFTrig2018",   "lepSFID2018",   "lepSFISO2018",   "vbfhmmModule2018"],
}

if len(sys.argv) != 3:
    raise Exception("Launch crab_script_all.py specifying two options: job numbers (eg. 0) and configuration (eg. mc2016). \n\nExample: python crab_script_all.py 0 data2018C\n")

moduleSettings = sys.argv[2]

from checker import checkModulesToBeCalled
checkModulesToBeCalled(modulesToBeCalled)

from checker import checkModuleSettingsFromFileName
checkModuleSettingsFromFileName(PSet.process.source.fileNames[0], moduleSettings)

print "I'm using the configuration %s: %s"%(moduleSettings, modulesToBeCalled[moduleSettings])

modulesCalled = []
for module in modulesToBeCalled[moduleSettings]:
    print "Calling %s"%module
    modulesCalled.append(globals()[module]())
    print

print "Creating PostProcessor"
if moduleSettings != '': postproc = PostProcessor(".",inputFiles(), "Jet_pt>15 && Muon_pt > 9", modules=modulesCalled, provenance=True,fwkJobReport=True,jsonInput=runsAndLumis())
else: print "ERROR: No PostProcessor found for datamc, year, era = %s, %d, %s"%(datamc, year, era)
print

print "Launching PostProcessor"
postproc.run()

print "DONE"
os.system("ls -lR")

