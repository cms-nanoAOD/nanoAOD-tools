import os
import sys
import math
import json
import ROOT
import random

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from utils import deltaR,deltaPhi

class EventObservables(Module):

    def __init__(
        self,
        jetInputCollection = lambda event: Collection(event, "Jet"),
        metInput = lambda event: Object(event, "MET"),
        outputName = "centralJets",
        globalOptions={"isData":False}
    ):
        self.globalOptions = globalOptions
        self.jetInputCollection = jetInputCollection
        self.metInput = metInput
        self.outputName = outputName

    def beginJob(self):
        pass
        
    def endJob(self):
        pass
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch(self.outputName+"_ht","F")
        self.out.branch(self.outputName+"_mht","F")
        self.out.branch(self.outputName+"_mass","F")
        self.out.branch(self.outputName+"_met","F")
        self.out.branch(self.outputName+"_minPhi","F")
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = self.jetInputCollection(event)
        met = self.metInput(event)
        jetVectorSum = ROOT.TLorentzVector()
        jetScalarPtSum = 0.0
        for jet in jets:
            jetVectorSum+=jet.p4()
            jetScalarPtSum+=jet.pt
            
        self.out.fillBranch(self.outputName+"_ht",jetScalarPtSum)
        setattr(event,self.outputName+"_ht",jetScalarPtSum)
        self.out.fillBranch(self.outputName+"_mht",jetVectorSum.Pt())
        setattr(event,self.outputName+"_mht",jetVectorSum.Pt())
        self.out.fillBranch(self.outputName+"_mass",jetVectorSum.M())
        setattr(event,self.outputName+"_mass",jetVectorSum.M())
        self.out.fillBranch(self.outputName+"_met",met.pt)
        setattr(event,self.outputName+"_met",met.pt)
        
        minPhi = math.pi
        for jet in jets:
            negSum = -(jetVectorSum-jet.p4())
            minPhi = min(minPhi,math.fabs(deltaPhi(negSum.Phi(),jet.phi)))
        self.out.fillBranch(self.outputName+"_minPhi",minPhi)
        setattr(event,self.outputName+"_minPhi",minPhi)
        return True
        
