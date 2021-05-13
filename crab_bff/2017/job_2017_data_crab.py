#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
from PhysicsTools.NanoAODTools.postprocessing.trigger.triggerFilter import triggerFilter
from PhysicsTools.NanoAODTools.postprocessing.bff.bffPreselModule import bffPreselProducer 
from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import countHistogramsProducer 
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import muonScaleRes2017 
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles, runsAndLumis

isMC = True
dataYear = "2017"
#runPeriod = ""

triggers= ['HLT_Mu50','HLT_OldMu100','HLT_TkMu100', 'HLT_DoubleEle25_CaloIdL_MW'] 

keep_and_drop = 'keep_and_drop_bff.txt'

modules=[
    countHistogramsProducer(),
    triggerFilter(triggers),
    muonScaleRes2017(),
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
