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
        globalOptions=globalOptions
    ),
    MuonVeto(
        inputCollection=lambda event: event["tightMuons"],
        globalOptions=globalOptions
    ),
    MuonTriggerSelection(
        inputCollection=lambda event: event["tightMuons"],
        outputName="IsoMuTrigger",
        globalOptions=globalOptions
    )
]

analyzerChain = []

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
                outputName="selectedJets_"+systName
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
