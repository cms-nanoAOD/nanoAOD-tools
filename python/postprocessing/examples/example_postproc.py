#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from  vbfhmmSkim import *
#from  exampleModule import *
#from  exampleModuleDATA import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jecUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.JetReCalibrator import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetRecalib import *
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *

from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer_old_not_Suvankar import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.hepmcDump import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.lepSFProducer_v2 import *


#p=PostProcessor(".",["/afs/cern.ch/user/g/gimandor/private/Hmumu/nanoAODtest/CMSSW_9_4_6/GluGlu_HToMuMu_M125_13TeV_powheg_pythia8_NANOAOD.root"],"Jet_pt>20 && Muon_pt > 9 && Entry$ < 10000","keep_and_drop.txt",[hepmcDump(),jetmetUncertainties2016(), btagSF2016(), muonScaleRes2016(), puAutoWeight(), exampleModule()],provenance=True)
#p=PostProcessor(".",["/afs/cern.ch/user/g/gimandor/private/Hmumu/nanoAODtest/CMSSW_9_4_6/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8_NANOAOD.root"],"Jet_pt>20 && Muon_pt > 9 && Entry$ < 10000","keep_and_drop.txt",[hepmcDump(),jetmetUncertainties2016(), btagSF2016(), muonScaleRes2016(), puAutoWeight(), exampleModule()],provenance=True)

#p=PostProcessor(".",["/afs/cern.ch/user/g/gimandor/private/Hmumu/nanoAODtest/CMSSW_9_4_6/SingleMuon_NANOAOD.root"],"Jet_pt>20 && Muon_pt > 9 && Entry$ < 10000","keep_and_drop.txt",[exampleModuleDATA()],provenance=True)
#p=PostProcessor(".",["root://xrootd-cms.infn.it//store/data/Run2017F/SingleMuon/NANOAOD/31Mar2018-v1/10000/80641B83-4D45-E811-9DAA-FA163E7EEF99.root"],"Jet_pt>20 && Muon_pt > 9","keep_and_drop.txt",[exampleModuleDATA()],provenance=True)

#p=PostProcessor(".",["root://xrootd-cms.infn.it//store/mc/RunIISummer16NanoAOD/VBF_HToMuMu_M125_13TeV_powheg_pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/00000/C26667F7-7216-E811-8ADD-B496910A9A24.root"],"Jet_pt>5 && Muon_pt >1","keep_and_drop.txt",[exampleModule()],provenance=True)

#p=PostProcessor(".",["root://xrootd-cms.infn.it//store/mc/RunIISummer16NanoAOD/VBF_HToMuMu_M125_13TeV_powheg_pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/00000/C26667F7-7216-E811-8ADD-B496910A9A24.root"], "Jet_pt>15 && Muon_pt > 9 && Entry$ < 10000", "keep_and_drop.txt",[hepmcDump(),jetmetUncertainties2016(), btagSF2016(), muonScaleRes2016(), puAutoWeight(), exampleModule()],provenance=True)


#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/user/arizzi/nano80XDeepAndRegMulti/VBF_HToMuMu_M125_13TeV_powheg_pythia8/RunIIMoriond17-DeepAndReg_M2_2016_TrancheIV_v6-v1/180904_090509/0000/test_data_80X_NANO_1.root"],"Jet_pt>15 && Muon_pt > 9","keep_and_drop.txt",[hepmcDump(),jetmetUncertainties2016(), btagSF2016(), muonScaleRes2016(), puAutoWeight(), exampleModule()],provenance=True)
#p=PostProcessor(".",["/afs/cern.ch/user/g/gimandor/private/Hmumu/nanoAODtest/CMSSW_9_4_6/test80X_NANO_1_TTJets_DiLept.root"],"Entry$ < 10000","keep_and_drop.txt",[hepmcDump(),jetmetUncertainties2016(), btagSF2016(), muonScaleRes2016(), puAutoWeight(), exampleModule()],provenance=True)
#p=PostProcessor(".",["/afs/cern.ch/user/g/gimandor/private/Hmumu/nanoAODtest/CMSSW_9_4_6/test80X_NANO_2.root"],"Jet_pt>25 && Muon_pt > 9 && Entry$ < 10000",modules=[hepmcDump(),jetmetUncertainties2016(), btagSF2016(), muonScaleRes2016(), puAutoWeight(), exampleModule()],provenance=True)

