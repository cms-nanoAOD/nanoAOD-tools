import os
import sys
import math
import json
import ROOT
import random

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from utils import getHist,combineHist2D,getSFPtEta

class SingleMuonTriggerSelection(Module):
    def __init__(
        self,
        inputCollection = lambda event: getattr(event,"tightMuons"),
        storeWeights=True,
        outputName = "IsoMuTrigger",
        globalOptions={"isData":False}
    ):
        self.globalOptions = globalOptions
        self.inputCollection = inputCollection
        self.outputName = outputName
        self.storeWeights = storeWeights
        
        '''
        if not self.globalOptions["isData"]:
            triggerSFBToF = getHist(
                "PhysicsTools/NanoAODTools/data/muon/2016/trigger_EfficienciesAndSF_RunBtoF.root",
                "IsoMu24_OR_IsoTkMu24_PtEtaBins/pt_abseta_ratio"
            )
            triggerSFGToH = getHist(
                "PhysicsTools/NanoAODTools/data/muon/trigger_EfficienciesAndSF_RunGtoH.root",
                "IsoMu24_OR_IsoTkMu24_PtEtaBins/pt_abseta_ratio"
            )
            self.triggerSFHist = combineHist2D(
                triggerSFBToF,
                triggerSFGToH,
                1.-16226.5/35916.4,
                16226.5/35916.4
            )
        '''
            
    def beginJob(self):
        pass
        
    def endJob(self):
        pass
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        self.out.branch(self.outputName+"_flag","I")
        
        if not self.globalOptions["isData"] and self.storeWeights:
            self.out.branch(self.outputName+"_weight_trigger_nominal","F")
            self.out.branch(self.outputName+"_weight_trigger_up","F")
            self.out.branch(self.outputName+"_weight_trigger_down","F")
            
            
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        muons = self.inputCollection(event)
        
        weight_trigger_nominal = 1.
        weight_trigger_up = 1.
        weight_trigger_down = 1.
        
        if (not self.globalOptions["isData"]) and len(muons)>0 and self.storeWeights: 
            #take the leading muon here; note: technically correct would be to match to HLT obj
            weight_trigger,weight_trigger_err = getSFPtEta(self.triggerSFHist,muons[0].pt,muons[0].eta)
            weight_trigger_nominal*=weight_trigger
            weight_trigger_up*=(weight_trigger+weight_trigger_err)
            weight_trigger_down*=(weight_trigger-weight_trigger_err)
            
        self.out.fillBranch(
            self.outputName+"_flag",
            event.HLT_IsoMu24>0 or event.HLT_IsoTkMu24>0
        )
            
        if not self.globalOptions["isData"] and self.storeWeights:
            self.out.fillBranch(self.outputName+"_weight_trigger_nominal",weight_trigger_nominal)
            self.out.fillBranch(self.outputName+"_weight_trigger_up",weight_trigger_up)
            self.out.fillBranch(self.outputName+"_weight_trigger_down",weight_trigger_down)

        return True
        
