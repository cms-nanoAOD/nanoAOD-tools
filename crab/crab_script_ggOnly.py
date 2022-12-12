import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this would take care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from  PhysicsTools.NanoAODTools.postprocessing.examples.exampleModule import *

from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
from  PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import *

from PhysicsTools.NanoAODTools.postprocessing.modules.common.tauCorrProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muSFProducer2 import *

from PhysicsTools.NanoAODTools.postprocessing.modules.common.ggTemporaryScale import *

import sys
print sys.argv
suffix=sys.argv[2].split("=")[1]
analysis=sys.argv[3].split("=")[1]
modulesToRun=[]

selection='''Sum$(Photon_pt > 18 && (Photon_isScEtaEB || Photon_isScEtaEE) && Photon_electronVeto > 0.5 && Photon_hoe < 0.08) > 1'''

#2016 modules MC
PrefireCorr2016 = lambda : PrefCorr("L1prefiring_jetpt_2016BtoH.root", "L1prefiring_jetpt_2016BtoH", "L1prefiring_photonpt_2016BtoH.root", "L1prefiring_photonpt_2016BtoH")

#2017 modules MC
PrefireCorr2017 = lambda : PrefCorr('L1prefiring_jetpt_2017BtoF.root', 'L1prefiring_jetpt_2017BtoF', 'L1prefiring_photonpt_2017BtoF.root', 'L1prefiring_photonpt_2017BtoF')


if suffix=='16a':
  if analysis=="ggtautau":
    modulesToRun=[puAutoWeight_UL2016(), jetmetUncertaintiesAPV2016UL(), jetmetUncertaintiesAPV2016ULAll(), muonScaleRes2016v5ULAPV(), PrefireCorr2016(), tauCorrs2016ULpreVFP(), lepSFID2016_B(), lepSFISO2016_B(), gammaSF_UL16PreVFP()]
  else if analysis=="ggbb"
    modulesToRun=[puAutoWeight_UL2016(), jetmetUncertaintiesAPV2016UL(), jetmetUncertaintiesAPV2016ULAll(), gammaSF_UL16PreVFP()]

  p=PostProcessor(".", 
                  inputFiles(), #NOT IN LOCAL  
                  selection.replace('\n',''),
                  branchsel="keep_and_drop.txt",
                  outputbranchsel="keep_and_drop.txt",
                  modules=modulesToRun,
                  provenance=True,
                  fwkJobReport=True, #NOT IN LOCAL
                  jsonInput=runsAndLumis() #NOT IN LOCAL
                  )

elif suffix=='16b' :
  if analysis=="ggtautau":
    modulesToRun=[puAutoWeight_UL2016(), jetmetUncertainties2016UL(), jetmetUncertainties2016ULAll(), muonScaleRes2016v5UL(), PrefireCorr2016(), tauCorrs2016ULpostVFB(), lepSFID2016_H(), lepSFISO2016_H(), gammaSF_UL16PostVFP()],
  else if analysis=="ggbb"
    modulesToRun=[puAutoWeight_UL2016(), jetmetUncertainties2016UL(), jetmetUncertainties2016ULAll(), gammaSF_UL16PostVFP()],

  p=PostProcessor(".", 
                  inputFiles(), #NOT IN LOCAL      
                  selection.replace('\n',''),
                  branchsel="keep_and_drop.txt",
                  outputbranchsel="keep_and_drop.txt",
                  modules=modulesToRun,
                  provenance=True,
                  fwkJobReport=True, #NOT IN LOCAL
                  jsonInput=runsAndLumis() #NOT IN LOCAL
                  )

