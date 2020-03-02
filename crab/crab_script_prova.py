#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
from PhysicsTools.NanoAODTools.postprocessing.examples import MCweight_writer, MET_HLT_Filter,preselection
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
metCorrector = createJMECorrector(isMC=True, dataYear=2016, jesUncert='All', redojec=True)
fatJetCorrector = createJMECorrector(isMC=True, dataYear=2016, jesUncert='All', redojec=True, jetType = 'AK8PFchs')
p=PostProcessor('.', , '', modules=[MCweight_writer(), MET_HLT_Filter(), preselection(), '''Prefcorr(), metCorrector(), fatJetCorrector()'''], provenance=True, fwkJobReport=True)
p.run()
print 'DONE'
