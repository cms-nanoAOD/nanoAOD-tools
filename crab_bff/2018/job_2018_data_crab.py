#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
from PhysicsTools.NanoAODTools.postprocessing.trigger.triggerFilter import triggerFilter
from PhysicsTools.NanoAODTools.postprocessing.bff.bffPreselModule import bffPreselProducer 
from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import countHistogramsProducer 
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import muonScaleRes2018 
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles, runsAndLumis

#ifilename=["/store/mc/RunIIFall18NanoAODv7/ZToEE_NNPDF31_13TeV-powheg_M_50_120/NANOAODSIM/PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/130000/B4302862-17BE-E443-A203-C1B4F2C91829.root"]
#ifilename=['164B861F-2B9B-794E-844A-761C4B0B7F97.root']
#sourceprefix="root://cms-xrd-global.cern.ch/"
#sourceprefix="./"
#ifname = ["{}{}".format(sourceprefix, fname) for fname in ifilename]
#isMC = True
dataYear = "2018"
#runPeriod = ""

triggers= ['HLT_Mu50','HLT_OldMu100','HLT_TkMu100', 'HLT_DoubleEle25_CaloIdL_MW'] 

keep_and_drop = 'keep_and_drop_bff.txt'

modules=[
    countHistogramsProducer(),
    triggerFilter(triggers),
    muonScaleRes2018(),
    bffPreselProducer(int(dataYear))
    ]

p = PostProcessor(".",
                  inputFiles(),
                  modules=modules,
                  provenance=True,
                  fwkJobReport=True,
                  outputbranchsel=keep_and_drop,
                  jsonInput=runsAndLumis()
                  )
p.run()

print("DONE")
#note: lepSF has to go before puWeight due to the lepton weight constructor redefining the weight constructor
#-I PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer btagSF$era \
