import os
import sys
import math
import json
import ROOT
import random
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from modules import *


import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--isData', dest='isData', action='store_true',default=False)
parser.add_argument('--input', dest='inputFiles', action='append',default=[])
parser.add_argument('output', nargs=1)

args = parser.parse_args()

print "isData:",args.isData
print "inputs:",len(args.inputFiles)
for inputFile in args.inputFiles:
    rootFile = ROOT.TFile.Open(inputFile)
    if not rootFile:
        print "CRITICAL - file '"+inputFile+"' not found!"
        sys.exit(1)
    tree = rootFile.Get("Events")
    if not tree:
        print "CRITICAL - 'Events' tree not found in file '"+inputFile+"'!"
        sys.exit(1)
    print " - ",inputFile,", events=",tree.GetEntries()
    
print "output directory:",args.output[0]

globalOptions = {
    "isData":args.isData
}


muonSelection = [
    MuonSelection(
        outputName="tightMuons",
        storeKinematics=['pt','eta'],
        storeWeights=True,
        muonMinPt = [26.,15.],
        muonID = MuonSelection.TIGHT,
        muonIso = MuonSelection.TIGHT,
        globalOptions=globalOptions
    ),
    MuonVeto(
        inputCollection=lambda event: event.tightMuons_unselected,
        globalOptions=globalOptions
    ),
    ElectronVeto(
        inputCollection=lambda event: Collection(event,"Electron"),
        globalOptions=globalOptions
    ),
    SingleMuonTriggerSelection(
        inputCollection=lambda event: event["tightMuons"],
        outputName="IsoMuTrigger",
        storeWeights=True,
        globalOptions=globalOptions
    ),
    EventSkim(selection=lambda event: event.ntightMuons>=1),
    #EventSkim(selection=lambda event: event.nvetoMuons==0),
    EventSkim(selection=lambda event: event.nvetoElectrons==0),
    #EventSkim(selection=lambda event: event.IsoMuTrigger_flag==1),
    
    InvariantSystem(
        inputCollection = lambda event: event.tightMuons,
        outputName = "muonsys",
    )
]

analyzerChain = []

analyzerChain.append(
    MetFilter(
        globalOptions=globalOptions
    )
)



analyzerChain.extend(muonSelection)