elif suffix=='17':
  if analysis=="ggtautau":
    modulesToRun=[puAutoWeight_UL2017(), jetmetUncertainties2017UL(), jetmetUncertainties2017ULAll(), muonScaleRes2017v5UL(), PrefireCorr2017(), tauCorrs2017UL(), lepSFID2017(), lepSFISO2017(), gammaSF_UL17()],
  else if analysis=="ggbb"
    modulesToRun=[puAutoWeight_UL2017(), jetmetUncertainties2017UL(), jetmetUncertainties2017ULAll(), gammaSF_UL17()],

  p=PostProcessor(".", 
                  inputFiles(), #NOT IN LOCAL  
                  selection.replace('\n',''),
                  branchsel="keep_and_drop.txt",
                  outputbranchsel="keep_and_drop.txt",
                  modules=modulesToRun,
                  provenance=True,
                  fwkJobReport=True, #NOT IN LOCAL
                  jsonInput=runsAndLumis() #NOT IN LOCAL
                  )

elif suffix=='18':
  if analysis=="ggtautau":
    modulesToRun=[puAutoWeight_UL2018(), jetmetUncertainties2018UL(), jetmetUncertainties2018ULAll(), muonScaleRes2018v5UL(), tauCorrs2018UL(), lepSFID2018(), lepSFISO2018(), gammaSF_UL18()],
  else if analysis=="ggbb"
    modulesToRun=[puAutoWeight_UL2018(), jetmetUncertainties2018UL(), jetmetUncertainties2018ULAll(), gammaSF_UL18()],

  p=PostProcessor(".", 
                  inputFiles(), #NOT IN LOCAL  
                  selection.replace('\n',''),
                  branchsel="keep_and_drop.txt",
                  outputbranchsel="keep_and_drop.txt",
                  modules=modulesToRun,
                  provenance=True, 
                  fwkJobReport=True, #NOT IN LOCAL
                  jsonInput=runsAndLumis() #NOT IN LOCAL
                  )

elif suffix=='16aD':
  if analysis=="ggtautau":
    modulesToRun=[muonScaleRes2016v5ULAPV()],
  else if analysis=="ggbb"
    modulesToRun=[],

  p=PostProcessor(".",
                  inputFiles(), #NOT IN LOCAL  
                  selection.replace('\n',''),
                  branchsel="keep_and_drop.txt",
                  outputbranchsel="keep_and_drop.txt",
                  modules=modulesToRun,
                  provenance=True,
                  fwkJobReport=True, #NOT IN LOCAL
                  jsonInput=runsAndLumis() #NOT IN LOCAL
                  )

elif suffix=='16bD' :
  if analysis=="ggtautau":
    modulesToRun=[muonScaleRes2016v5UL()],
  else if analysis=="ggbb"
    modulesToRun=[],

  p=PostProcessor(".",
                  inputFiles(), #NOT IN LOCAL      
                  selection.replace('\n',''),
                  branchsel="keep_and_drop.txt",
                  outputbranchsel="keep_and_drop.txt",
                  modules=modulesToRun,
                  provenance=True,
                  fwkJobReport=True, #NOT IN LOCAL
                  jsonInput=runsAndLumis() #NOT IN LOCAL
                  )

elif suffix=='17D':
  if analysis=="ggtautau":
    modulesToRun=[muonScaleRes2017v5UL()],
  else if analysis=="ggbb"
    modulesToRun=[],

  p=PostProcessor(".",
                  inputFiles(), #NOT IN LOCAL  
                  selection.replace('\n',''),
                  branchsel="keep_and_drop.txt",
                  outputbranchsel="keep_and_drop.txt",
                  modules=modulesToRun,
                  provenance=True,
                  fwkJobReport=True, #NOT IN LOCAL
                  jsonInput=runsAndLumis() #NOT IN LOCAL
                  )

elif suffix=='18D':
  if analysis=="ggtautau":
    modulesToRun=[muonScaleRes2018v5UL()],
  else if analysis=="ggbb"
    modulesToRun=[],

  p=PostProcessor(".",
                  inputFiles(), #NOT IN LOCAL  
                  selection.replace('\n',''),
                  branchsel="keep_and_drop.txt",
                  outputbranchsel="keep_and_drop.txt",
                  modules=modulesToRun,
                  provenance=True,
                  fwkJobReport=True, #NOT IN LOCAL
                  jsonInput=runsAndLumis() #NOT IN LOCAL
                  )

else:
  print "bo"


# keep and drop printout
print p.branchsel._ops
print p.outputbranchsel._ops

p.run()

print("DONE")