#p=PostProcessor(".",["/afs/cern.ch/user/g/gimandor/private/Hmumu/nanoAODtest/CMSSW_9_4_6/test80X_NANO_1_TTTo2L2Nu.root"],"Entry$ < 1000","keep_and_drop.txt",[hepmcDump(),jetmetUncertainties2017(), btagSF2017(), muonScaleRes2017(), puAutoWeight(), exampleModule()],provenance=True)
#p=PostProcessor(".",["/afs/cern.ch/user/g/gimandor/private/Hmumu/nanoAODtest/CMSSW_9_4_6/EA2B7FA6-0032-7C47-A078-A7E3DD8003D6.root"],"Entry$ < 1000","keep_and_drop.txt",[hepmcDump(),jetmetUncertainties2017(), btagSF2017(), muonScaleRes2017(), puAutoWeight(), exampleModule()],provenance=True)
#p=PostProcessor(".",["/afs/cern.ch/user/g/gimandor/private/Hmumu/nanoAODtest/CMSSW_9_4_6/test80X_ttHToMuMu_NANO2018.root"],"Entry$ < 1000","keep_and_drop.txt",[hepmcDump(),jetmetUncertainties2018(), btagSF2018(), muonScaleRes2017(), puAutoWeight(), exampleModule()],provenance=True)
#p=PostProcessor(".",["root://xrootd-cms.infn.it//store/mc/RunIIAutumn18NanoAODv4/ZH_HToMuMu_ZToAll_M125_TuneCP5_PSweights_13TeV_powheg_pythia8/NANOAODSIM/Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/110000/5881DF01-6B82-DC40-82BD-A20F13961CB7.root"],"Jet_pt>25 && Muon_pt > 9",modules=[hepmcDump(),jetmetUncertainties2018(), btagSF2018(), puAutoWeight(), exampleModule()],provenance=True)


#p=PostProcessor(".",["/afs/cern.ch/user/g/gimandor/private/Hmumu/nanoAODtest/CMSSW_9_4_6/5881DF01-6B82-DC40-82BD-A20F13961CB7.root"],"Jet_pt>25 && Muon_pt > 9 && Entry$ < 1000",modules=[jetmetUncertainties2018(), btagSF2018(), muonScaleRes2016(), puAutoWeight2016(), exampleModule()],provenance=True)
#p=PostProcessor(".",["/afs/cern.ch/user/g/gimandor/private/Hmumu/nanoAODtest/CMSSW_9_4_6/5881DF01-6B82-DC40-82BD-A20F13961CB7.root"],"Jet_pt>25 && Muon_pt > 9 && Entry$ < 1000",modules=[jetmetUncertainties2018(), btagSF2018(), muonScaleRes2016(), puAutoWeight2016(), lepSFTrig2016_B(), lepSFID2016_B(), lepSFISO2016_B(), lepSFTrig2016_H(), lepSFID2016_H(), lepSFISO2016_H(), exampleModule()],provenance=True)
#p=PostProcessor(".",["/afs/cern.ch/user/g/gimandor/private/Hmumu/nanoAODtest/CMSSW_9_4_6/5881DF01-6B82-DC40-82BD-A20F13961CB7.root"],"Jet_pt>25 && Muon_pt > 9 && Entry$ < 1000",modules=[jetmetUncertainties2018(), btagSF2018(), muonScaleRes2016(), puAutoWeight2016(), lepSFTrig2017(), lepSFID2017(), lepSFISO2017(), exampleModule()],provenance=True)
#p=PostProcessor(".",["/afs/cern.ch/user/g/gimandor/private/Hmumu/nanoAODtest/CMSSW_9_4_6/5881DF01-6B82-DC40-82BD-A20F13961CB7.root"],"Jet_pt>25 && Muon_pt > 9 && Entry$ < 1000",modules=[jetmetUncertainties2018(), btagSF2018(), muonScaleRes2018(), puAutoWeight2018(), lepSFTrig2018(), lepSFID2018(), lepSFISO2018(), exampleModule()],provenance=True)

