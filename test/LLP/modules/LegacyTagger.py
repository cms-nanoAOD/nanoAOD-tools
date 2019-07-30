import os
import sys
import math
import json
import ROOT
import random

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from utils import deltaR,getCtauLabel

class LegacyTagger(Module):

    def __init__(
        self,
        inputCollection = lambda event: Collection(event, "Jet"),
        globalOptions={"isData":False}
    ):
        self.globalOptions = globalOptions
        self.inputCollection = inputCollection
 
    def beginJob(self):
        pass
        
    def endJob(self):
        pass
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        self.out.branch("legacyTag_alpha", "F",lenVar="nselectedJets")
        self.out.branch("legacyTag_median_dxy", "F",lenVar="nselectedJets")
        self.out.branch("legacyTag_median_trackSip2dSig", "F",lenVar="nselectedJets")
        
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
            
        jets = self.inputCollection(event)
        legacyTag = Collection(event, "legacyTag")

        alphas = []
        median_dxys = []
        median_trackSip2dSigs = []
        
        for jet in jets:
            alphas.append(event.legacyTag_alpha[jet._index])
            median_dxys.append(event.legacyTag_median_dxy[jet._index])
            median_trackSip2dSigs.append(event.legacyTag_median_trackSip2dSig[jet._index])
                    
        self.out.fillBranch("legacyTag_alpha", alphas)
        self.out.fillBranch("legacyTag_median_dxy", median_dxys)
        self.out.fillBranch("legacyTag_median_trackSip2dSig", median_trackSip2dSigs)
        
        return True
        
