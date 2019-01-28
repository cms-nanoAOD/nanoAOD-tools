import os
import sys
import math
import json
import ROOT
import random

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from utils import getHist, getX

class SignalTriggerSelection(Module):
    def __init__(
        self,
        outputName = "signalTrigger",
        globalOptions={"isData":False}
    ):
        self.globalOptions = globalOptions
         
        if not self.globalOptions["isData"]:
            self.trigger_nominal = getHist("PhysicsTools/NanoAODTools/data/trigger/trigger.root","eff/eff_nominal")
            self.trigger_up = getHist("PhysicsTools/NanoAODTools/data/trigger/trigger.root","eff/eff_up")
            self.trigger_down = getHist("PhysicsTools/NanoAODTools/data/trigger/trigger.root","eff/eff_down")
        self.outputName = outputName
        
    def beginJob(self):
        pass
        
    def endJob(self):
        pass
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        self.out.branch(self.outputName+"_flag","I")

        if not self.globalOptions["isData"]:
            self.out.branch(self.outputName+"_weight_trigger_nominal", "F")
            self.out.branch(self.outputName+"_weight_trigger_up", "F")
            self.out.branch(self.outputName+"_weight_trigger_down", "F")

        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        mht = event.nominal_mht
       
        if not self.globalOptions["isData"]:
     
            self.out.fillBranch(
                self.outputName+"_flag",
                event.HLT_MonoCentralPFJet80_PFMETNoMu90_PFMHTNoMu90_IDTight > 0 or
                event.HLT_MonoCentralPFJet80_PFMETNoMu100_PFMHTNoMu100_IDTight > 0 or
                event.HLT_MonoCentralPFJet80_PFMETNoMu110_PFMHTNoMu110_IDTight > 0 or
                event.HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight > 0 or
                event.HLT_PFHT900
            )
     
            weight_trigger_nominal, _ = getX(self.trigger_up, mht)
            weight_trigger_up, _ = getX(self.trigger_up, mht)
            weight_trigger_down, _ = getX(self.trigger_down, mht)
            
            self.out.fillBranch(self.outputName+"_weight_trigger_nominal",weight_trigger_nominal)
            self.out.fillBranch(self.outputName+"_weight_trigger_up",weight_trigger_up)
            self.out.fillBranch(self.outputName+"_weight_trigger_down",weight_trigger_down)

        else:
            self.out.fillBranch(
                self.outputName+"_flag", 1)

        return True
