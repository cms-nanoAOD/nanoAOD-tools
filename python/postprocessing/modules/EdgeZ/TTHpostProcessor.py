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
from PhysicsTools.NanoAODTools.postprocessing.modules.EdgeZ.skimNRecoLeps import SkimRecoLeps
from PhysicsTools.NanoAODTools.postprocessing.modules.EdgeZ.isoTrackAnalysis import IsoTrackAnalysis
from PhysicsTools.NanoAODTools.postprocessing.modules.common.TriggerBitFilter import TriggerBitFilter
from PhysicsTools.NanoAODTools.postprocessing.modules.EdgeZ.edgeFriends import edgeFriends, _susyEdgeTight, _susyEdgeLoose



goodElec =  lambda x : _susyEdgeLoose(x)
goodMuon =  lambda x : _susyEdgeLoose(x)

goodLepProducer = collectionMerger(input=["Electron","Muon"], output="LepGood",
                                   maxObjects=10,
                                   selector=dict([("Electron", goodElec),
                                                  ("Muon", goodMuon)
                                                  ]))

puAutoWeight     = puAutoWeight()
isoTrackAnalysis = IsoTrackAnalysis(storeCollection=True) # store collection only for synch

edgeFriends = edgeFriends("Edge", lambda lep : _susyEdgeTight(lep),
                          cleanJet = lambda lep,jet,dr : (jet.pt < 35 and dr < 0.4))

from PhysicsTools.NanoAODTools.postprocessing.datasets.triggers_13TeV_DATA2017 import * 


def BuildJsonForTesting():

 
    sampOpt = { 'isData' : True,
                'triggers' : [], #triggers_mumu_iso + triggers_3mu , # [],#triggers_ee + triggers_3e+triggers_ee_noniso,
                'vetotriggers' : [],#triggers_mumu_iso + triggers_3mu,
                'json':   None # '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt'
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
        jsonFile='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt'
        
        selectedSamples = dataSamples

        DatasetsAndTriggersMap = {}; DatasetsAndVetosMap = {} 
        DatasetsAndTriggersMap["DoubleMuon"     ] = triggers_mumu_iso + triggers_3mu
        DatasetsAndTriggersMap["DoubleEG"       ] = triggers_ee + triggers_3e + triggers_ee_noniso
        DatasetsAndTriggersMap["MuonEG"         ] = triggers_mue + triggers_2mu1e + triggers_2e1mu + triggers_mue_noiso
        DatasetsAndTriggersMap["SingleMuon"     ] = triggers_1mu_iso
        DatasetsAndTriggersMap["SingleElectron" ] = triggers_1e_iso
        DatasetsAndTriggersMap["MET" ] = []
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
    mod = [puAutoWeight,  goodLepProducer, skimRecoLeps, isoTrackAnalysis, edgeFriends]
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
    filepath  = [
        '/pool/ciencias/userstorage/sscruz/NanoAOD_test/Run2017C_MuonEG_Nano14Dec2018-v1_F7055783-BE3F-BF4B-83A2-64A73E13EA85.root',
        #'/pool/ciencias/userstorage/sscruz/NanoAOD_test/SingleMuon_612BB142-CD08-B14D-BA60-2311FA0F2BD2.root',
        #'/pool/ciencias/userstorage/sscruz/NanoAOD_test/TTbar_4B84BCC5-FE7C-714B-81AD-5A76C3B511FF.root',
                  ]


    outdir = '.'



    POSTPROCESSOR = LoadCfgToRun(filepath)
    POSTPROCESSOR.run()
