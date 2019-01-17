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

globalOptions = {"isData":False}

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

analyzerChain.extend(leptonSelection)

analyzerChain.append(
    JetSelection(
        inputCollection=lambda event:Collection(event,"Jet"),
        leptonCollection=lambda event: event.looseMuons,
        outputName="selectedJets",
        jetMinPt = 30.,
        jetMaxEta = 2.4,
        storeKinematics=['pt','eta','btagCMVA', 'btagCSVV2', 'btagDeepB']
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
    EventInfo(
        storeVariables=storeVariables
    )
)

analyzerChain.append(
    TaggerEvaluation(
        modelPath="PhysicsTools/NanoAODTools/data/nn/model_noda_retrain.pb",
        inputCollections=[
            lambda event: event.selectedJets
        ],
        taggerName="llpdnnx_noda",
        logctauValues = range(-3,5)
    )
)
'''

analyzerChain.append(
    TaggerWorkingpoints(
        inputCollection = lambda event: event.selectedJets,
        taggerName = "llpdnnx_noda",
        outputName = "llpdnnx_noda_nominal",
        logctauValues = range(-3,5),
        globalOptions=globalOptions,
        saveAllLabels=True
    )
)

analyzerChain.append(
    TaggerEvaluation(
        modelPath="PhysicsTools/NanoAODTools/data/nn/model_bothmuon_retrain.pb",
        inputCollections=[
            lambda event: event.selectedJets,
        ],
        taggerName="llpdnnx_da",
        logctauValues = range(-3,5)
    )
)
analyzerChain.append(
    TaggerWorkingpoints(
        inputCollection = lambda event: event.selectedJets,
        taggerName = "llpdnnx_da",
        outputName = "llpdnnx_da_nominal",
        logctauValues = range(-3,5),
        globalOptions=globalOptions,
        saveAllLabels=True
    )
)
'''

p=PostProcessor(
    args.output[0],
    [args.inputFiles],
    cut=None,
    branchsel=None,
    maxEvents=-1,
    modules=analyzerChain,
    friend=True
)
p.run()