if not args.isData:
    analyzerChain.append(
        JetMetUncertainties(
            era="2016",
            globalTag="Summer16_23Sep2016V4_MC"
        )
    )
    for systName,collection in [
        ("nominal",lambda event: event.jets_nominal),
        #("jerUp",lambda event: event.jets_jerUp),
        #("jerDown",lambda event: event.jets_jerDown),
        #("jesTotalUp",lambda event: event.jets_jesUp["Total"]),
        #("jesTotalDown",lambda event: event.jets_jesDown["Total"]),
    ]:
        analyzerChain.append(
            JetSelection(
                inputCollection=collection,
                leptonCollection=lambda event: event.tightMuons,
                outputName="selectedJets_"+systName,
                jetMinPt = 30.,
                jetMaxEta = 2.4,
                storeKinematics=['pt','eta'],
            )
        )
        analyzerChain.append(
            JetSelection(
                inputCollection=lambda event,systName=systName: getattr(event,"selectedJets_"+systName+"_unselected"),
                leptonCollection=lambda event: event.tightMuons,
                outputName="vetoFwdJets_"+systName,
                jetMinPt = 50.,
                jetMaxEta = 5.0,
                storeKinematics=[],
            )
        )
    
    analyzerChain.append(
        EventSkim(selection=lambda event: 
            len(event.selectedJets_nominal)>=2 #or \
            #len(event.selectedJets_jerUp)>=2 or \
            #len(event.selectedJets_jerDown)>=2 or \
            #len(event.selectedJets_jesTotalUp)>=2 or \
            #len(event.selectedJets_jesTotalDown)>=2
        )
    )
    
    for systName,jetCollection,metObject in [
        ("nominal",lambda event: event.selectedJets_nominal,lambda event: event.met_nominal),
        #("jerUp",lambda event: event.selectedJets_jerUp,lambda event: event.met_jerUp),
        #("jerDown",lambda event: event.selectedJets_jerDown,lambda event: event.met_jerDown),
        #("jesUp",lambda event: event.selectedJets_jesTotalUp,lambda event: event.met_jesUp["Total"]),
        #("jesDown",lambda event: event.selectedJets_jesTotalDown,lambda event: event.met_jesDown["Total"]),
        #("unclEnUp",lambda event: event.selectedJets_nominal,lambda event: event.met_unclEnUp),
        #("unclEnDown",lambda event: event.selectedJets_nominal,lambda event: event.met_unclEnDown),
    ]:
    
        analyzerChain.append(
            EventObservables(
                inputCollection = jetCollection,
                metInput = metObject,
                outputName = systName,
            )
        )
        analyzerChain.append(
            EventObservables(
                inputCollection = lambda event,jetCollection=jetCollection: jetCollection(event)+event.tightMuons,
                metInput = metObject,
                outputName = systName+"_lepton",
            )
        )
    '''
    #loose skim on ht/met (limits might use ht>1000 or (ht>200 && met>200))
    analyzerChain.append(
        EventSkim(selection=lambda event: 
            event.nominal_met>150.# or \
            #event.jerUp_met>150. or \
            #event.jerDown_met>150. or \
            #event.jesUp_met>150. or \
            #event.jesDown_met>150. or \
            #event.unclEnUp_met>150. or \
            #event.unclEnDown_met>150.
        )
    )
    '''
    analyzerChain.extend([
        PileupWeight(
            dataFile = os.path.expandvars("$CMSSW_BASE/src/PhysicsTools/NanoAODTools/data/pu/PU69000.root"),
            outputName ="puweight",
            processName = "TT_TuneCUETP8M2T4_13TeV-powheg-pythia8-evtgen",
            globalOptions=globalOptions
        ),
        PileupWeight(
            dataFile = os.path.expandvars("$CMSSW_BASE/src/PhysicsTools/NanoAODTools/data/pu/PU72500.root"),
            outputName ="puweightUp",
            processName = "TT_TuneCUETP8M2T4_13TeV-powheg-pythia8-evtgen",
            globalOptions=globalOptions
        ),
        PileupWeight(
            dataFile = os.path.expandvars("$CMSSW_BASE/src/PhysicsTools/NanoAODTools/data/pu/PU65500.root"),
            outputName ="puweightDown",
            processName = "TT_TuneCUETP8M2T4_13TeV-powheg-pythia8-evtgen",
            globalOptions=globalOptions
        )   
    ])
    
    storeVariables = [
        [lambda tree: tree.branch("genweight","F"),lambda tree,event: tree.fillBranch("genweight",event.Generator_weight)],
        [lambda tree: tree.branch("rho","F"),lambda tree,event: tree.fillBranch("rho",event.fixedGridRhoFastjetAll)], 
        [lambda tree: tree.branch("nPV","I"),lambda tree,event: tree.fillBranch("nPV",event.PV_npvsGood)],
        [lambda tree: tree.branch("nSV","I"),lambda tree,event: tree.fillBranch("nSV",event.nSV)],
        [
            lambda tree: tree.branch("MonoCentralPFJet80_PFMETNoMu_PFMHTNoMu_IDTight","I"),
            lambda tree,event: tree.fillBranch(
                "MonoCentralPFJet80_PFMETNoMu_PFMHTNoMu_IDTight",
                event.HLT_MonoCentralPFJet80_PFMETNoMu110_PFMHTNoMu110_IDTight*1+\
                event.HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight*2
            )
        ],
        [
            lambda tree: tree.branch("PFHT900","I"),
            lambda tree,event: tree.fillBranch("PFHT900",event.HLT_PFHT900)
        ],
    ]
    
    if args.inputFiles[0].find("SMS-T1qqqq_ctau")>=0:
        analyzerChain.append(
            EventSkim(selection=lambda event: 
                event.nllpinfo>0
            )
        )
        storeVariables.extend([
            [lambda tree: tree.branch("llp","I"),lambda tree,event: tree.fillBranch("llp",int(round(Collection(event,"llpinfo")[0].llp_mass/100.))*100)],
            [lambda tree: tree.branch("lsp","I"),lambda tree,event: tree.fillBranch("lsp",int(round(Collection(event,"llpinfo")[0].lsp_mass/100.))*100)],
        ])
        
    if args.inputFiles[0].find("madgraph")>=0 and \
    (args.inputFiles[0].find("DYJetsToLL")>=0 or \
    args.inputFiles[0].find("ZJetsToNuNu")>=0):
        analyzerChain.append(
            ZNLOWeights()
        )
        
    if args.inputFiles[0].find("DYJetsToLL")>=0 or \
    args.inputFiles[0].find("TTJets")>=0 or \
    args.inputFiles[0].find("TT_")>=0 or \
    args.inputFiles[0].find("WToLNu")>=0 or \
    args.inputFiles[0].find("WJetsToLNu")>=0:
        storeVariables.append([lambda tree: tree.branch("genHt","F"),lambda tree,event: tree.fillBranch("genHt",event.LHE_HTIncoming)])
        storeVariables.append([lambda tree: tree.branch("genNb","F"),lambda tree,event: tree.fillBranch("genNb",event.LHE_Nb)])
        storeVariables.append([lambda tree: tree.branch("genNc","F"),lambda tree,event: tree.fillBranch("genNc",event.LHE_Nc)])
        storeVariables.append([lambda tree: tree.branch("genNuds","F"),lambda tree,event: tree.fillBranch("genNuds",event.LHE_Nuds)])
        storeVariables.append([lambda tree: tree.branch("genNglu","F"),lambda tree,event: tree.fillBranch("genNglu",event.LHE_Nglu)])
        
    if args.inputFiles[0].find("DYJetsToLL")>=0 or \
    args.inputFiles[0].find("WToLNu")>=0 or \
    args.inputFiles[0].find("WJetsToLNu")>=0:
        storeVariables.append([lambda tree: tree.branch("genVpt","F"),lambda tree,event: tree.fillBranch("genVpt",event.LHE_Vpt)])
        
    '''
    for i in range(0,101):
        storeVariables.append([lambda tree: tree.branch("lheweight_%i"%i,"F"),lambda tree,event: tree.fillBranch("lheweight_%i"%i,event.LHEPdfWeight[i])])
    for i in range(0,9):
        storeVariables.append([lambda tree: tree.branch("scaleweight_%i"%i,"F"),lambda tree,event: tree.fillBranch("scaleweight_%i"%i,event.LHEScaleWeight[i])])
    '''
    
    storeVariables.append([lambda tree: tree.branch("genx1","F"),lambda tree,event: tree.fillBranch("genx1",event.Generator_x1)])
    storeVariables.append([lambda tree: tree.branch("genx2","F"),lambda tree,event: tree.fillBranch("genx2",event.Generator_x2)])
    storeVariables.append([lambda tree: tree.branch("genid1","F"),lambda tree,event: tree.fillBranch("genid1",event.Generator_id1)])
    storeVariables.append([lambda tree: tree.branch("genid2","F"),lambda tree,event: tree.fillBranch("genid2",event.Generator_id2)])
    storeVariables.append([lambda tree: tree.branch("genpdfscale","F"),lambda tree,event: tree.fillBranch("genpdfscale",event.Generator_scalePDF)])

    
    analyzerChain.append(
        EventInfo(
            storeVariables=storeVariables
        )
    )
    
    
        
    
