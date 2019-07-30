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
parser.add_argument('--input', dest='inputFiles', action='append',default=[])
parser.add_argument('output', nargs=1)

args = parser.parse_args()

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
    "isData": False
}

muonSelection = [
    MuonVeto(
        inputCollection=lambda event: Collection(event,"Muon"),
    ),
    ElectronVeto(
        inputCollection=lambda event: Collection(event,"Electron"),
    ),
    
    EventSkim(selection=lambda event: event.nvetoMuons==0),
    EventSkim(selection=lambda event: event.nvetoElectrons==0),

]

analyzerChain = []

analyzerChain.append(
    MetFilter(
        globalOptions=globalOptions
    )
)

analyzerChain.append(MetFilter(outputName="metFilterSkim"))

analyzerChain.extend(muonSelection)

analyzerChain.append(
    JetSelection(
        outputName="selectedJets_nominal",
        jetMinPt = 30.,
        jetMaxEta = 2.4,
        storeKinematics=[],
    )
)

analyzerChain.append(
    JetSelection(
        inputCollection=lambda event: event.selectedJets_nominal_unselected,
        outputName="vetoFwdJets_nominal",
        jetMinPt = 50.,
        jetMaxEta = 5.0,
        storeKinematics=[],
    )
)

analyzerChain.append(
    EventSkim(selection=lambda event: 
        len(event.selectedJets_nominal)>=3,
    )
)

analyzerChain.append(
    EventSkim(selection=lambda event: 
        len(event.vetoFwdJets_nominal)==0,
    )
)

analyzerChain.append(
    EventObservables(
        jetCollection = lambda event: event.selectedJets_nominal,
        outputName = "nominal",
    )
)

analyzerChain.append(
    EventSkim(selection=lambda event: 
        event.nominal_mht>270.,
    )
)
   
analyzerChain.append(
    TaggerEvaluation(
        modelPath="PhysicsTools/NanoAODTools/data/nn/model_bothmuon_retrain.pb",
        inputCollections=[
            lambda event: event.selectedJets_nominal,
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
        globalOptions=globalOptions,
        saveAllLabels=True
    )
)


analyzerChain.extend([
    PileupWeight(
        dataFile = os.path.expandvars("$CMSSW_BASE/src/PhysicsTools/NanoAODTools/data/pu/PU69000.root"),
        outputName ="puweight",
        processName = "TT_TuneCUETP8M2T4_13TeV-powheg-pythia8-evtgen",
        globalOptions=globalOptions
    )
])

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
