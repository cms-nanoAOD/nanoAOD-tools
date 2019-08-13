import os
import sys
import math
import json
import ROOT
import random

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class MuonVeto(Module):

    def __init__(
        self,
        inputCollection = lambda event: Collection(event, "Muon"),
        outputName = "vetoMuons",
        muonMinPt = 10.,
        muonMaxEta = 2.4,
        globalOptions={"isData":False}
    ):
        self.globalOptions = globalOptions
        self.inputCollection = inputCollection
        self.outputName = outputName
        self.muonMinPt = muonMinPt
        self.muonMaxEta = muonMaxEta
 
    def beginJob(self):
        pass
        
    def endJob(self):
        pass
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("n"+self.outputName,"I")
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        muons = self.inputCollection(event)
        
        selectedMuons = []
        unselectedMuons = []
        
        #https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonIdRun2#Tight_Muon
        for muon in muons:
            if muon.pt>self.muonMinPt and math.fabs(muon.eta)<self.muonMaxEta and muon.isPFcand==1 and (muon.pfRelIso04_all<0.25):
                selectedMuons.append(muon)
            else:
                unselectedMuons.append(muon)
  
        self.out.fillBranch("n"+self.outputName,len(selectedMuons))
        
        setattr(event,self.outputName,selectedMuons)
        setattr(event,self.outputName+"_unselected",unselectedMuons)

        return True
        