else:
    analyzerChain.append(
        JetSelection(
            inputCollection=lambda event: Collection(event,"Jet"),
            leptonCollection=lambda event: event.tightMuons,
            outputName="selectedJets_nominal",
            jetMinPt = 30.,
            jetMaxEta = 2.4,
            storeKinematics=['pt','eta'],
        )
    )
    analyzerChain.append(
        JetSelection(
            inputCollection=lambda event: getattr(event,"selectedJets_nominal_unselected"),
            leptonCollection=lambda event: event.tightMuons,
            outputName="vetoFwdJets_nominal",
            jetMinPt = 50.,
            jetMaxEta = 5.0,
            storeKinematics=[],
        )
    )
        
    analyzerChain.append(
        EventSkim(selection=lambda event: 
            len(event.selectedJets_nominal)>=2
        )
    )
    
    analyzerChain.append(
        EventObservables(
            inputCollection = lambda event: event.selectedJets_nominal,
            metInput = lambda event: Object(event,"MET"),
            outputName = "nominal",
        )
    )
    analyzerChain.append(
        EventObservables(
            inputCollection = lambda event: event.selectedJets_nominal+event.tightMuons,
            metInput = lambda event: Object(event,"MET"),
            outputName = "nominal_lepton",
        )
    )
    '''
    #loose skim on ht/met (limits might use ht>1000 or (ht>200 && met>200))
    analyzerChain.append(
        EventSkim(selection=lambda event: 
            event.nominal_met>150.
        )
    )
    '''
    storeVariables = [
        [lambda tree: tree.branch("rho","F"),lambda tree,event: tree.fillBranch("rho",event.fixedGridRhoFastjetAll)], 
        [lambda tree: tree.branch("nPV","I"),lambda tree,event: tree.fillBranch("nPV",event.PV_npvsGood)],
        [lambda tree: tree.branch("nSV","I"),lambda tree,event: tree.fillBranch("nSV",event.nSV)],
        [
            lambda tree: tree.branch("MonoCentralPFJet80_PFMETNoMu_PFMHTNoMu_IDTight","I"),
            lambda tree,event: tree.fillBranch(
                "MonoCentralPFJet80_PFMETNoMu_PFMHTNoMu_IDTight",
                event.HLT_MonoCentralPFJet80_PFMETNoMu110_PFMHTNoMu110_IDTight*1+\
                event.HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight*2
            )
        ],
        [
            lambda tree: tree.branch("PFHT900","I"),
            lambda tree,event: tree.fillBranch("PFHT900",event.HLT_PFHT900)
        ],
    ]
    analyzerChain.append(
        EventInfo(
            storeVariables=storeVariables
        )
    )
    
