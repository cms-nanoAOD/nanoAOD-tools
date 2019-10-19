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

#p=PostProcessor(".",["/home/users/sdonato/scratchssd/WWTo2L2Nu_DoubleScattering_2018_nanoV5.root"],"Jet_pt>25 && Muon_pt > 9 && Entry$ < 10000",modules=[jetmetUncertainties2018All(), btagSF2018(), muonScaleRes2018(), PrefCorr2018(), puWeight_2018(), lepSFTrig2018(), lepSFID2018(), lepSFISO2018(), vbfhmmModule2018()],provenance=True)

#p=PostProcessor(".",["/home/users/sdonato/DYJetsToLL_M-105To160_VBFFilter_TuneCP5_PSweights_13TeV-amcatnloFXFX-pythia8_RunIIAutumn18MiniAOD_VBFPostMGFilter_102X_upgrade2018_realistic_v15-v1_B0B8172B-71D3-1845-BFB5-252F06B8A6A7.root"], "Jet_pt>15 && Muon_pt > 9", modules=[jetmetUncertainties2018All(), btagSF2018(), muonScaleRes2018(), puAutoWeight_2018(), lepSFTrig2018(), lepSFID2018(), lepSFISO2018(), vbfhmmModule2018()], provenance=True,fwkJobReport=True)

p=PostProcessor("tree-data2018D.root",["/home/users/sdonato/scratchssd/Run2018D_SingleMuon_NANOAOD_Nano1June2019-v1_98CBE3D1-4761-F24E-8007-2B2777551D2B.root"], "Jet_pt>15 && Muon_pt > 9 && Entry$ < 1000", modules=[jetRecalib2018D()], provenance=True,fwkJobReport=True)

p.run()
