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
parser.add_argument('--year', dest='year', action='store',default=2016, type=int)
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
    "isData":False,
    "year":args.year
}

leptonSelection = [
    MuonSelection(
        outputName="looseMuons",
        storeKinematics=['pt','eta'],
        storeWeights=True,
        muonMinPt = [26.,15.],
        muonID = MuonSelection.LOOSE,
        muonIso = MuonSelection.LOOSE,
        globalOptions=globalOptions
    )
]

analyzerChain = []

analyzerChain.append(JetFeatures(outputName="preselectedJets"))

analyzerChain.extend(leptonSelection)

analyzerChain.append(
    JetSelection(
        inputCollection=lambda event: event.preselectedJets,
        leptonCollection=lambda event: event.looseMuons,
        outputName="selectedJets",
        jetMinPt = 30.,
        jetMaxEta = 2.4,
        storeKinematics=['pt','eta', 'btagDeepB', 'btagDeepFlavB', 'btagCSVV2', 'chEmEF', 'chHEF', 'neEmEF', 'neHEF', 'nConstituents', 'nsv', 'ncpf', 'nnpf'],
    )
)

analyzerChain.append(
        JetTruthFlags(
            inputCollection = lambda event: event.selectedJets,            
            outputName = "selectedJets"
    )
)
    
analyzerChain.append(
    EventSkim(selection=lambda event: 
        len(event.selectedJets)>0
    )
)
  
storeVariables = [
        [lambda tree: tree.branch("genweight","F"),lambda tree,event: tree.fillBranch("genweight",event.Generator_weight)],
        [lambda tree: tree.branch("rho","F"),lambda tree,event: tree.fillBranch("rho",event.fixedGridRhoFastjetAll)], 
        [lambda tree: tree.branch("nPV","I"),lambda tree,event: tree.fillBranch("nPV",event.PV_npvsGood)],
        [lambda tree: tree.branch("nSV","I"),lambda tree,event: tree.fillBranch("nSV",event.nSV)],
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
 
analyzerChain.append(
    MetFilter(
        globalOptions=globalOptions
    )
)

   
 
analyzerChain.append(
    EventInfo(
        storeVariables=storeVariables
    )
)

analyzerChain.append(
    TaggerEvaluation(
        modelPath="PhysicsTools/NanoAODTools/data/nn/noda.pb",
        inputCollections=[
            lambda event: event.selectedJets
        ],
        taggerName="llpdnnx_noda",
    )
)

analyzerChain.append(
    JetTaggerResult(
        inputCollection = lambda event: event.selectedJets,
        taggerName = "llpdnnx_noda",
        predictionLabels = ["LLP", "B"],
    )
)
analyzerChain.append(
    TaggerEvaluation(
        modelPath="PhysicsTools/NanoAODTools/data/nn/da.pb",
        inputCollections=[
            lambda event: event.selectedJets,
        ],
        taggerName="llpdnnx_da",
    )
)

analyzerChain.append(
    JetTaggerResult(
        inputCollection = lambda event: event.selectedJets,
        taggerName = "llpdnnx_da",
        predictionLabels = ["LLP", "B"],
    )
)

analyzerChain.append(
    LegacyTagger(
        inputCollection = lambda event: event.selectedJets,
    )
)
 

p=PostProcessor(
    args.output[0],
    [args.inputFiles],
    modules=analyzerChain,
    maxEvents=-1,
    friend=True
)
p.run()
