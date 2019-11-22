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
muonSelection = [
    MuonVeto(
        inputCollection=lambda event: Collection(event,"Muon"),
    ),
    ElectronVeto(
        inputCollection=lambda event: Collection(event,"Electron"),
    ),
    
    EventSkim(selection=lambda event: event.nvetoMuons==0, outputName="vetoMuonsSkim"),
    EventSkim(selection=lambda event: event.nvetoElectrons==0, outputName="vetoElectronsSkim"),

]

analyzerChain = []
 
if args.inputFiles[0].find("SMS-T1qqqq_ctau")>=0:
    analyzerChain.append(
        EventSkim(selection=lambda event: 
            event.nllpinfo>0
        )
    )
     
    storeVariables = [
                [lambda tree: tree.branch("llp","I"),lambda tree,event: tree.fillBranch("llp",int(round(Collection(event,"llpinfo")[0].llp_mass/100.))*100)],
                [lambda tree: tree.branch("lsp","I"),lambda tree,event: tree.fillBranch("lsp",int(round(Collection(event,"llpinfo")[0].lsp_mass/100.))*100)]
    ]
        
    analyzerChain.append(
        EventInfo(
            storeVariables=storeVariables
        )
    )


analyzerChain.append(MetFilter(outputName="metFilterSkim"))

analyzerChain.extend(muonSelection)

analyzerChain.append(
    JetSelection(
        leptonCollection=lambda event: [],
        outputName="selectedJets_nominal",
        jetMinPt = 30.,
        jetMaxEta = 2.4,
        storeKinematics=[],
    )
)

analyzerChain.append(
    JetSelection(
        inputCollection=lambda event: event.selectedJets_nominal_unselected,
        leptonCollection=lambda event: [],
        outputName="vetoFwdJets_nominal",
        jetMinPt = 50.,
        jetMaxEta = 5.0,
        storeKinematics=[],
    )
)

analyzerChain.append(
    JetSelection(
        inputCollection=lambda event: event.vetoFwdJets_nominal_unselected,
        leptonCollection=lambda event: [],
        outputName="vetoLooseIdJets_nominal",
        jetMinPt = 30.,
        jetMaxEta = 5.0,
        jetId = -1,
        storeKinematics=[],
    )
)

analyzerChain.append(
    EventSkim(selection=lambda event: 
        len(event.selectedJets_nominal)>=3,
        outputName="jetSkim"
    )
)

analyzerChain.append(
    EventSkim(selection=lambda event: 
        len(event.vetoFwdJets_nominal)==0,
        outputName="vetoFwdJetSkim"
    )
)

analyzerChain.append(
    EventSkim(selection=lambda event: 
        len(event.vetoLooseIdJets_nominal)==0,
        outputName="vetoLooseIdJetSkim"
    )
)
analyzerChain.append(
    EventObservables(
        jetInputCollection = lambda event: event.selectedJets_nominal,
        outputName = "nominal",
    )
)

analyzerChain.append(
    EventSkim(selection=lambda event: 
        event.nominal_mht>300.,
        outputName="mhtSkim"
    )
)

analyzerChain.append(
    EventSkim(selection=lambda event: 
        event.nominal_mht/event.nominal_met<1.25,
        outputName="mhtovermetSkim"
    )
)
analyzerChain.append(
    EventSkim(selection=lambda event: 
        event.nominal_minPhi>0.2,
        outputName="minPhiSkim"
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
