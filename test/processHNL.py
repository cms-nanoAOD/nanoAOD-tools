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
parser.add_argument('--year', dest='year', action='store',type=int, default=2016)
parser.add_argument('--input', dest='inputFiles', action='append',default=[])
parser.add_argument('output', nargs=1)

args = parser.parse_args()

print "isData:",args.isData
print "year:",args.year
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
    "isData":args.isData,
    "year":args.year
}


muonSelection = [
    MuonSelection(
        outputName="tightMuons",
        storeKinematics=['pt','eta', 'dxy', 'dxyErr', 'dz', 'dzErr'],
        storeWeights=True,
        muonMinPt = 25.,
        muonMaxDxy = 0.002,
        muonMaxDz = 0.01,
        muonID = MuonSelection.TIGHT,
        muonIso = MuonSelection.TIGHT,
        globalOptions=globalOptions
    ),
    MuonSelection(
        inputCollection = lambda event: event.tightMuons_unselected,
        outputName="looseMuons",
        storeKinematics=['pt','eta', 'dxy', 'dxyErr', 'dz', 'dzErr'],
        storeWeights=False,
        muonMinPt = 5.,
        muonMinDxy = 0.02,
        muonID = MuonSelection.LOOSE,
        muonIso = MuonSelection.NONE,
        globalOptions=globalOptions
    ),
    
    SingleMuonTriggerSelection(
        inputCollection=lambda event: event["tightMuons"],
        outputName="IsoMuTrigger",
        storeWeights=False,
        globalOptions=globalOptions
    ),
    EventSkim(selection=lambda event: event.IsoMuTrigger_flag==1, outputName="WeightIsoMu24"),
    EventSkim(selection=lambda event: event.ntightMuons>0, outputName="WeightPromptMuon"),
    EventSkim(selection=lambda event: event.nlooseMuons>0, outputName="WeightDisplacedMuon"),
]

analyzerChain = []

analyzerChain.extend(muonSelection)

analyzerChain.append(
    JetSelection(
        outputName="selJets",
        jetMinPt = 15.,
        jetMaxEta = 2.4,
        storeKinematics=['pt','eta', 'phi'],
    )
)


storeVariables = [
    [lambda tree: tree.branch("genweight","F"),lambda tree,event: tree.fillBranch("genweight",event.Generator_weight)],
]


analyzerChain.append(
    EventInfo(
        storeVariables=storeVariables
    )
)

analyzerChain.append(
    EventSkim(selection=lambda event: len(event.selJets)>0,outputName="WeightJet"
        )
)


analyzerChain.append(
    InvariantSystem(
        inputCollection = lambda event: [event.looseMuons[0] if len(event.looseMuons) > 0 else None, event.tightMuons[0] if len(event.tightMuons) > 0 else None],
        outputName = "dimuon"
    )
)

analyzerChain.append(
    LepJetFinder(
        jetCollection = lambda event: event.selJets,
        leptonCollection = lambda event: event.looseMuons,
    )
)
 
analyzerChain.append(
    EventSkim(selection=lambda event: event.lepJet_deltaR<0.4,
        outputName="Weight_lepJet"
        )
)


analyzerChain.append(
    EventSkim(selection=lambda event: 
        event.dimuon_mass > 20 and event.dimuon_mass < 85,
        outputName = "Weight_diMuonMass"
    )
)
  
analyzerChain.append(
    EventSkim(selection=lambda event: 
        event.dimuon_deltaR > 1 and event.dimuon_deltaR < 5,
        outputName = "Weight_diMuon_DeltaR"
    )
)


'''
analyzerChain.append(
    TaggerEvaluation(
        modelPath="PhysicsTools/NanoAODTools/data/nn/da.pb",
        inputCollections=[
            lambda event: event.lepJet
        ],
        taggerName="llpdnnx",
        logctauValues = range(0,5)
    )
)

analyzerChain.append(
    JetTruthFlags(inputCollection= lambda event: event.lepJet
    )
)

analyzerChain.append(
    JetTaggerResult(
        inputCollection = lambda event: event.lepJet,
        taggerName = "llpdnnx",
        predictionLabels = ["LLP"],
        logctauValues = range(0,5)
    )
)

'''
p=PostProcessor(
    args.output[0],
    [args.inputFiles],
    cut="",
    branchsel=None,
    maxEvents=-1,
    modules=analyzerChain,
    friend=True
)
p.run()
