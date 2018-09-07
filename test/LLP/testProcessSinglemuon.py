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
        muonMinPt = 26.,
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
    EventSkim(selection=lambda event: event.ntightMuons==1),
    EventSkim(selection=lambda event: event.nvetoMuons==0),
    EventSkim(selection=lambda event: event.nvetoElectrons==0),
    EventSkim(selection=lambda event: event.IsoMuTrigger_flag==1),
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
                outputName="selectedJets_"+systName,
                storeKinematics=['pt','eta'],
            )
        )
        
   
    
    analyzerChain.append(
        EventSkim(selection=lambda event: 
            len(event.selectedJets_nominal)>=2 and len(event.selectedJets_nominal)<6#or \
            #len(event.selectedJets_jerUp)>=2 or \
            #len(event.selectedJets_jerDown)>=2 or \
            #len(event.selectedJets_jesTotalUp)>=2 or \
            #len(event.selectedJets_jesTotalDown)>=2
        )
    )
    
    analyzerChain.append(
        JetSelection(
            inputCollection=lambda event: event.selectedJets_nominal,
            outputName="Jet",
            addSize=False,
            flagDA=True,
            storeKinematics=[]#['pt','eta'],
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
                jetInputCollection = jetCollection,
                metInput = metObject,
                outputName = systName,
            )
        )
    
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
    if args.inputFiles[0].find("DYJetsToLL")>=0 or args.inputFiles[0].find("TTJets")>=0:
        storeVariables.append([lambda tree: tree.branch("genHt","F"),lambda tree,event: tree.fillBranch("genHt",event.LHE_HTIncoming)])
    
    
    analyzerChain.append(
        EventInfo(
            storeVariables=storeVariables
        )
    )
    
else:
    analyzerChain.append(
        JetSelection(
            inputCollection=lambda event: Collection(event,"Jet"),
            outputName="selectedJets_nominal",
            storeKinematics=['pt','eta'],
        )
    )

    analyzerChain.append(
        EventSkim(selection=lambda event: 
            len(event.selectedJets_nominal)>=2 and len(event.selectedJets_nominal)<6
        )
    )
    
    analyzerChain.append(
        JetSelection(
            inputCollection=lambda event: event.selectedJets_nominal,
            outputName="Jet",
            addSize=False,
            flagDA=True,
            storeKinematics=[]#['pt','eta'],
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
            event.nominal_met>150.
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