#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv5/GluGluHToMuMu_M-125_TuneCP5_PSweights_13TeV_powheg_pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/120000/E51EBF0C-BF32-A74E-BAF6-390BAC3CFFDC.root"],"Jet_pt>25 && Muon_pt > 9 && Entry$ < 1000",modules=[jetmetUncertainties2018AK4PuppiAll(), btagSF2018(), muonScaleRes2018(), puWeight_2018(), lepSFTrig2018(), lepSFID2018(), lepSFISO2018(), vbfhmmModule2018()],provenance=True)

#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAODv5/GluGluHToMuMu_M125_TuneCP5_PSweights_13TeV_amcatnloFXFX_pythia8/NANOAODSIM/PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/60000/C8F6A654-D0BC-1A41-A375-6836E9A6D580.root"],"Jet_pt>25 && Muon_pt > 9 && Entry$ < 100",modules=[jetmetUncertainties2017AK4PuppiAll(), btagSF2017(), muonScaleRes2017(), PrefCorr2017(), puWeight_2017(), lepSFTrig2017(), lepSFID2017(), lepSFISO2017(), vbfhmmModule2017()],provenance=True)


#p=PostProcessor(".",["/afs/cern.ch/user/g/gimandor/public/Hmumu/nanoAODtest/CMSSW_9_4_6/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8_nanoV5_2017.root"],"Jet_pt>25 && Muon_pt > 9 && Entry$ < 10000",modules=[jetmetUncertainties2017All(), btagSF2017(), muonScaleRes2017(), PrefCorr2017(), puAutoWeight_2017(), lepSFTrig2017(), lepSFID2017(), lepSFISO2017(), vbfhmmModule2017()],provenance=True)


#p=PostProcessor(".",["/afs/cern.ch/user/g/gimandor/private/Hmumu/nanoAODtest/CMSSW_9_4_6/WWTo2L2Nu_DoubleScattering_2017_part1_nanoV4.root"],"Jet_pt>25 && Muon_pt > 9 && Entry$ < 100000",modules=[jetmetUncertainties2017All(), btagSF2017(), muonScaleRes2017(), PrefCorr2017(), puWeight_2017(), lepSFTrig2017(), lepSFID2017(), lepSFISO2017(), vbfhmmModule2017()],provenance=True)
p=PostProcessor(".",["/afs/cern.ch/user/g/gimandor/public/Hmumu/nanoAODtest/CMSSW_9_4_6/WWTo2L2Nu_DoubleScattering_2017_nanoV5.root"],"Jet_pt>25 && Muon_pt > 9 && Entry$ < 100000",modules=[jetmetUncertainties2017All(), btagSF2017(), muonScaleRes2017(), PrefCorr2017(), puWeight_2017(), lepSFTrig2017(), lepSFID2017(), lepSFISO2017(), vbfhmmModule2017()],provenance=True)


#p=PostProcessor(".",["/afs/cern.ch/user/g/gimandor/public/Hmumu/nanoAODtest/CMSSW_9_4_6/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8_nanoV5_2017.root"],"Jet_pt>25 && Muon_pt > 9 && Entry$ < 10000",modules=[jetmetUncertainties2017AK4PuppiAll(), btagSF2017(), muonScaleRes2017(), PrefCorr2017(), puAutoWeight_2017(), lepSFTrig2017(), lepSFID2017(), lepSFISO2017(), vbfhmmModule2017()],provenance=True)
#p=PostProcessor(".",["/afs/cern.ch/user/g/gimandor/public/Hmumu/nanoAODtest/CMSSW_9_4_6/EWK_LLJJ_MLL-50_MJJ-120_TuneCH3_PSweights_13TeV-madgraph-herwig7_nanoV4_2017.root"],"Jet_pt>25 && Muon_pt > 9",modules=[jetmetUncertainties2017AK4PuppiAll(), btagSF2017(), muonScaleRes2017(), PrefCorr2017(), puAutoWeight_2017(), lepSFTrig2017(), lepSFID2017(), lepSFISO2017(), vbfhmmModule2017()],provenance=True)


