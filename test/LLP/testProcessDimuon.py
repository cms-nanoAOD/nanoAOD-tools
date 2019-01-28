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
    DataFlag(
        globalOptions=globalOptions
    ),
    EventSkim(selection=lambda event: event.ntightMuons==2),
    EventSkim(selection=lambda event: event.nvetoMuons==0),
    EventSkim(selection=lambda event: event.nvetoElectrons==0),
    EventSkim(selection=lambda event: event.IsoMuTrigger_flag==1),
    
    InvariantSystem(
        inputCollection = lambda event: event.tightMuons,
        outputName = "dimuon",
    ),
    
    EventSkim(selection=lambda event: event.dimuon_mass>=50. and math.fabs(event.dimuon_mass-90.)>15),
    
]

analyzerChain = []

analyzerChain.append(
    MetFilter(
        globalOptions=globalOptions
    )
)


analyzerChain.extend(muonSelection)


analyzerChain.append(
    JetSelection(
        inputCollection=lambda event: Collection(event,"Jet"),
        leptonCollection=lambda event: event.tightMuons,
        outputName="selectedJets_nominal",
        jetMinPt = 30.,
        jetMaxEta = 2.4,
        dRCleaning = 0.4,
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
        len(event.selectedJets_nominal)>=2 and len(event.selectedJets_nominal)<=6 and len(event.vetoFwdJets_nominal)==0
    )
)

analyzerChain.append(
    EventObservables(
        jetInputCollection = lambda event: event.selectedJets_nominal,
        metInput = lambda event: Object(event,"MET"),
        outputName = "nominal",
    )
)

analyzerChain.append(
    EventSkim(selection=lambda event: 
        event.nominal_met>10. and event.nominal_met<250.
    )
)

analyzerChain.append(
    JetSelection(
        inputCollection=lambda event: event.selectedJets_nominal,
        leptonCollection=lambda event: event.tightMuons,
        jetMinPt = 30.,
        jetMaxEta = 2.4,
        dRCleaning = 0.4,
        outputName="Jet",
        addSize=False,
        flagDA=True,
        storeKinematics=[]#['pt','eta'],
    )
)

p=PostProcessor(
    args.output[0],
    [args.inputFiles],
    cut=None,
    branchsel=None,
    maxEvents=-1,
    modules=analyzerChain,
    friend=False
)
p.run()
