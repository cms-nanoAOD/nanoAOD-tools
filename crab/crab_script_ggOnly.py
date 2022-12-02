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

#very basic selection which is covered then by the actual Hgg selection and crop at 1000 evts
#selection='''Sum$(Photon_pt > 18 && abs(Photon_eta)<2.5) > 1'''
selection='''Sum$(Photon_pt > 18 && (Photon_isScEtaEB || Photon_isScEtaEE) && Photon_electronVeto > 0.5 && Photon_hoe < 0.08) > 1'''

#2016 modules MC
PrefireCorr2016 = lambda : PrefCorr("L1prefiring_jetpt_2016BtoH.root", "L1prefiring_jetpt_2016BtoH", "L1prefiring_photonpt_2016BtoH.root", "L1prefiring_photonpt_2016BtoH")

#2017 modules MC
PrefireCorr2017 = lambda : PrefCorr('L1prefiring_jetpt_2017BtoF.root', 'L1prefiring_jetpt_2017BtoF', 'L1prefiring_photonpt_2017BtoF.root', 'L1prefiring_photonpt_2017BtoF')

import sys
print sys.argv
suffix=sys.argv[2].split("=")[1]


if suffix=='16a':
  p=PostProcessor(".", 
                  inputFiles(), #NOT IN LOCAL  
                  selection.replace('\n',''),
                  branchsel="keep_and_drop.txt",
                  outputbranchsel="keep_and_drop.txt",
                  modules=[puAutoWeight_UL2016(),jetmetUncertaintiesAPV2016UL(),jetmetUncertaintiesAPV2016ULAll(), muonScaleRes2016v5ULAPV(), PrefireCorr2016(), tauCorrs2016ULpreVFP(), lepSFID2016_B(), lepSFISO2016_B(), gammaSF_UL16PreVFP()],
                  provenance=True,
                  fwkJobReport=True, #NOT IN LOCAL
                  jsonInput=runsAndLumis() #NOT IN LOCAL
                  )
elif suffix=='16b' :
   p=PostProcessor(".", 
                  inputFiles(), #NOT IN LOCAL      
                  selection.replace('\n',''),
                  branchsel="keep_and_drop.txt",
                  outputbranchsel="keep_and_drop.txt",
                  modules=[puAutoWeight_UL2016(),jetmetUncertainties2016UL(),jetmetUncertainties2016ULAll(), muonScaleRes2016v5UL(), PrefireCorr2016(), tauCorrs2016ULpostVFB(), lepSFID2016_H(), lepSFISO2016_H(), gammaSF_UL16PostVFP()],
                  provenance=True,
                  fwkJobReport=True, #NOT IN LOCAL
                  jsonInput=runsAndLumis() #NOT IN LOCAL
                  )
elif suffix=='17':
   p=PostProcessor(".", 
                  inputFiles(), #NOT IN LOCAL  
                  selection.replace('\n',''),
                  branchsel="keep_and_drop.txt",
                  outputbranchsel="keep_and_drop.txt",
                  modules=[puAutoWeight_UL2017(),jetmetUncertainties2017UL(),jetmetUncertainties2017ULAll(), muonScaleRes2017v5UL(), PrefireCorr2017(), tauCorrs2017UL(), lepSFID2017(), lepSFISO2017(), gammaSF_UL17()],
                  provenance=True,
                  fwkJobReport=True, #NOT IN LOCAL
                  jsonInput=runsAndLumis() #NOT IN LOCAL
                  )
elif suffix=='18':
   p=PostProcessor(".", 
                  inputFiles(), #NOT IN LOCAL  
                  selection.replace('\n',''),
                  branchsel="keep_and_drop.txt",
                  outputbranchsel="keep_and_drop.txt",
                  modules=[puAutoWeight_UL2018(),jetmetUncertainties2018UL(),jetmetUncertainties2018ULAll(), muonScaleRes2018v5UL(), tauCorrs2018UL(), lepSFID2018(), lepSFISO2018(), gammaSF_UL18()],
                  provenance=True, 
                  fwkJobReport=True, #NOT IN LOCAL
                  jsonInput=runsAndLumis() #NOT IN LOCAL
                  )
elif suffix=='16aD':
  p=PostProcessor(".",
                  inputFiles(), #NOT IN LOCAL  
                  selection.replace('\n',''),
                  branchsel="keep_and_drop.txt",
                  outputbranchsel="keep_and_drop.txt",
                  modules=[muonScaleRes2016v5ULAPV()],
                  provenance=True,
                  fwkJobReport=True, #NOT IN LOCAL
                  jsonInput=runsAndLumis() #NOT IN LOCAL
                  )
elif suffix=='16bD' :
   p=PostProcessor(".",
                  inputFiles(), #NOT IN LOCAL      
                  selection.replace('\n',''),
                  branchsel="keep_and_drop.txt",
                  outputbranchsel="keep_and_drop.txt",
                  modules=[muonScaleRes2016v5UL()],
                  provenance=True,
                  fwkJobReport=True, #NOT IN LOCAL
                  jsonInput=runsAndLumis() #NOT IN LOCAL
                  )
elif suffix=='17D':
   p=PostProcessor(".",
                  inputFiles(), #NOT IN LOCAL  
                  selection.replace('\n',''),
                  branchsel="keep_and_drop.txt",
                  outputbranchsel="keep_and_drop.txt",
                  modules=[muonScaleRes2017v5UL()],
                  provenance=True,
                  fwkJobReport=True, #NOT IN LOCAL
                  jsonInput=runsAndLumis() #NOT IN LOCAL
                  )
elif suffix=='18D':
   p=PostProcessor(".",
                  inputFiles(), #NOT IN LOCAL  
                  selection.replace('\n',''),
                  branchsel="keep_and_drop.txt",
                  outputbranchsel="keep_and_drop.txt",
                  modules=[muonScaleRes2018v5UL()],
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