#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv5/EWK_LLJJ_MLL_105-160_SM_5f_LO_TuneEEC5_13TeV-madgraph-herwigpp/NANOAODSIM/PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/270000/82662C7A-AA05-F044-B258-E17987D59463.root"],"Jet_pt>25 && Muon_pt > 9 && Entry$ < 1000",modules=[jetmetUncertainties2016AK4PuppiAll(), btagSF2016(), muonScaleRes2016(), PrefCorr2016(), puAutoWeight_2016(), lepSFTrig2016_B(), lepSFID2016_B(), lepSFISO2016_B(), lepSFTrig2016_H(), lepSFID2016_H(), lepSFISO2016_H(), vbfhmmModule2016()],provenance=True)
#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv5/EWK_LLJJ_MLL_105-160_SM_5f_LO_TuneCH3_13TeV-madgraph-herwig7/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/40000/26E358BC-11A2-9546-BC3C-FF9E81298879.root"],"Jet_pt>25 && Muon_pt > 9 && Entry$ < 1000",modules=[jetmetUncertainties2018AK4PuppiAll(), btagSF2018(), muonScaleRes2018(), puAutoWeight_2018(), lepSFTrig2018(), lepSFID2018(), lepSFISO2018(), vbfhmmModule2018()],provenance=True)





#p=PostProcessor(".",["/afs/cern.ch/user/g/gimandor/private/Hmumu/nanoAODtest/CMSSW_9_4_6/test80X_ttHToMuMu_NANO2018.root"],"Entry$ < 10000 && Jet_pt>15 && Muon_pt > 9", modules=[jetmetUncertainties2018(), btagSF2018(), muonScaleRes2017(), puAutoWeight2017(), lepSFTrig2018(), lepSFID2018(), lepSFISO2018(), exampleModule()], provenance=True)
#p=PostProcessor(".",["/afs/cern.ch/user/g/gimandor/private/Hmumu/nanoAODtest/CMSSW_9_4_6/test80X_TT_NANO2017.root"],"Entry$ < 20000 && Jet_pt>15 && Muon_pt > 9", modules=[jetmetUncertainties2017(), btagSF2017(), muonScaleRes2017(), puAutoWeight2017(), lepSFTrig2017(), lepSFID2017(), lepSFISO2017(), exampleModule()], provenance=True)
#p=PostProcessor(".",["/afs/cern.ch/user/g/gimandor/private/Hmumu/nanoAODtest/CMSSW_9_4_6/test80X_TT_NANO2017.root"],"Entry$ < 1000 && Jet_pt>15 && Muon_pt > 9", modules=[jetmetUncertainties2017(), btagSF2017(), muonScaleRes2017(), puAutoWeight2017(), lepSFTrig2017(), lepSFID2017(), lepSFISO2017(), exampleModule()], provenance=True)
#p=PostProcessor(".",["/afs/cern.ch/user/g/gimandor/private/Hmumu/nanoAODtest/CMSSW_9_4_6/test80X_TT_NANO2017.root"],"Entry$ < 200 && Jet_pt>15 && Muon_pt > 9", modules=[jetmetUncertainties2017(), btagSF2017(), muonScaleRes2017(), puWeight_2017(), lepSFTrig2017(), lepSFID2017(), lepSFISO2017(), exampleModule()], provenance=True)


#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/data/Run2016H/SingleMuon/NANOAOD/Nano14Dec2018-v1/280000/8EA66449-9D0A-DA48-8D63-04836D7984AE.root"],"Jet_pt>20 && Muon_pt > 9", modules=[muonScaleRes2016(), exampleModuleDATA()],provenance=True)
#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAODv4/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6_ext1-v1/90000/FE00E0FC-2BA6-5944-86BD-D273444F6596.root"],"Jet_pt>15 && Muon_pt > 9", modules=[jetmetUncertainties2017(), btagSF2017(), muonScaleRes2017(), puWeight_2017(), lepSFTrig2017(), lepSFID2017(), lepSFISO2017(), exampleModule()], provenance=True)
#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAODv4/DYJetsToLL_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/20000/D90BEEB7-B07A-2948-AABE-0988F9654AFF.root"],"Jet_pt>15 && Muon_pt > 9", modules=[jetmetUncertainties2017(), btagSF2017(), muonScaleRes2017(), puWeight_2017(), lepSFTrig2017(), lepSFID2017(), lepSFISO2017(), exampleModule()], provenance=True)
#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAODv4/DYJetsToLL_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/20000/C1725238-F199-EA41-9989-975899693E5B.root"],"Jet_pt>15 && Muon_pt > 9", modules=[jetmetUncertainties2017(), btagSF2017(), muonScaleRes2017(), puWeight_2017(), lepSFTrig2017(), lepSFID2017(), lepSFISO2017(), exampleModule()], provenance=True)

