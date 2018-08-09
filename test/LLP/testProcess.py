import os
import sys
import math
import json
import ROOT
import random
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
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
        globalOptions=globalOptions
    ),
    MuonVeto(
        inputCollection=lambda event: event["tightMuons_unselected"],
        globalOptions=globalOptions
    ),
    SingleMuonTriggerSelection(
        inputCollection=lambda event: event["tightMuons"],
        outputName="IsoMuTrigger",
        globalOptions=globalOptions
    ),
    EventSkim(selection=lambda event: len(event.tightMuons)==1)
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
        ("jerUp",lambda event: event.jets_jerUp),
        ("jerDown",lambda event: event.jets_jerDown),
        ("jesUp",lambda event: event.jets_jesUp["Total"]),
        ("jesDown",lambda event: event.jets_jesDown["Total"]),
    ]:
        analyzerChain.append(
            JetSelection(
                inputCollection=collection,
                outputName="selectedJets_"+systName,
                storeKinematics=['pt','eta'],
            )
        )
        
    analyzerChain.append(
        EventSkim(selection=lambda event: 
            len(event.selectedJets_nominal)>=2 or \
            len(event.selectedJets_jerUp)>=2 or \
            len(event.selectedJets_jerDown)>=2 or \
            len(event.selectedJets_jesUp)>=2 or \
            len(event.selectedJets_jesDown)>=2
        )
    )
    
    for systName,jetCollection,metObject in [
        ("nominal",lambda event: event.jets_nominal,lambda event: event.met_nominal),
        ("jerUp",lambda event: event.jets_jerUp,lambda event: event.met_jerUp),
        ("jerDown",lambda event: event.jets_jerDown,lambda event: event.met_jerDown),
        ("jesUp",lambda event: event.jets_jesUp["Total"],lambda event: event.met_jesUp["Total"]),
        ("jesDown",lambda event: event.jets_jesDown["Total"],lambda event: event.met_jesDown["Total"]),
        ("unclEnUp",lambda event: event.jets_nominal,lambda event: event.met_unclEnUp),
        ("unclEnDown",lambda event: event.jets_nominal,lambda event: event.met_unclEnDown),
    ]:
    
        analyzerChain.append(
            EventObservables(
                jetInputCollection = jetCollection,
                metInput = metObject,
                outputName = systName,
            )
        )
    
    #loose skim on ht/met (limits might use ht>1000 or (ht>200 && met>200))
    analyzerChain.append(
        EventSkim(selection=lambda event: 
            event.met_nominal>150 or \
            event.met_jerUp>150 or \
            event.met_jerDown>150 or \
            event.met_jesUp>150 or \
            event.met_jesDown>150 or \
            event.met_unclEnUp>150 or \
            event.met_unclEnDown>150
        )
    )
    
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
    
    analyzerChain.append(
        TaggerEvaluation(
            modelPath="model_parametric.pb",
            inputCollections=[
                lambda event: event.selectedJets_nominal,
                lambda event: event.selectedJets_jerUp,
                lambda event: event.selectedJets_jerDown,
                lambda event: event.selectedJets_jesUp,
                lambda event: event.selectedJets_jesDown
            ],
            taggerName="llpdnnx",
            logctauValues = range(-3,5)
        )
    )
    
    analyzerChain.append(
        TaggerWorkingpoints(
            inputCollection = lambda event: event.selectedJets_nominal,
            taggerName = "llpdnnx",
            outputName = "llpdnnx_nominal",
            logctauValues = range(-3,5),
            globalOptions=globalOptions
        )
    ),
    analyzerChain.append(
        EventInfo(
            storeVariables = [
                [lambda tree: tree.branch("genweight","F"),lambda tree,event: tree.fillBranch("genweight",event.Generator_weight)],
                [lambda tree: tree.branch("genHt","F"),lambda tree,event: tree.fillBranch("genHt",event.LHE_HTIncoming)],
                [lambda tree: tree.branch("rho","F"),lambda tree,event: tree.fillBranch("rho",event.fixedGridRhoFastjetAll)], 
                [lambda tree: tree.branch("nPV","I"),lambda tree,event: tree.fillBranch("nPV",event.PV_npvsGood)],
                [lambda tree: tree.branch("nSV","I"),lambda tree,event: tree.fillBranch("nSV",event.nSV)],
            ]
        )
    )
    

p=PostProcessor(
    args.output[0],
    [args.inputFiles],
    cut=None,
    branchsel=None,
    modules=analyzerChain,
    friend=True
)
p.run()
