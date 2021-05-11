#!/usr/bin/env python

ifilename=["/store/mc/RunIIFall18NanoAODv7/ZToEE_NNPDF31_13TeV-powheg_M_50_120/NANOAODSIM/PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/130000/B4302862-17BE-E443-A203-C1B4F2C91829.root"]
ifilename=['164B861F-2B9B-794E-844A-761C4B0B7F97.root']
sourceprefix="root://cms-xrd-global.cern.ch/"
sourceprefix="./"
ifname = ["{}{}".format(sourceprefix, fname) for fname in ifilename]


import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *

from PhysicsTools.NanoAODTools.postprocessing.bff.bffPreselModule import bffPreselProducer
from PhysicsTools.NanoAODTools.postprocessing.examples.exampleModule import exampleModuleConstr

p = PostProcessor(".",
                  ifname,
                  maxEntries=100, 
                  modules=[exampleModuleConstr()],
                  provenance=True,
                  fwkJobReport=True,
                  )
p.run()

print("DONE")
#note: lepSF has to go before puWeight due to the lepton weight constructor redefining the weight constructor