#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAODv4/DYJetsToLL_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/280000/CC203D3D-5D88-734D-A460-B96B3787F2ED.root"],"Entry$ < 20000 && Jet_pt>15 && Muon_pt > 9", modules=[jetmetUncertainties2017(), btagSF2017(), muonScaleRes2017(), puWeight_2017(), lepSFTrig2017(), lepSFID2017(), lepSFISO2017(),exampleModule()], provenance=True)
#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAODv4/DYJetsToLL_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/280000/CC203D3D-5D88-734D-A460-B96B3787F2ED.root"],"Entry$ < 20000 && Jet_pt>15 && Muon_pt > 9", modules=[jetmetUncertainties2017AK4PuppiAll(), btagSF2017(), PrefCorr2017(), muonScaleRes2017(), puWeight_2017(), lepSFTrig2017(), lepSFID2017(), lepSFISO2017(),vbfhmmModule()], provenance=True)


#p=PostProcessor(".",["/afs/cern.ch/user/g/gimandor/private/Hmumu/nanoAODtest/CMSSW_9_4_6/ST_tW_top_NANO2018.root"],"Entry$ < 2000 && Jet_pt>15 && Muon_pt > 9", modules=[jetmetUncertainties2018AK4PuppiAll(), btagSF2018(), muonScaleRes2018(), puWeight_2018(), lepSFTrig2018(), lepSFID2018(), lepSFISO2018(),vbfhmmModule2018()], provenance=True)
#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAODv4/DYJetsToLL_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/20000/C1725238-F199-EA41-9989-975899693E5B.root"],"Entry$ < 2000 && Jet_pt>15 && Muon_pt > 9", modules=[jetmetUncertainties2017AK4PuppiAll(), btagSF2017(), PrefCorr2017(), muonScaleRes2017(), puWeight_2017(), lepSFTrig2017(), lepSFID2017(), lepSFISO2017(),vbfhmmModule2017()], provenance=True)
#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv4/DYJetsToLL_M-105To160_VBFFilter_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_Nano14Dec2018_VBFPostMGFilter_102X_mcRun2_asymptotic_v6_ext2-v1/120000/58263BA9-93E4-C243-800E-ABFC074E008B.root"],"Entry$ < 2000 && Jet_pt>15 && Muon_pt > 9", modules=[jetmetUncertainties2016AK4PuppiAll(), btagSF2016(), muonScaleRes2016(), PrefCorr2016(), puWeight_2016(), lepSFTrig2016_B(), lepSFID2016_B(), lepSFISO2016_B(), lepSFTrig2016_H(), lepSFID2016_H(), lepSFISO2016_H(), vbfhmmModule2016()], provenance=True)

#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv4/WplusH_HToMuMu_WToAll_M125_TuneCP5_PSweights_13TeV_powheg_pythia8/NANOAODSIM/PUMoriond17_Nano14Dec2018_102X_mcRun2_asymptotic_v6-v1/270000/F3E3786F-F18B-A24E-8F51-E1AD384DBBB0.root"],"Entry$ < 2000 && Jet_pt>15 && Muon_pt > 9", modules=[jetmetUncertainties2016AK4PuppiAll(), btagSF2016(), muonScaleRes2016(), PrefCorr2016(), puWeight_2016(), lepSFTrig2016_B(), lepSFID2016_B(), lepSFISO2016_B(), lepSFTrig2016_H(), lepSFID2016_H(), lepSFISO2016_H(), vbfhmmModule2016()], provenance=True)















#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAOD/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/102X_upgrade2018_realistic_v15-v1/90000/7E197AC3-49C6-D746-AA5F-3FA5AB7584AA.root"],"Entry$ < 20000 && Jet_pt>15 && Muon_pt > 9", modules=[jetmetUncertainties2018(), btagSF2018(), muonScaleRes2018(), puWeight_2018(), lepSFTrig2018(), lepSFID2018(), lepSFISO2018(), exampleModule()], provenance=True)



