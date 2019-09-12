#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from  PhysicsTools.NanoAODTools.postprocessing.examples.vbfhmmSkim import *
#from  PhysicsTools.NanoAODTools.postprocessing.examples.exampleModule import *
#from  PhysicsTools.NanoAODTools.postprocessing.examples.exampleModuleDATA import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.hepmcDump import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.lepSFProducer_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *




#import os
#release=os.environ['CMSSW_VERSION'][6:]
#print("Using release "+release)
#print(os.getcwd())
#print("this is where I am")


#import glob
#glob.glob("../postprocessing/modules/common/*")
#glob.glob("../postprocessing/data/leptonSF/*")

#data = sys.argv[2]
#era = sys.argv[3]

#if data == "MC" :

###p=PostProcessor(".",inputFiles(), "Jet_pt>15 && Muon_pt > 9", modules=[jetmetUncertainties2018AK4PuppiAll(), btagSF2018(), muonScaleRes2018(), puWeight_2018(), lepSFTrig2018(), lepSFID2018(), lepSFISO2018(), vbfhmmModule()], provenance=True,fwkJobReport=True,jsonInput=runsAndLumis()) 
###p=PostProcessor(".",inputFiles(), "Jet_pt>15 && Muon_pt > 9", modules=[jetmetUncertainties2017AK4PuppiAll(), btagSF2017(), muonScaleRes2017(), PrefCorr2017(), puWeight_2017(), lepSFTrig2017(), lepSFID2017(), lepSFISO2017(),vbfhmmModule()], provenance=True,fwkJobReport=True,jsonInput=runsAndLumis()) 
p=PostProcessor(".",inputFiles(), "Jet_pt>15 && Muon_pt > 9", modules=[jetmetUncertainties2016AK4PuppiAll(), btagSF2016(), muonScaleRes2016(), PrefCorr2016(), puAutoWeight_2016(), lepSFTrig2016_B(), lepSFID2016_B(), lepSFISO2016_B(), lepSFTrig2016_H(), lepSFID2016_H(), lepSFISO2016_H(), vbfhmmModule2016()], provenance=True,fwkJobReport=True,jsonInput=runsAndLumis()) 


###p=PostProcessor(".",inputFiles(), "Jet_pt>15 && Muon_pt > 9", modules=[muonScaleRes2018(), vbfhmmModuleDATA()], provenance=True,fwkJobReport=True,jsonInput=runsAndLumis()) 
###p=PostProcessor(".",inputFiles(), "Jet_pt>15 && Muon_pt > 9", modules=[muonScaleRes2017(), vbfhmmModuleDATA()], provenance=True,fwkJobReport=True,jsonInput=runsAndLumis()) 
#p=PostProcessor(".",inputFiles(), "Jet_pt>15 && Muon_pt > 9", modules=[muonScaleRes2016(), vbfhmmModuleDATA()], provenance=True,fwkJobReport=True,jsonInput=runsAndLumis()) 



#p=PostProcessor(".",["root://cmsxrootd.fnal.gov//store/user/arizzi/NanoTest3/VBF_HToMuMu_M125_13TeV_powheg_pythia8/NanoTest3/171103_143903/0000/nanoaod_1.root"], "Jet_pt>20 && Muon_pt > 9", modules=[hepmcDump(),jetmetUncertainties2016(), btagSF2016(), muonScaleRes2016(), puAutoWeight(), exampleModule()], provenance=True,fwkJobReport=True,jsonInput=runsAndLumis()) 
#p=PostProcessor(".",["root://cmsxrootd.fnal.gov//store/user/arizzi/NanoTest3/VBF_HToMuMu_M125_13TeV_powheg_pythia8/NanoTest3/171103_143903/0000/nanoaod_1.root"], "Jet_pt>20 && Muon_pt > 10", modules=[hepmcDump(), jetmetUncertainties2016(), btagSF2016(), muonScaleRes2016(), puAutoWeight(), exampleModule2016()], provenance=True,fwkJobReport=True,jsonInput=runsAndLumis()) 

#p=PostProcessor(".",inputFiles(),"Jet_pt>200",modules=[exampleModule()],provenance=True,fwkJobReport=True,jsonInput=runsAndLumis())
p.run()

print "DONE"
os.system("ls -lR")

