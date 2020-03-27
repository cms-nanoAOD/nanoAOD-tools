#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
from PhysicsTools.NanoAODTools.postprocessing.examples.MCweight_writer import *
from PhysicsTools.NanoAODTools.postprocessing.examples.MET_HLT_Filter import *
from PhysicsTools.NanoAODTools.postprocessing.examples.preselection import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.lepSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *
metCorrector = createJMECorrector(isMC=False, dataYear=2017, jesUncert='All', redojec=True)
fatJetCorrector = createJMECorrector(isMC=False, dataYear=2017, jesUncert='All', redojec=True, jetType = 'AK8PFchs')
p=PostProcessor('.', inputFiles(), 'Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter  && (HLT_PFHT780 || HLT_PFHT890 || HLT_Ele115_CaloIdVT_GsfTrkIdT)', modules=[metCorrector(), fatJetCorrector(), preselection()], provenance=True, fwkJobReport=True, jsonInput=runsAndLumis(), haddFileName='tree_hadd.root', outputbranchsel='keep_and_drop.txt')
p.run()
print 'DONE'
