#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
from PhysicsTools.NanoAODTools.postprocessing.bff.bffPreselModule import bffPreselProducer 
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import createJMECorrector

ifilename=["/store/mc/RunIIFall18NanoAODv7/ZToEE_NNPDF31_13TeV-powheg_M_50_120/NANOAODSIM/PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/130000/B4302862-17BE-E443-A203-C1B4F2C91829.root"]
ifilename=['164B861F-2B9B-794E-844A-761C4B0B7F97.root']
sourceprefix="root://cms-xrd-global.cern.ch/"
sourceprefix="./"
ifname = ["{}{}".format(sourceprefix, fname) for fname in ifilename]
isMC = True
dataYear = "2017"
runPeriod = ""

jmeCorrections = createJMECorrector(
    isMC=isMC, 
    dataYear=dataYear, 
    runPeriod=runPeriod,
    jesUncert="Total", 
    applySmearing=True,
    jetType="AK4PFchs",
    noGroom=False)

p = PostProcessor(".",
                  ifname,
                  maxEntries=1000, 
                  modules=[jmeCorrections(),bffPreselProducer(int(dataYear))],
                  provenance=True,
                  fwkJobReport=True,
                  )
p.run()

print("DONE")
#note: lepSF has to go before puWeight due to the lepton weight constructor redefining the weight constructor
#-I PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule countHistogramsProducer \
#-I PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer btagSF$era \
#-I PhysicsTools.NanoAODTools.postprocessing.modules.common.lepSFProducer lepSF$era$subera \
#-I PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer puWeight_$era \
#-I PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer muonScaleRes$era \
#-I PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 jmeCorrections"$era"MC \
#-I PhysicsTools.NanoAODTools.postprocessing.bff.bffPreselModule bffPreselModuleConstr$era \
#-b ${NANOAODTOOLS_BASE}/scripts/keep_and_drop_bff.txt $outdirbase/$outdirname $sourceprefix/$ifilename
