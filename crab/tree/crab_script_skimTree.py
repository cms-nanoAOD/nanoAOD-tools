import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
#from exampleModule import *
from MainModule import *
#from btv import *
#from EfficiencyModule import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr16 import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import * # using NanoAod branch L1PreFiringWeight*

treecut = "nJet>0 && Jet_pt>20 && (Sum$(Muon_pt>20)>0 || Sum$(Electron_pt>30)>0)" # && Entry$<100"#(nMuon>0 || nElectron>0)" # && (Muon_pt>5 || Electron_pt>10) (nMuon>0 || nElectron>0)"
#inputFiles=["root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL16NanoAODAPVv9/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/280000/D2AF2E22-BD5B-B542-B6BA-6ABF26FAC0FC.root"]
#/store/data/Run2017B/SingleMuon/NANOAOD/02Apr2020-v1/50000/FBFADBAD-5164-6A4D-A19E-EFF003090EC5.root"]
#inputFiles=["/afs/cern.ch/user/m/mikumar/work/private/NanoAOD_new/CMSSW_10_6_0/src/Inputroot_files/Tree/single_electrondata_2016_runD/35F06149-6032-374D-8750-10CAAF330EEE.root"]
#inputFiles=["/afs/cern.ch/user/m/mikumar/work/private/NanoAOD_new/CMSSW_10_6_0/src/Inputroot_files/Tree/single_muondata_2016_runD/5A4AA866-8941-334C-A591-7D2728C6F63F.root"]
#inputFiles=["/afs/cern.ch/user/m/mikumar/work/private/NanoAOD_new/CMSSW_10_6_0/src/Inputroot_files/Tree/ST_tch/06314878-0D6B-544B-9E2C-C5EDCD0666D3_2017.root"]
p=PostProcessor(".",
		inputFiles(),
		treecut,
		modules=[MainModuleConstr_mc_UL2016postVFP(),puWeight_UL2016postVFP()],
		outputbranchsel="keep_and_drop.txt",
		provenance=True,
		fwkJobReport=True,
		jsonInput=runsAndLumis())
		
p.run()

print("DONE")
