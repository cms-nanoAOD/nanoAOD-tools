#!/usr/bin/env python

# Config file defines two things: POSTPROCESSOR and selectedSamples. 
# selectedSamples is read by the submitter to configure the different samples. The submiter should produce a json file with all the sample options. 
# POSTPROCESSOR is read at running time, and configures the modules to run using the json file produced.

import os
import sys
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

import json


from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.collectionMerger import collectionMerger
from PhysicsTools.NanoAODTools.postprocessing.modules.common.TriggerBitFilter import TriggerBitFilter
from PhysicsTools.NanoAODTools.postprocessing.modules.common.addFlags import AddFlags
from PhysicsTools.NanoAODTools.postprocessing.modules.ttH.objectCleaning import ObjectCleaning

# get the options
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import getCrabOption


# definition of output (additional skim may be applied in the modules) 
### SKIM 
cut = None

### SLIM FILE
outputSlim = os.environ['CMSSW_BASE']+"/python/PhysicsTools/NanoAODTools/postprocessing/modules/ttH/OutputSlim.txt"
inputSlim  = os.environ['CMSSW_BASE']+"/python/PhysicsTools/NanoAODTools/postprocessing/modules/ttH/InputSlim.txt"


doData=getCrabOption("doData",False)

if not 'IS_CRAB' in os.environ and not 'IS_RUN' in os.environ:

    from PhysicsTools.NanoAODTools.postprocessing.datasets.triggers_13TeV_DATA2017 import * 


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



## definition of postprocessor 

# postprocessor is only read when we are in running mode 

if 'IS_CRAB' in os.environ or 'IS_RUN' in os.environ:
    try:
        with open('options_sample.json','r') as sampoptjson: 
            sampOpt = json.loads(sampoptjson.read())
            sampoptjson.close()
    except: 
        raise RuntimeError("No options_sample.json found")


    def _ttH_idEmu_cuts_E3(lep):
        if (abs(lep.pdgId)!=11): return True
        if (lep.hoe>=(0.10-0.00*(abs(lep.deltaEtaSC+lep.eta)>1.479))): return False
        if (lep.eInvMinusPInv<=-0.04): return False
        if (lep.sieie>=(0.011+0.019*(abs(lep.deltaEtaSC+lep.eta)>1.479))): return False
        return True

    def preselectMuon(lep):
        return lep.pt > 5 and abs(lep.eta) < 2.4 and abs(lep.dxy) < 0.05 and abs(lep.dz) < 0.1 and lep.miniPFRelIso_all < 0.4 and lep.sip3d < 8

    def preselectElectron(lep):
        return lep.pt > 7 and abs(lep.eta) < 2.5 and abs(lep.dxy) < 0.05 and abs(lep.dz) < 0.1 and lep.miniPFRelIso_all < 0.4  and lep.sip3d < 8 and lep.mvaFall17V1noIso_WPL and lep.lostHits <=1

    def preselectLepton(lep):
        return preselectElectron(lep) if abs(lep.pdgId) == 11 else preselectMuon(lep)
    
    def clean_and_FO_selection_TTH(lep):
        return lep.conept>10 and lep.jetBTagDeepCSV<0.4941 and (abs(lep.pdgId)!=11 or (_ttH_idEmu_cuts_E3(lep) and lep.convVeto and lep.lostHits==0)\
                                                                    ) \
                                                                    and (lep.mvaTTH>0.90 or \
                                                                             (abs(lep.pdgId)==13 and lep.jetBTagDeepCSV<0.07 and lep.segmentComp>0.3 and 1/(1+lep.jetRelIso)>0.60) or \
                                                                             (abs(lep.pdgId)==11 and lep.jetBTagDeepCSV<0.07 and lep.mvaFall17V1noIso>0.5 and 1/(1+lep.jetRelIso)>0.60) \
                                                                             )

    def _bitFromInt(num, idx):
        # returns the bit in the idx's position of num
        bitMap = "{0:b}".format(num)
        if idx > len(bitMap): return False
        return bool(int(bitMap[-idx]))

    def _FOTauSel(tau):
        return tau.pt > 20 and abs(tau.eta)<2.3 and abs(tau.dxy) < 1000 and abs(tau.dz) < 0.2 and _bitFromInt(tau.idMVAoldDMdR032017v2,2) and tau.idDecayMode

    def conept_TTH(lep):
        if (abs(lep.pdgId)!=11 and abs(lep.pdgId)!=13): return lep.pt
        if (abs(lep.pdgId)!=13 or lep.mediumId>0) and lep.mvaTTH > 0.90: return lep.pt
        else: return 0.90 * lep.pt * (1+lep.jetRelIso)

    objCleaning = ObjectCleaning( looseLeptonSelection = lambda x : preselectLepton(x),
                                  FOLeptonSelection    = lambda x : clean_and_FO_selection_TTH(x),
                                  FOTauSelection       = lambda x : _FOTauSel(x),
                                  jetSelection         = lambda jet: abs(jet.eta)<2.4 and _bitFromInt(jet.jetId,2) and (jet.pt) > 15,
                                  conePt               = lambda x : conept_TTH(x),
                                  )
                                  
    puAutoWeight     = puAutoWeight()
    
    from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis


    mod = [objCleaning ] 
    
    if not sampOpt['isData']:
        # add pile-up weight before any skim
        mod = [puAutoWeight] + mod
        
        ## add jet met uncertainties
        from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import jetmetUncertainties2017All, jetmetUncertainties2017
        jmeUncert = jetmetUncertainties2017()
        jmeUncert.metBranchName = 'METFixEE2017'
        mod.extend([jmeUncert]) # jetmetUncertainties2017All()
    
        ## add xsec branch
        addFlags = AddFlags([ (('xsec','F'), lambda ev : sampOpt['xsec'] ) ])
        mod.extend([addFlags])
    
    
    if 'triggers' in sampOpt:
        if not 'vetotriggers' in sampOpt:
            raise RuntimeError('[%s]: You have specified trigger requierments, but not veto triggers. Please include them (can be an empty list)')
        triggerBitFilter = TriggerBitFilter( triggers = sampOpt['triggers'],
                                             vetotriggers = sampOpt['vetotriggers'])
        mod = [triggerBitFilter] + mod
    
    
    jsonInput = sampOpt['json'] if 'json' in sampOpt else runsAndLumis()     
    POSTPROCESSOR=PostProcessor(".",inputFiles() if 'IS_CRAB' in os.environ else [],cut,inputSlim,mod,provenance=True,fwkJobReport=True,jsonInput=jsonInput, outputbranchsel=outputSlim)




