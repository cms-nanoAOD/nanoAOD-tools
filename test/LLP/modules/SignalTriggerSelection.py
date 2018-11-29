import os
import sys
import math
import json
import ROOT
import random

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class SignalTriggerSelection(Module):
    def __init__(
        self,
        outputName = "signalTrigger",
        globalOptions={"isData":False}
    ):
        self.globalOptions = globalOptions
        self.outputName = outputName
        
    def beginJob(self):
        pass
        
    def endJob(self):
        pass
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        self.out.branch(self.outputName+"_flag","I")
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
            
        self.out.fillBranch(
            self.outputName+"_flag",
            event.HLT_MonoCentralPFJet80_PFMETNoMu90_PFMHTNoMu90_IDTight > 0 or
            event.HLT_MonoCentralPFJet80_PFMETNoMu100_PFMHTNoMu100_IDTight > 0 or
            event.HLT_MonoCentralPFJet80_PFMETNoMu110_PFMHTNoMu110_IDTight > 0 or
            event.HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight > 0 or
            event.HLT_PFHT900
        )
            
        return True
        
