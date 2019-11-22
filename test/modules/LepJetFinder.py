import os
import sys
import math
import json
import ROOT
import random

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class LepJetFinder(Module):
    def __init__(
        self,
        jetCollection,
        leptonCollection,
        outputName = "lepJet",
    ):
        self.jetCollection = jetCollection
        self.leptonCollection = leptonCollection
        self.outputName = outputName
        
        
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch(self.outputName+"_pt","F")
        self.out.branch(self.outputName+"_eta","F")
        self.out.branch(self.outputName+"_phi","F")
        self.out.branch(self.outputName+"_deltaR","F")
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        jetCollection = self.jetCollection(event)
        leptonCollection = self.leptonCollection(event)

        lepton = leptonCollection[0]
        jet = jetCollection[0]
        deltaR = lepton.p4().DeltaR(jet.p4())

        for _jet in jetCollection:
            _deltaR = lepton.p4().DeltaR(_jet.p4())
            if _deltaR < deltaR:
                jet = _jet
                deltaR = _deltaR

        self.out.fillBranch(self.outputName+"_pt",jet.pt)
        self.out.fillBranch(self.outputName+"_eta",jet.eta)
        self.out.fillBranch(self.outputName+"_phi",jet.phi)
        self.out.fillBranch(self.outputName+"_deltaR",deltaR)

        setattr(event, self.outputName, [jet])
        
        return True
