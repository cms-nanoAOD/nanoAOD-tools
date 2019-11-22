import os
import sys
import math
import json
import ROOT
import random

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class InvariantSystem(Module):
    def __init__(
        self,
        inputCollection = lambda event: Collection(event, "Muon"),
        outputName = "sys",
        globalOptions={"isData":False}
    ):
        self.inputCollection = inputCollection
        self.outputName = outputName
        self.globalOptions = globalOptions
        
        
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch(self.outputName+"_mass","F")
        self.out.branch(self.outputName+"_pt","F")
        self.out.branch(self.outputName+"_eta","F")
        self.out.branch(self.outputName+"_deltaR","F")
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        collection = self.inputCollection(event)
        vec = ROOT.TLorentzVector()
        for obj in collection:
            vec+=obj.p4()

        self.out.fillBranch(self.outputName+"_deltaR", collection[0].p4().DeltaR(collection[1].p4()))
        self.out.fillBranch(self.outputName+"_mass",vec.M())
        self.out.fillBranch(self.outputName+"_pt",vec.Pt())
        self.out.fillBranch(self.outputName+"_eta",vec.Eta())
        
        return True
        
        