#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAOD/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/102X_upgrade2018_realistic_v15-v1/90000/7E197AC3-49C6-D746-AA5F-3FA5AB7584AA.root"],"Jet_pt>15 && Muon_pt > 9", modules=[jetmetUncertainties2018(), btagSF2018(), muonScaleRes2018(), puWeight_2018(), lepSFTrig2018(), lepSFID2018(), lepSFISO2018(), exampleModule()], provenance=True)

#p=PostProcessor(".",["root://xrootd-cms.infn.it//store/data/Run2017B/SingleMuon/NANOAOD/Nano1June2019-v1/40000/485877F9-940F-3D44-BB38-5FA05A80AD9C.root"],"Entry$ < 10000 && Jet_pt>15 && Muon_pt > 9", modules=[muonScaleRes2017(), vbfhmmModuleDATA()], provenance=True)
#p=PostProcessor(".",["root://xrootd-cms.infn.it//store/data/Run2018D/SingleMuon/NANOAOD/Nano1June2019-v1/40000/AEDB195D-E412-2648-AD2F-FB69FF4AE99E.root"],"Entry$ < 10000 && Jet_pt>15 && Muon_pt > 9", modules=[muonScaleRes2018(), vbfhmmModuleDATA()], provenance=True)


#p=PostProcessor(".",["root://xrootd-cms.infn.it//store/data/Run2016B/SingleMuon/NANOAOD/05Feb2018_ver2-v1/00000/2055267F-3110-E811-8956-AC1F6B1AEF94.root"],"Entry$ < 1000 && Jet_pt>15 && Muon_pt > 9", modules=[muonScaleRes2018()], provenance=True)
#p=PostProcessor(".",["/afs/cern.ch/user/g/gimandor/private/Hmumu/nanoAODtest/CMSSW_9_4_6/EWK_2017.root"],"Entry$ < 2000 && Jet_pt>15 && Muon_pt > 9", modules=[jetmetUncertainties2017AK4PuppiAll(), btagSF2017(), muonScaleRes2017(), PrefCorr2017(), puWeight_2017(), lepSFTrig2017(), lepSFID2017(), lepSFISO2017(),vbfhmmModule2017()], provenance=True)
#p=PostProcessor(".",["/afs/cern.ch/user/g/gimandor/private/Hmumu/nanoAODtest/CMSSW_9_4_6/SingleMuon2018.root"],"Entry$ < 50000 && Jet_pt>15 && Muon_pt > 9", modules=[jetRecalib2018C(), muonScaleRes2018(),vbfhmmModuleDATA()], provenance=True)


#p=PostProcessor(".",["/afs/cern.ch/user/g/gimandor/private/Hmumu/nanoAODtest/CMSSW_9_4_6/ZH_HToMuMu_ZToAll_M125_TuneCP5_PSweights_13TeV_powheg_pythia8_NANOAODSIM_2018.root"],modules=[hepmcDump(),jetmetUncertainties2018(), btagSF2018(), muonScaleRes2017(), puAutoWeight(), exampleModule()],provenance=True)
#p=PostProcessor(".",["/afs/cern.ch/user/g/gimandor/private/Hmumu/nanoAODtest/CMSSW_9_4_6/test80X_ttHToMuMu_NANO2018.root"],"Entry$ < 10000",modules=[hepmcDump(),jetmetUncertainties2018(), btagSF2018(), muonScaleRes2017(), puAutoWeight(), exampleModule()],provenance=True)

#p=PostProcessor(".",["/afs/cern.ch/user/g/gimandor/private/Hmumu/nanoAODtest/CMSSW_9_4_6/test80X_NANO_1_TTTo2L2Nu.root"],"Entry$ < 10000","keep_and_drop.txt",[jetmetUncertainties2016(), muonScaleRes2016(), exampleModule()],provenance=True)
#p=PostProcessor(".",["/afs/cern.ch/user/g/gimandor/private/Hmumu/nanoAODtest/CMSSW_9_4_6/test80X_NANO_1_TTTo2L2Nu.root"],"Entry$ < 10000","keep_and_drop.txt",[hepmcDump(),jetmetUncertainties2016(), btagSF2016(), muonScaleRes2016(), puAutoWeight(), exampleModule()],provenance=True)


