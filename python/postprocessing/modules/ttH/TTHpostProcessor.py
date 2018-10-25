#!/usr/bin/env python
import os
import sys
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 





### SKIM 
cut = ''

### SLIM FILE
outputSlim = os.environ['CMSSW_BASE']+"/python/PhysicsTools/NanoAODTools/postprocessing/modules/ttH/OutputSlim.txt"
inputSlim  = os.environ['CMSSW_BASE']+"/python/PhysicsTools/NanoAODTools/postprocessing/modules/ttH/InputSlim.txt"

from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.collectionMerger import collectionMerger
from PhysicsTools.NanoAODTools.postprocessing.modules.ttH.skimNRecoLeps import *

#
minelpt  = 10
minmupt  = 10
maxeleta = 2.5
maxmueta = 2.5

isoAndIPCuts = lambda  x : x.miniPFRelIso_all < 0.1  and x.dxy < 0.05 and x.dz < 0.1 and x.sip3d < 8 

goodElec = lambda x : x.pt > minelpt and abs(x.eta) < maxeleta and x.mvaFall17noIso_WPL and isoAndIPCuts(x)
goodMuon = lambda x : x.pt > minmupt and abs(x.eta) < maxmueta  and isoAndIPCuts(x)

goodLepProducer = collectionMerger(input=["Electron","Muon"], output="LepGood",
                                   maxObjects=10,
                                   selector=dict([("Electron", goodElec),
                                                  ("Muon", goodMuon)
                                                  ]))

mod = [puAutoWeight(), goodLepProducer, skimRecoLeps()]



if __name__ == "__main__": # more stuff to import below
    filepath = ['../EdgeZ/EE61951B-4642-E811-B72D-001E67FA38A8.root']
    outdir = '.'
    POSTPROCESSOR=PostProcessor(outdir,filepath,cut,inputSlim,mod,provenance=True,outputbranchsel=outputSlim)
    POSTPROCESSOR.run()
    
    

else: 
    # get the options
    from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import getCrabOption
    doData=getCrabOption("doData",False)
    if doData: mod = [goodLepProducer, skimRecoLeps()]

    


    #this takes care of converting the input files from CRAB
    from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
    
    if 'IS_CRAB' in os.environ:
        POSTPROCESSOR=PostProcessor(".",inputFiles(),cut,inputSlim,mod,provenance=True,fwkJobReport=True,jsonInput=runsAndLumis(), outputbranchsel=outputSlim)
    else:
        print 'we are not yet in crab'

    from PhysicsTools.NanoAODTools.postprocessing.datasets.mc2017    import samples as mcSamples
    from PhysicsTools.NanoAODTools.postprocessing.datasets.data2017  import samples as dataSamples

    selectedSamples=mcSamples
    if doData:
        jsonFile='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Final/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'
    else: 
        jsonFile=0
    print jsonFile


