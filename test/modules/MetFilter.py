import os
import sys
import math
import json
import ROOT
import random

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class MetFilter(Module):
    def __init__(self,globalOptions={"isData":False}, outputName=None):
        self.globalOptions=globalOptions
        self.outputName=outputName
        
    def beginJob(self):
        pass
        
    def endJob(self):
        pass
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        if self.outputName is not None:
            self.out.branch(self.outputName, "I")
            
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def passFilters(self,event):
        #https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFiltersRun2
        if event.Flag_goodVertices==0:
            return False
        if event.Flag_globalSuperTightHalo2016Filter==0:
            return False
        if event.Flag_HBHENoiseFilter==0:
            return False
        if event.Flag_HBHENoiseIsoFilter==0:
            return False
        if event.Flag_EcalDeadCellTriggerPrimitiveFilter==0:
            return False
        if event.Flag_BadPFMuonFilter==0:
            return False
        if self.globalOptions["isData"] and event.Flag_eeBadScFilter==0: #not suggested on MC
            return False
        return True
        
    def analyze(self, event):
        if self.outputName is not None:
            self.out.fillBranch(self.outputName, self.passFilters(event))
            return True
        else:
            return self.passFilters(event)
            
            
