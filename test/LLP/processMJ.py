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
        globalOptions=globalOptions
    ),
    ElectronVeto(
        inputCollection=lambda event: Collection(event,"Electron"),
        globalOptions=globalOptions
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

analyzerChain.append(
    SignalTriggerSelection(
        globalOptions=globalOptions
        )
    )

analyzerChain.extend(muonSelection)

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
            leptonCollection=lambda event: [],
            outputName="selectedJets_"+systName,
            jetMinPt = 30.,
            jetMaxEta = 2.4,
            storeKinematics=['pt','eta'],
        )
    )
    analyzerChain.append(
        JetSelection(
            inputCollection=lambda event,systName=systName: getattr(event,"selectedJets_"+systName+"_unselected"),
            leptonCollection=lambda event: [],
            outputName="vetoFwdJets_"+systName,
            jetMinPt = 50.,
            jetMaxEta = 5.0,
            storeKinematics=[],
        )
    )

analyzerChain.append(
    EventSkim(selection=lambda event: 
        len(event.selectedJets_nominal)>=3 and len(event.vetoFwdJets_nominal)==0)
        #len(event.selectedJets_jerUp)>=2 or \
        #len(event.selectedJets_jerDown)>=2 or \
        #len(event.selectedJets_jesTotalUp)>=2 or \
        #len(event.selectedJets_jesTotalDown)>=2
)

for systName,jetCollection,metObject in [
    ("nominal",lambda event: event.selectedJets_nominal,lambda event: event.met_nominal),
    #("jerUp",lambda event: event.selectedJets_jerUp,lambda event: event.met_jerUp),
    #("jerDown",lambda event: event.selectedJets_jerDown,lambda event: event.met_jerDown),
    #("jesTotalUp",lambda event: event.selectedJets_jesTotalUp,lambda event: event.met_jesUp["Total"]),
    #("jesTotalDown",lambda event: event.selectedJets_jesTotalDown,lambda event: event.met_jesDown["Total"]),
    #("unclEnUp",lambda event: event.selectedJets_nominal,lambda event: event.met_unclEnUp),
    #("unclEnDown",lambda event: event.selectedJets_nominal,lambda event: event.met_unclEnDown),
]:

    analyzerChain.append(
        EventObservables(
            jetInputCollection = jetCollection,
            metInput = metObject,
            outputName = systName,
        )
    )

analyzerChain.append(
    EventSkim(selection=lambda event: 
        event.nominal_mht>200.
        #event.jerUp_met>150. or \
        #event.jerDown_met>150. or \
        #event.jesTotalUp_met>150. or \
        #event.jesTotalDown_met>150. or \
        #event.unclEnUp_met>150. or \
        #event.unclEnDown_met>150.
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
        modelPath="PhysicsTools/NanoAODTools/data/nn/model_bothmuon_retrain.pb",
        inputCollections=[
            lambda event: event.selectedJets_nominal,
            #lambda event: event.selectedJets_jerUp,
            #lambda event: event.selectedJets_jerDown,
            #lambda event: event.selectedJets_jesTotalUp,
            #lambda event: event.selectedJets_jesTotalDown,
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
        globalOptions=globalOptions
    )
)

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
