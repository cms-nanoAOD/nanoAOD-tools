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

#very basic selection which is covered then by the actual Hgg selection and crop at 1000 evts
selection='''Sum$(Photon_pt > 18 && abs(Photon_eta)<2.5) > 1'''

#work on a local file
# a modified nanoAOD which contians extra phton features -> to be merged soon to the central stuff
files=["/hadoop/cms/store/user/hmei/nanoaod_runII/HHggtautau/HHggtautau_Era2018_private_v2_20201005/test_nanoaod_1.root"]

f16a=["root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL16NanoAODAPVv9/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v2/2520000/09C7F740-4B72-164F-802A-AD61543C717C.root"]

f16b=["root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL16NanoAODv9/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_v17-v2/2520000/9503E3B6-3BC0-A043-92BF-019E4C64026D.root"]

f17=["root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL17NanoAODv9/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_mc2017_realistic_v9-v2/100000/89E8691C-A390-C74F-A065-70EF7E3B8F77.root"]

f18=["root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18NanoAODv9/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/100000/5816099C-2902-3348-8627-2DEB0BBC33CD.root"]


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
                  modules=[puAutoWeight_UL2016(),jetmetUncertaintiesAPV2016UL(),jetmetUncertaintiesAPV2016ULAll(), muonScaleRes2016v5ULAPV(), PrefireCorr2016(), tauCorrs2016ULpreVFP(), lepSFID2016_B(), lepSFISO2016_B()],
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
                  modules=[puAutoWeight_UL2016(),jetmetUncertainties2016UL(),jetmetUncertainties2016ULAll(), muonScaleRes2016v5UL(), PrefireCorr2016(), tauCorrs2016ULpostVFB(), lepSFID2016_H(), lepSFISO2016_H()],
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
                  modules=[puAutoWeight_UL2017(),jetmetUncertainties2017UL(),jetmetUncertainties2017ULAll(), muonScaleRes2017v5UL(), PrefireCorr2017(), tauCorrs2017UL(), lepSFID2017(), lepSFISO2017()],
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
                  modules=[puAutoWeight_UL2018(),jetmetUncertainties2018UL(),jetmetUncertainties2018ULAll(), muonScaleRes2018v5UL(), tauCorrs2018UL(), lepSFID2018(), lepSFISO2018()],
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
