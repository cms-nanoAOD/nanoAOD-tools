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
metCorrector = createJMECorrector(isMC=True, dataYear=2016, jesUncert='All', redojec=True)
fatJetCorrector = createJMECorrector(isMC=True, dataYear=2016, jesUncert='All', redojec=True, jetType = 'AK8PFchs')
p=PostProcessor('.', ['/eos/home-a/adeiorio/Wprime/nosynch/TT_Mtt-1000toInf_2016_1.root'], '', modules=[MCweight_writer(), MET_HLT_Filter(), preselection()], histFileName="histOut.root",histDirName="plots", provenance=True, fwkJobReport=True)
p.run()
print 'DONE'
#, Prefcorr(), metCorrector(), fatJetCorrector()