analyzerChain.append(
    TaggerEvaluation(
        modelPath="PhysicsTools/NanoAODTools/data/nn/model_noda_retrain.pb",
        inputCollections=[
            lambda event: event.selectedJets_nominal
        ],
        taggerName="llpdnnx_noda",
        logctauValues = range(-3,5)
    )
)

analyzerChain.append(
    TaggerWorkingpoints(
        inputCollection = lambda event: event.selectedJets_nominal,
        taggerName = "llpdnnx_noda",
        outputName = "llpdnnx_noda_nominal",
        logctauValues = range(-3,5),
        predictionLabels = ["LLP"],
        globalOptions=globalOptions
    )
)

analyzerChain.append(
    TaggerEvaluation(
        modelPath="PhysicsTools/NanoAODTools/data/nn/model_singlemuon_retrain.pb",
        inputCollections=[
            lambda event: event.selectedJets_nominal
        ],
        taggerName="llpdnnx_da",
        logctauValues = range(-3,5)
    )
)

analyzerChain.append(
    TaggerWorkingpoints(
        inputCollection = lambda event: event.selectedJets_nominal,
        taggerName = "llpdnnx_da",
        outputName = "llpdnnx_da_nominal",
        logctauValues = range(-3,5),
        predictionLabels = ["LLP"],
        globalOptions=globalOptions
    )
)

p=PostProcessor(
    args.output[0],
    [args.inputFiles],
    cut="(nJet>0)",
    branchsel=None,
    maxEvents=-1,
    modules=analyzerChain,
    friend=True
)
p.run()
