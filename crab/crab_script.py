#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
from PhysicsTools.NanoAODTools.postprocessing.examples.MySelectorModule import *

#common tools
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *

#metCorrector = createJMECorrector(isMC=False, dataYear=2016, runPeriod="E", jesUncert="Total" , metBranchName="METFixEE2017")

metCorrector = createJMECorrector(isMC=True, dataYear='2018', jesUncert="All", redojec=True)
fatJetCorrector = createJMECorrector(isMC=True, dataYear='2018', jesUncert="All", redojec=True, jetType = "AK8PFchs")
'''
pufile_data2018="%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/puData2018_withVar.root" % os.environ['CMSSW_BASE']
pufile_mc2018="%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/mcPileup2018.root" % os.environ['CMSSW_BASE']
puWeight_2018 = puWeightProducer(pufile_mc2018,pufile_data2018,"pu_mc","pileup",verbose=False, doSysVar=True)
puAutoWeight_2018 = puWeightProducer("auto",pufile_data2018,"pu_mc","pileup",verbose=False)
'''
passMETFilter = "Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter"

infile = ["/eos/user/a/adeiorio/Wprime/nosynch/WJets.root"]
#infile = ["/eos/user/a/adeiorio/Wprime/Wprime_4000_RH.root"]
#infile = ["/eos/user/a/adeiorio/Wprime/Wprime_1000_RH.root"]
#infile = ["/eos/user/a/adeiorio/Wprime/TT_Mtt-700to1000.root"]

#infile = [" root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv5/WprimeToTB_TToLep_M-4000_RH_TuneCUETP8M1_13TeV-comphep-pythia8/NANOAODSIM/PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/120000/3DEA7D83-43FB-5141-9EC7-376B57192BE8.root"]
outpath = "/eos/user/a/adeiorio/Wprime/nosynch/"
#p=PostProcessor(".",infile, passMETFilter, "", modules=[MySelectorModule(), PrefireCorr(), metCorrector(), fatJetCorrector(), puWeightProducer()], provenance=True, fwkJobReport=True, jsonInput=runsAndLumis())
branc_sel = "/afs/cern.ch/work/a/adeiorio/CMSSW_10_5_0/src/PhysicsTools/NanoAODTools/python/postprocessing/examples/keep_and_drop.txt"
#Deafult PostProcessor(outputDir,inputFiles,cut=None,branchsel=None,modules=[],compression="LZMA:9",friend=False,postfix=None, jsonInput=None,noOut=False,justcount=False,provenance=False,haddFileName=None,fwkJobReport=False,histFileName=None,histDirName=None, outputbranchsel=None,maxEntries=None,firstEntry=0, prefetch=False,longTermCache=False)
p=PostProcessor(outpath, infile, passMETFilter, modules=[MySelectorModule(), puWeight_2018()], provenance=True, outputbranchsel=branc_sel, maxEntries=50000)
p.run()

#, PrefCorr(), metCorrector(), fatJetCorrector(), puWeight_2018()
print "DONE"