#p=PostProcessor(".",["/afs/cern.ch/user/g/gimandor/private/Hmumu/nanoAODtest/CMSSW_9_4_6/test80X_NANO_20.root"],"Jet_pt>15 && Muon_pt > 9 && Entry$ < 10000","keep_and_drop.txt",[hepmcDump(),jetmetUncertainties2016(), btagSF2016(), muonScaleRes2016(), puAutoWeight(), exampleModule()],provenance=True)


#p=PostProcessor(".",["root://xrootd-cms.infn.it//store/data/Run2016B/SingleMuon/NANOAOD/05Feb2018_ver2-v1/00000/2055267F-3110-E811-8956-AC1F6B1AEF94.root"],"Entry$ < 2000 && Jet_pt>15 && Muon_pt > 9", modules=[muonScaleRes2016(), vbfhmmModuleDATA()], provenance=True)



#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/user/arizzi/nano80XDeepAndReg/SingleMuon/NanoDeepAndReg2016Run2016G-03Feb2017-v1/180516_082336/0000/test_data_80X_NANO_734.root"],"Jet_pt>20 && Muon_pt > 9","keep_and_drop.txt",[exampleModuleDATA()],provenance=True)



# 2016 V85 ext6 
#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/data/Run2016G/SingleMuon/NANOAOD/05Feb2018-v1/20000/EC7C30D1-6C0C-E811-B042-0242AC130002.root"],"Jet_pt>20 && Muon_pt > 9 && Entry$ < 10000","keep_and_drop.txt",[exampleModuleDATA()],provenance=True)

# 2016 V79 ext5 
#p=PostProcessor(".",["root://xrootd-cms.infn.it//store/data/Run2016F/SingleMuon/NANOAOD/05Feb2018-v1/80000/1006BFED-640C-E811-8500-44A84225C827.root"],"Jet_pt>20 && Muon_pt > 9","keep_and_drop.txt",[exampleModuleDATA()],provenance=True)
# 2016 V79 ext2 
#p=PostProcessor(".",["root://xrootd-cms.infn.it//store/data/Run2016C/SingleMuon/NANOAOD/05Feb2018-v1/00000/6CE972C3-500C-E811-B67E-6CC2173D6140.root"],"Jet_pt>20 && Muon_pt > 9","keep_and_drop.txt",[exampleModuleDATA()],provenance=True)

# 2016 V79 all 
#p=PostProcessor(".",["root://xrootd-cms.infn.it//store/data/Run2016F/SingleMuon/NANOAOD/05Feb2018-v1/80000/1006BFED-640C-E811-8500-44A84225C827.root", "root://xrootd-cms.infn.it//store/data/Run2016C/SingleMuon/NANOAOD/05Feb2018-v1/00000/6CE972C3-500C-E811-B67E-6CC2173D6140.root"],"Jet_pt>20 && Muon_pt > 9","keep_and_drop.txt",[exampleModuleDATA()],provenance=True)

# 2016 V79 ext8
#p=PostProcessor(".",["root://xrootd-cms.infn.it//store/data/Run2016G/SingleMuon/NANOAOD/05Feb2018-v1/40000/9EF4B56A-510C-E811-905E-0CC47A4D7636.root", "root://xrootd-cms.infn.it//store/data/Run2016G/SingleMuon/NANOAOD/05Feb2018-v1/40000/B4C781C8-610C-E811-9343-0242AC130002.root", "root://xrootd-cms.infn.it//store/data/Run2016G/SingleMuon/NANOAOD/05Feb2018-v1/40000/CC9FBCB0-5D0C-E811-9601-34E6D7BDDEDB.root"],"Jet_pt>20 && Muon_pt > 9","keep_and_drop.txt",[exampleModuleDATA()],provenance=True)




#p=PostProcessor(".",["../../../../NanoAOD/test/lzma.root"],"Jet_pt>150","keep_and_drop.txt",[exampleModule()],provenance=True)
p.run()
