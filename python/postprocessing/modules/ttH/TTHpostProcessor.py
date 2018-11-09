#!/usr/bin/env python
import os
import sys
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

import json



### SKIM 
cut = None

### SLIM FILE
outputSlim = os.environ['CMSSW_BASE']+"/python/PhysicsTools/NanoAODTools/postprocessing/modules/ttH/OutputSlim.txt"
inputSlim  = os.environ['CMSSW_BASE']+"/python/PhysicsTools/NanoAODTools/postprocessing/modules/ttH/InputSlim.txt"

from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.collectionMerger import collectionMerger
from PhysicsTools.NanoAODTools.postprocessing.modules.ttH.skimNRecoLeps import *
from PhysicsTools.NanoAODTools.postprocessing.modules.ttH.l1JetCalibrations import l1JetCalibrations
from PhysicsTools.NanoAODTools.postprocessing.modules.common.TriggerBitFilter import TriggerBitFilter

#
minelpt  = 10
minmupt  = 10
maxeleta = 2.5
maxmueta = 2.5

isoAndIPCuts = lambda  x : x.miniPFRelIso_all < 0.1  and abs(x.dxy) < 0.05 and abs(x.dz) < 0.1 and x.sip3d < 8 

goodElec = lambda x : x.pt > minelpt and abs(x.eta) < maxeleta and x.mvaFall17noIso_WPL and isoAndIPCuts(x)
goodMuon = lambda x : x.pt > minmupt and abs(x.eta) < maxmueta  and isoAndIPCuts(x)

goodLepProducer = collectionMerger(input=["Electron","Muon"], output="LepGood",
                                   maxObjects=10,
                                   selector=dict([("Electron", goodElec),
                                                  ("Muon", goodMuon)
                                                  ]))

jetCalibrations = l1JetCalibrations( 'Fall17_17Nov2017F_V6_DATA') # '94X_dataRun2_v6' if doData else
puAutoWeight    = puAutoWeight()
skimRecoLeps    = skimRecoLeps()

from PhysicsTools.NanoAODTools.postprocessing.datasets.triggers_13TeV_DATA2017 import * 

def BuildJsonForTesting():

 
    sampOpt = { 'isData' : True,
                'triggers' : triggers_ee + triggers_3e+triggers_ee_noniso,
                'vetotriggers' : triggers_mumu_iso + triggers_3mu,
                'json': '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Final/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'
                }

    optjsonfile = open('options_sample.json','w')
    optjsonfile.write(json.dumps(sampOpt))
    optjsonfile.close()

    

    

def LoadCfgForSubmission():
    # get the options
    from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import getCrabOption
    doData=getCrabOption("doData",False)




    print '[TTHpostProcessor]: Submission step'
    from PhysicsTools.NanoAODTools.postprocessing.datasets.mc2017    import samples as mcSamples
    from PhysicsTools.NanoAODTools.postprocessing.datasets.data2017  import samples as dataSamples
    
    selectedSamples=mcSamples
    if doData:
        jsonFile='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Final/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'
        
        selectedSamples = dataSamples

        DatasetsAndTriggersMap = {}; DatasetsAndVetosMap = {} 
        DatasetsAndTriggersMap["DoubleMuon"     ] = triggers_mumu_iso + triggers_3mu
        DatasetsAndTriggersMap["DoubleEG"       ] = triggers_ee + triggers_3e + triggers_ee_noniso
        DatasetsAndTriggersMap["MuonEG"         ] = triggers_mue + triggers_2mu1e + triggers_2e1mu
        DatasetsAndTriggersMap["SingleMuon"     ] = triggers_1mu_iso
        DatasetsAndTriggersMap["SingleElectron" ] = triggers_1e_iso
        
        DatasetsAndVetosMap["DoubleMuon"    ] = []
        DatasetsAndVetosMap["DoubleEG"      ] = DatasetsAndTriggersMap["DoubleMuon"] + DatasetsAndVetosMap["DoubleMuon"] 
        DatasetsAndVetosMap["MuonEG"        ] = DatasetsAndTriggersMap["DoubleEG"  ] + DatasetsAndVetosMap["DoubleEG"  ] 
        DatasetsAndVetosMap["SingleMuon"    ] = DatasetsAndTriggersMap["MuonEG"    ] + DatasetsAndVetosMap["MuonEG"    ] 
        DatasetsAndVetosMap["SingleElectron"] = DatasetsAndTriggersMap["SingleMuon"] + DatasetsAndVetosMap["SingleMuon"] 


        for sample in selectedSamples:
            jsn = open( jsonFile ,'r')
            sample.options['json'] = json.loads ( jsn.read())
            jsn.close()
            for smp, trig in DatasetsAndTriggersMap.iteritems():
                if smp in sample.name:
                    sample.options['triggers']     = trig
                    sample.options['vetotriggers'] = DatasetsAndVetosMap[smp]
                    
                    break

    return selectedSamples

def LoadCfgToRun(inputFile=None):

 #this takes care of converting the input files from CRAB
    if not inputFile:
        from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
    
    sampoptjson = open('options_sample.json','r')
    sampOpt = json.loads(sampoptjson.read())
    sampoptjson.close()

    mod = [puAutoWeight,  goodLepProducer, skimRecoLeps, jetCalibrations]
    if sampOpt['isData']: 
        mod.remove( puAutoWeight ) 

    if 'triggers' in sampOpt:
        if not 'vetotriggers' in sampOpt:
            raise RuntimeError('[%s]: You have specified trigger requierments, but not veto triggers. Please include them (can be an empty list)')
        triggerBitFilter = TriggerBitFilter( triggers = sampOpt['triggers'],
                                             vetotriggers = sampOpt['vetotriggers'])
        mod = [triggerBitFilter] + mod


    jsonInput = sampOpt['json'] if 'json' in sampOpt else runsAndLumis()     
    POSTPROCESSOR=PostProcessor(".",inputFile if inputFile else inputFiles(),cut,inputSlim,mod,provenance=True,fwkJobReport=True,jsonInput=jsonInput, outputbranchsel=outputSlim)
        
    return POSTPROCESSOR





if not __name__ == "__main__": # this is only done when importing

    if 'IS_CRAB' in os.environ:
        POSTPROCESSOR = LoadCfgToRun()
    else:
        selectedSamples = LoadCfgForSubmission()



else:


    BuildJsonForTesting()
    #filepath = ['root://xrootd-cms.infn.it///store/mc/RunIIFall17NanoAOD/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/20000/0CB20624-3642-E811-B93F-001E6739B849.root']
    filepath = ['root://xrootd-cms.infn.it///store/data/Run2017F/DoubleEG/NANOAOD/31Mar2018-v1/10000/B471FCAD-734A-E811-BAD1-002590CB0B5A.root',]
    #filepath = ['fewEvents.root']
    #'root://xrootd-cms.infn.it///store/data/Run2017F/DoubleEG/NANOAOD/31Mar2018-v1/10000/FCF63A41-754A-E811-893A-0CC47A3B0572.root']

    outdir = '.'



    POSTPROCESSOR = LoadCfgToRun(filepath)
    POSTPROCESSOR.run()
