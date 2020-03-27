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

metCorrector = createJMECorrector(isMC=True, dataYear=2016, jesUncert='All', redojec=True)
fatJetCorrector = createJMECorrector(isMC=True, dataYear=2016, jesUncert='All', redojec=True, jetType = 'AK8PFchs')

p = PostProcessor('.', ['root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAODv6/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/270000/B8DF881B-B8F5-7540-863A-C2DF5E5B1CC8.root'], '', modules=[MCweight_writer(), MET_HLT_Filter_2017(), lepSF_2017(), btagSF2016() ], outputbranchsel=os.path.abspath('../python/postprocessing/examples/keep_and_drop.txt'), histFileName="histOut.root",histDirName="plots", provenance=True, maxEntries=100, fwkJobReport=True)#
p.run()
print 'DONE'
#, Prefcorr(), metCorrector(), fatJetCorrector()
