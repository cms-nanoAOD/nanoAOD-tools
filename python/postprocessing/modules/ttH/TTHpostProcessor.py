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
from PhysicsTools.NanoAODTools.postprocessing.modules.ttH.skimNRecoLeps import SkimRecoLeps
#from PhysicsTools.NanoAODTools.postprocessing.modules.ttH.l1JetCalibrations import l1JetCalibrations
from PhysicsTools.NanoAODTools.postprocessing.modules.ttH.isoTrackAnalysis import IsoTrackAnalysis
from PhysicsTools.NanoAODTools.postprocessing.modules.common.TriggerBitFilter import TriggerBitFilter

#
minelpt  = 5
minmupt  = 5
maxeleta = 2.5
maxmueta = 2.4

isoAndIPCuts = lambda  x : x.miniPFRelIso_all < 0.4  and abs(x.dxy) < 0.05 and abs(x.dz) < 0.1 and x.sip3d < 8 

susy_ttH_el  = lambda x  : x.pt > minelpt and abs(x.eta) < maxeleta and x.mvaFall17V1noIso_WPL and isoAndIPCuts(x)
susy_ttH_mu  = lambda x : x.pt > minmupt and abs(x.eta) < maxmueta  and isoAndIPCuts(x)

top_el       = lambda x : x.pt > 20 and x.lostHits < 2 and x.cutBased == 4 and x.pfRelIso03_all < 0.0588 # (pf iso larger than the cuts used)
top_mu       = lambda x : x.pt > 20 and x.tightId  and x.pfRelIso04_all < 0.4

goodElec =  lambda x : susy_ttH_el(x) or top_el(x)
goodMuon =  lambda x : susy_ttH_mu(x) or top_mu(x)

goodLepProducer = collectionMerger(input=["Electron","Muon"], output="LepGood",
                                   maxObjects=10,
                                   selector=dict([("Electron", goodElec),
                                                  ("Muon", goodMuon)
                                                  ]))

puAutoWeight     = puAutoWeight()
isoTrackAnalysis = IsoTrackAnalysis(storeCollection=True) # store collection only for synch

from PhysicsTools.NanoAODTools.postprocessing.datasets.triggers_13TeV_DATA2017 import * 

def BuildJsonForTesting():

 
    sampOpt = { 'isData' : False,
                'triggers' : [],#triggers_ee + triggers_3e+triggers_ee_noniso,
                'vetotriggers' : [],#triggers_mumu_iso + triggers_3mu,
                #'json': '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Final/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'
                'json': None
                }

    optjsonfile = open('options_sample.json','w')
    optjsonfile.write(json.dumps(sampOpt))
    optjsonfile.close()

    

    

def LoadCfgForSubmission():
    # get the options
    from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import getCrabOption
    doData=getCrabOption("doData",False)

    print 'Shall we do data?', doData


    print '[TTHpostProcessor]: Submission step'
    from PhysicsTools.NanoAODTools.postprocessing.datasets.mc2017    import samples as mcSamples
    from PhysicsTools.NanoAODTools.postprocessing.datasets.data2017  import samples as dataSamples
    
    
    if doData:
        jsonFile='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Final/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'
        
        selectedSamples = dataSamples

        DatasetsAndTriggersMap = {}; DatasetsAndVetosMap = {} 
        DatasetsAndTriggersMap["DoubleMuon"     ] = triggers_mumu_iso + triggers_3mu
        DatasetsAndTriggersMap["DoubleEG"       ] = triggers_ee + triggers_3e + triggers_ee_noniso
        DatasetsAndTriggersMap["MuonEG"         ] = triggers_mue + triggers_2mu1e + triggers_2e1mu + triggers_mue_noiso
        DatasetsAndTriggersMap["SingleMuon"     ] = triggers_1mu_iso
        DatasetsAndTriggersMap["SingleElectron" ] = triggers_1e_iso
        DatasetsAndTriggersMap["MET" ] = triggers_met
        DatasetsAndTriggersMap["Electron_noOverlapRemov"] = [] 

        DatasetsAndVetosMap["DoubleMuon"    ] = []
        DatasetsAndVetosMap["DoubleEG"      ] = DatasetsAndTriggersMap["DoubleMuon"] + DatasetsAndVetosMap["DoubleMuon"] 
        DatasetsAndVetosMap["MuonEG"        ] = DatasetsAndTriggersMap["DoubleEG"  ] + DatasetsAndVetosMap["DoubleEG"  ] 
        DatasetsAndVetosMap["SingleMuon"    ] = DatasetsAndTriggersMap["MuonEG"    ] + DatasetsAndVetosMap["MuonEG"    ] 
        DatasetsAndVetosMap["SingleElectron"] = DatasetsAndTriggersMap["SingleMuon"] + DatasetsAndVetosMap["SingleMuon"] 
        DatasetsAndVetosMap["MET"] = [] 
        DatasetsAndVetosMap["Electron_noOverlapRemov"] = [] 

        for sample in selectedSamples:
            jsn = open( jsonFile ,'r')
            sample.options['json'] = json.loads ( jsn.read())
            sample.options['isData'] = True
            jsn.close()
            for smp, trig in DatasetsAndTriggersMap.iteritems():
                if smp in sample.name:
                    sample.options['triggers']     = trig
                    sample.options['vetotriggers'] = DatasetsAndVetosMap[smp]
                    
                    break

    else:
        selectedSamples=mcSamples
        for sample in selectedSamples: sample.options['isData'] = False

    return selectedSamples

def LoadCfgToRun(inputFile=None):

 #this takes care of converting the input files from CRAB
    if not inputFile:
        from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
    
    sampoptjson = open('options_sample.json','r')
    sampOpt = json.loads(sampoptjson.read())
    sampoptjson.close()

    skimRecoLeps     = SkimRecoLeps(sampOpt['isData'] == True, nMinLeps=2)
    mod = [puAutoWeight,  goodLepProducer, skimRecoLeps, isoTrackAnalysis]
    if sampOpt['isData']: 
        mod.remove( puAutoWeight ) 
    else:
        from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import jetmetUncertainties2017All, jetmetUncertainties2017
        jmeUncert = jetmetUncertainties2017()
        jmeUncert.metBranchName = 'METFixEE2017'
        mod.extend([jmeUncert]) # jetmetUncertainties2017All()

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
#    filepath = ['root://xrootd-cms.infn.it///store/data/Run2017F/DoubleEG/NANOAOD/31Mar2018-v1/10000/B471FCAD-734A-E811-BAD1-002590CB0B5A.root',]
    #filepath = ['/afs/cern.ch/work/s/sesanche/public/forEdge/test_forsynch_v2.root']
    filepath  = ['/afs/cern.ch/work/s/sesanche/public/forEdge/test_forsynch_v4.root']
    #filepath = ['root://xrootd-cms.infn.it///store/mc/RunIIFall17NanoAODv4/ZZTo4L_13TeV_powheg_pythia8/NANOAODSIM/PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/00000/8E11DCE3-B8F2-204E-9E55-EB57E8443B83.root']
    #filepath = ['fewEvents.root']
    #'root://xrootd-cms.infn.it///store/data/Run2017F/DoubleEG/NANOAOD/31Mar2018-v1/10000/FCF63A41-754A-E811-893A-0CC47A3B0572.root']


    outdir = '.'



    POSTPROCESSOR = LoadCfgToRun(filepath)
    POSTPROCESSOR.run()
